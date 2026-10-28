import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

"""
Lab 6: Code and Branch Coverage Analysis
Bookstore Trade-In Buyback & Scanner Calibration Test Suite

Student Details:
- Name: Hitha Shree Suresh
- SRN: PES2UG24CS196
- Section: D

Coverage Targets:
- Line Coverage: 100% (57/57 statements)
- Branch Coverage: 100% (40/40 branches)
"""

# =======================================================================
# Baseline Starter Test Case
# =======================================================================

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


# =======================================================================
# Input Validation & Guard Clause Branches
# =======================================================================

def test_invalid_batches_type():
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks("invalid_not_a_list", 5.0)


def test_negative_store_credit_bonus():
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks([], -1.0)


def test_empty_batches_zero_credit():
    result = process_book_buybacks([], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


# =======================================================================
# Batch Approval & Format Decision Branches
# =======================================================================

def test_unapproved_batch_skipped():
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


def test_format_textbook():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 40.0
    assert result["status"] == "COMPLETED"


def test_format_hardcover():
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


def test_format_paperback():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_format_unrecognized_rejection():
    batches = [
        {
            "intake_approved": True,
            "format": "audiobook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# =======================================================================
# Book Attributes, Missing Pages, Counterfeit & Condition Branches
# =======================================================================

def test_book_missing_pages_rejected():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 3, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_textbook_counterfeit_breaks_batch():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
                {"missing_pages": 0, "condition": "mint", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_non_textbook_counterfeit_adds_zero():
    batches = [
        {
            "intake_approved": True,
            "format": "hardcover",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


def test_book_condition_mint():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 50.0
    assert result["status"] == "COMPLETED"


def test_book_condition_poor():
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 16.0
    assert result["status"] == "COMPLETED"


def test_book_condition_other_default_good():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "fair", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


# =======================================================================
# Store Credit Bonus & Final Payout Status Branches
# =======================================================================

def test_store_credit_bonus_applied():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": True,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 5.0)
    assert result["total_payout"] == 13.0
    assert result["status"] == "COMPLETED"


def test_audit_rejected_status_exceeds_threshold():
    batches = [
        {"intake_approved": True, "format": "unknown_1", "books": []},
        {"intake_approved": True, "format": "unknown_2", "books": []},
        {"intake_approved": True, "format": "unknown_3", "books": []},
        {"intake_approved": True, "format": "unknown_4", "books": []},
        {"intake_approved": True, "format": "unknown_5", "books": []},
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["status"] == "AUDIT_REJECTED"


def test_zero_credit_status_with_low_rejected():
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 1, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# =======================================================================
# Scanner Calibration Tests
# =======================================================================

def test_scanner_matrix_empty():
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration(None) == "NO_DATA"


def test_scanner_recalibrate_on_streak():
    matrix = [[2, 7, 8, 1]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"


def test_scanner_streak_reset_calibrated():
    matrix = [[7, 2, 7, 3, 4]]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_multiple_devices_clean():
    matrix = [
        [1, 2, 3],
        [4, 5, 2],
        [0, 1, 0]
    ]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_device_two_recalibrate():
    matrix = [
        [1, 2, 3],
        [6, 9, 0]
    ]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"