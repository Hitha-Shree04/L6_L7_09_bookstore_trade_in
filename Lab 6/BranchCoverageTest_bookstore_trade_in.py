import pytest
from bookstore_trade_in import process_book_buybacks, inspect_scanner_calibration

"""
Branch Coverage Test Suite for bookstore_trade_in.py
Student Name: Hitha Shree Suresh
SRN: PES2UG24CS196
Section: D

Objective:
Achieve 100% Branch Coverage by systematically evaluating every conditional
decision structure (if, elif, else), loop boundaries, and logical operator branches
to both True and False pathways.
"""

# =======================================================================
# 1. Tests for process_book_buybacks - Input Validation Branches
# =======================================================================

def test_input_validation_invalid_batches_type():
    """Branch: not isinstance(batches, list) evaluates to True."""
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks("invalid_batches_type", 10.0)


def test_input_validation_negative_store_credit_bonus():
    """Branch: store_credit_bonus < 0 evaluates to True (with valid list)."""
    with pytest.raises(ValueError, match="Invalid batches list or credit bonus"):
        process_book_buybacks([], -5.0)


def test_input_validation_empty_valid_batches():
    """
    Branch: not isinstance(batches, list) is False AND store_credit_bonus < 0 is False.
    Loops do not execute; total_payout == 0.0 evaluates to True -> ZERO_CREDIT.
    """
    result = process_book_buybacks([], 5.0)
    assert result == {"total_payout": 0.0, "status": "ZERO_CREDIT"}


# =======================================================================
# 2. Tests for Batch Approval & Format Types (Decision Branches)
# =======================================================================

def test_batch_intake_unapproved_skipped():
    """
    Branch: not batch.get("intake_approved", False) evaluates to True.
    Skipped batch should not add to payout or rejected count.
    """
    batches = [
        {
            "intake_approved": False,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        },
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


def test_batch_format_textbook_branch():
    """Branch: format_type == 'textbook' evaluates to True (base_value = 40.0)."""
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


def test_batch_format_hardcover_branch():
    """Branch: format_type == 'hardcover' evaluates to True (base_value = 15.0)."""
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


def test_batch_format_paperback_branch():
    """Branch: format_type == 'paperback' evaluates to True (base_value = 8.0)."""
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


def test_batch_format_unknown_rejection_branch():
    """Branch: unknown format falls through all format elifs to else -> rejected_items += 1."""
    batches = [
        {
            "intake_approved": True,
            "format": "digital_audiobook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


# =======================================================================
# 3. Tests for Book Condition, Missing Pages & Counterfeits
# =======================================================================

def test_book_missing_pages_rejection_branch():
    """Branch: pages_missing > 0 evaluates to True -> rejected_items += 1, continue."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 5, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_book_counterfeit_textbook_breaks_loop():
    """
    Branch: is_counterfeit is True AND format_type == 'textbook' is True.
    Sets batch_credit = 0.0 and breaks inner loop immediately.
    """
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 0, "condition": "good", "counterfeit": True},
                {"missing_pages": 0, "condition": "mint", "counterfeit": False}  # Should not be processed
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_book_counterfeit_non_textbook_branch():
    """
    Branch: is_counterfeit is True AND format_type == 'textbook' is False.
    Executes batch_credit += 0.0 without breaking loop.
    """
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
    # 0.0 + 15.0 = 15.0
    assert result["total_payout"] == 15.0
    assert result["status"] == "COMPLETED"


def test_book_condition_mint_branch():
    """Branch: condition == 'mint' evaluates to True (multiplier 1.25)."""
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "mint", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # 40.0 * 1.25 = 50.0
    assert result["total_payout"] == 50.0
    assert result["status"] == "COMPLETED"


def test_book_condition_poor_branch():
    """Branch: condition == 'poor' evaluates to True (multiplier 0.40)."""
    batches = [
        {
            "intake_approved": True,
            "format": "textbook",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "poor", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # 40.0 * 0.40 = 16.0
    assert result["total_payout"] == 16.0
    assert result["status"] == "COMPLETED"


def test_book_condition_default_good_branch():
    """Branch: condition is neither 'mint' nor 'poor' (falls to else -> base_value)."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "average", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


# =======================================================================
# 4. Tests for Store Credit Bonus & Status Outputs
# =======================================================================

def test_payout_in_credit_true_adds_bonus():
    """Branch: batch.get('payout_in_credit', False) evaluates to True."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": True,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 12.50)
    # 8.0 + 12.50 = 20.50
    assert result["total_payout"] == 20.50
    assert result["status"] == "COMPLETED"


def test_payout_in_credit_false_skips_bonus():
    """Branch: batch.get('payout_in_credit', False) evaluates to False."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [{"missing_pages": 0, "condition": "good", "counterfeit": False}]
        }
    ]
    result = process_book_buybacks(batches, 12.50)
    assert result["total_payout"] == 8.0
    assert result["status"] == "COMPLETED"


def test_status_audit_rejected_branch():
    """Branch: rejected_items > 4 evaluates to True -> AUDIT_REJECTED."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 1, "condition": "good", "counterfeit": False},
                {"missing_pages": 2, "condition": "good", "counterfeit": False},
                {"missing_pages": 3, "condition": "good", "counterfeit": False},
                {"missing_pages": 4, "condition": "good", "counterfeit": False},
                {"missing_pages": 5, "condition": "good", "counterfeit": False},
                {"missing_pages": 0, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    # 1 good book payout = 8.0, but rejected_items = 5 (> 4)
    assert result["total_payout"] == 8.0
    assert result["status"] == "AUDIT_REJECTED"


def test_status_zero_credit_branch():
    """Branch: rejected_items <= 4 AND total_payout == 0.0 evaluates to True -> ZERO_CREDIT."""
    batches = [
        {
            "intake_approved": True,
            "format": "paperback",
            "payout_in_credit": False,
            "books": [
                {"missing_pages": 1, "condition": "good", "counterfeit": False}
            ]
        }
    ]
    result = process_book_buybacks(batches, 0.0)
    assert result["total_payout"] == 0.0
    assert result["status"] == "ZERO_CREDIT"


def test_status_completed_normal_branch():
    """Branch: rejected_items <= 4 AND total_payout > 0.0 -> COMPLETED."""
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


# =======================================================================
# 5. Tests for inspect_scanner_calibration - Matrix and Streak Branches
# =======================================================================

def test_scanner_matrix_empty_no_data():
    """Branch: not scanner_matrix evaluates to True -> NO_DATA."""
    assert inspect_scanner_calibration([]) == "NO_DATA"
    assert inspect_scanner_calibration(None) == "NO_DATA"


def test_scanner_streak_recalibrate():
    """
    Branch: error_rate > 5 is True twice consecutively -> misread_streak >= 2 is True.
    Returns 'RECALIBRATE'.
    """
    matrix = [[2, 6, 9, 3]]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"


def test_scanner_streak_resets_when_error_low():
    """
    Branch: error_rate > 5 is True once (streak = 1), then error_rate <= 5 is False (streak resets to 0).
    Never reaches streak >= 2 -> returns 'CALIBRATED'.
    """
    matrix = [
        [6, 2, 6, 1, 4]  # error 6 (streak=1), error 2 (streak=0), error 6 (streak=1), error 1 (streak=0)
    ]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_multiple_devices_calibrated():
    """
    Branch: multiple device readings iterate through outer loop cleanly.
    All device readings stay within safe thresholds -> returns 'CALIBRATED'.
    """
    matrix = [
        [1, 2, 3],
        [4, 5, 2],
        [0, 1, 0]
    ]
    assert inspect_scanner_calibration(matrix) == "CALIBRATED"


def test_scanner_recalibrate_on_second_device():
    """
    Branch: first device passes, second device encounters consecutive misreads >= 2.
    """
    matrix = [
        [1, 2, 3],
        [7, 8, 1]
    ]
    assert inspect_scanner_calibration(matrix) == "RECALIBRATE"
