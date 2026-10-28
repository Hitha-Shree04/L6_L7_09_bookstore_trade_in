import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

# Test suite designed to achieve full Code Coverage (Statement / Line Coverage)
# Every line of executable code in bookstore_trade_in.py is executed.

def test_single_paperback_good():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_invalid_batches_input():
    # Covers lines 2-3 (ValueError when batches is not a list)
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks("invalid_batches", 5.0)


def test_unapproved_batch_skipped():
    # Covers line 9-10 (continue when intake_approved is False)
    batches = [
        {
            "intake_approved": False,
            "format": "paperback",
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_unsupported_format_rejected():
    # Covers lines 22-23 (unrecognized format increments rejected_items and continues)
    batches = [
        {
            "intake_approved": True,
            "format": "audiobook",
            "books": []
        },
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_missing_pages_rejected():
    # Covers lines 33-34 (missing pages increments rejected_items and continues)
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "books": [
                {"missing_pages": 4, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_textbook_format_and_counterfeit_break():
    # Covers lines 16 (format textbook) and lines 38-40 (counterfeit textbook sets credit 0 and breaks)
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": True}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # total_payout is 0.0, covers line 57 (ZERO_CREDIT)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_hardcover_mint_with_store_credit_bonus():
    # Covers line 18 (hardcover), line 43 (condition mint * 1.25), and line 50 (payout_in_credit bonus)
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": True,
            "books": [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 10.0)
    # 15.0 * 1.25 = 18.75 + 10.0 = 28.75
    assert result["total_payout"] == 28.75
    assert result["status"] == "COMPLETED"


def test_paperback_poor_and_non_textbook_counterfeit():
    # Covers line 45 (condition poor * 0.40) and line 41 (counterfeit non-textbook += 0.0)
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "poor", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": True}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # 8.0 * 0.40 = 3.20 + 0.0 = 3.20
    assert result["total_payout"] == 3.20
    assert result["status"] == "COMPLETED"


def test_audit_rejected_status():
    # Covers line 55 (rejected_items > 4 -> AUDIT_REJECTED)
    batches = [
        {"intake_approved": True, "format": "magazine_format", "books": []},
        {"intake_approved": True, "format": "scroll_format", "books": []},
        {"intake_approved": True, "format": "pdf_printout", "books": []},
        {"intake_approved": True, "format": "comic_format", "books": []},
        {"intake_approved": True, "format": "unknown_format", "books": []},
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_scanner_no_data():
    # Covers line 63 (empty scanner_matrix -> NO_DATA)
    assert inspect_scanner_calibration([]) == "NO_DATA"


def test_scanner_recalibrate():
    # Covers line 71 (misread streak >= 2 -> RECALIBRATE)
    matrix = [[3, 6, 8, 2]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"


def test_scanner_calibrated():
    # Covers line 73 (reset streak) and line 74 (CALIBRATED)
    matrix = [[2, 6, 1, 6, 4]]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"
