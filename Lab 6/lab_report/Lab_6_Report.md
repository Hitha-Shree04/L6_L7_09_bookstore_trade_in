# Lab 6: Code and Branch Coverage Analysis

**Name:** Hitha Shree Suresh  
**SRN:** PES2UG24CS196  
**Section:** D  
**Assigned Repository:** SETAPESU26/L6_L7_09_bookstore_trade_in (`bookstore_trade_in.py`)  

---

## 1. Code Coverage Analysis

### Commands Used:
```bash
coverage run -m pytest CodeCoverageTest_bookstore_trade_in.py
coverage report -m
```

### Test Implementation & Results:
Wrote 12 unit test cases in `CodeCoverageTest_bookstore_trade_in.py` targeting all statements in `bookstore_trade_in.py`.

- **Statements:** 57
- **Missed:** 0
- **Line Coverage Achieved:** **100%** (Requirement: >= 90%)
- **Test Result:** 12 passed in 0.06s

| Test Case | Target Statements / Logic | Expected Result |
| :--- | :--- | :--- |
| `test_single_paperback_good` | Standard paperback ($8 base, good condition) | Payout: $8.0, COMPLETED |
| `test_invalid_batches_input` | Guard clause: batches is not a list (lines 2-3) | ValueError raised |
| `test_unapproved_batch_skipped` | Intake approved guard (`intake_approved=False`) | Batch skipped, payout $8.0 |
| `test_unsupported_format_rejected` | Unknown format rejection (lines 22-23) | Batch rejected, payout $8.0 |
| `test_missing_pages_rejected` | Condition `missing_pages > 0` (lines 33-34) | Book rejected, payout $8.0 |
| `test_textbook_format_and_counterfeit` | Textbook format ($40) & counterfeit break | Payout: $0.0, ZERO_CREDIT |
| `test_hardcover_mint_credit_bonus` | Hardcover ($15) * mint (1.25) + $10 bonus | Payout: $28.75, COMPLETED |
| `test_paperback_poor_and_counterfeit` | Poor condition (0.4x) + non-textbook counterfeit | Payout: $3.20, COMPLETED |
| `test_audit_rejected_status` | Threshold `rejected_items > 4` (line 55) | Status: AUDIT_REJECTED |
| `test_scanner_no_data` | Empty scanner matrix (lines 62-63) | Returns NO_DATA |
| `test_scanner_recalibrate` | Error rates > 5 triggering recalibration | Returns RECALIBRATE |
| `test_scanner_calibrated` | Error rates <= 5 resetting streak | Returns CALIBRATED |

### Terminal Output Screenshot:
![Code Coverage Terminal Output](screenshots/code_coverage_analysis.png)

---

## 2. Branch Coverage Analysis

### Commands Used:
```bash
coverage run --branch -m pytest BranchCoverageTest_bookstore_trade_in.py
coverage report -m
```

### Test Implementation & Results:
Wrote 24 unit test cases in `BranchCoverageTest_bookstore_trade_in.py` to evaluate both True and False outcomes for every decision point in `bookstore_trade_in.py`.

- **Total Branches:** 40
- **Partial Branches:** 0
- **Branches Missed:** 0
- **Branch Coverage Achieved:** **100%** (Requirement: >= 90%)
- **Test Result:** 24 passed in 0.07s

| Decision Point / Condition | Line | True Branch Tested | False Branch Tested |
| :--- | :---: | :--- | :--- |
| `not isinstance(batches, list)` | 2 | String input -> raises ValueError | Valid list -> execution proceeds |
| `store_credit_bonus < 0` | 2 | Negative bonus -> raises ValueError | Valid bonus -> execution proceeds |
| `not batch.get('intake_approved')` | 9 | `approved=False` -> batch skipped | `approved=True` -> batch processed |
| `format_type == 'textbook'` | 15 | Textbook -> base price $40.0 | Other format -> checks hardcover |
| `format_type == 'hardcover'` | 17 | Hardcover -> base price $15.0 | Other format -> checks paperback |
| `format_type == 'paperback'` | 19 | Paperback -> base price $8.0 | Unknown format -> rejected |
| `pages_missing > 0` | 32 | Pages missing -> item rejected | Pages missing == 0 -> checks counterfeit |
| `is_counterfeit and textbook` | 38 | Counterfeit textbook -> break, payout 0 | Non-textbook / legitimate book |
| `condition == 'mint' / 'poor'` | 42 | Mint (1.25x), Poor (0.40x) multipliers | Good / other -> 1.0x multiplier |
| `payout_in_credit == True` | 49 | Bonus added to batch payout | Bonus not added |
| `rejected_items > 4` | 54 | 5 rejected items -> AUDIT_REJECTED | <= 4 rejected -> checks payout |
| `error_rate > 5 (scanner)` | 70 | Error > 5 -> increments streak | Error <= 5 -> resets streak to 0 |

### Terminal Output Screenshot:
![Branch Coverage Terminal Output](screenshots/branch_coverage_analysis.png)

---

## 3. Line Coverage vs. Branch Coverage Analysis

### Difference:
- **Line Coverage:** Verifies whether each line of code was executed at least once.
- **Branch Coverage:** Verifies whether every control structure (`if`, `elif`, loop conditions) evaluated to both `True` and `False`.

### Why Line Coverage Alone Gives a False Sense of Security:
Line coverage only checks that execution reached a statement. If an `if` statement does not have an `else` branch, testing only the scenario where the condition is `True` achieves 100% line coverage, while completely ignoring the `False` execution path.

**Examples in `bookstore_trade_in.py`:**
1. **Store Credit Bonus (Line 49):**
   ```python
   if batch.get("payout_in_credit"):
       batch_payout += store_credit_bonus
   ```
   Testing only `payout_in_credit=True` executes line 50 and reports 100% line coverage for that block. The alternate path where `payout_in_credit=False` is never tested. Any logic bug or state issue occurring when credit is not requested would remain undetected.
2. **Scanner Misread Streak Reset (Line 70):**
   Testing only scans where `error_rate > 5` covers the streak increment. However, branch coverage requires testing `error_rate <= 5` to confirm that clean reads properly reset `consecutive_misreads = 0`.

---

## 4. Git Commits

| Commit Hash | Commit Message | Files Committed |
| :---: | :--- | :--- |
| `b027b4c` | Add code coverage test suite achieving 100% line coverage and terminal screenshot | `CodeCoverageTest_bookstore_trade_in.py`, `screenshots/code_coverage_analysis.png`, `.gitignore` |
| `fa10ccb` | Add branch coverage test suite achieving 100% branch coverage and terminal screenshot | `BranchCoverageTest_bookstore_trade_in.py`, `test_bookstore_trade.py`, `screenshots/branch_coverage_analysis.png`, `screenshots/baseline_initial_coverage.png` |
| `d7b2a17` | Add comprehensive lab report deliverables (DOCX, PDF, and Markdown) | `Lab 6/lab_report/Lab_6_Report.md`, `PES2UG24CS196_Hitha_Shree_Suresh.docx`, `PES2UG24CS196_Hitha_Shree_Suresh.pdf` |
