# CIT 105 Week 4 — Streamlit Invoice Builder

A Streamlit invoicing application with an exact `Decimal` calculation layer, JSON storage, PDF export, and pytest test suite.

## Required structure
- `calculations.py` — all invoice arithmetic; no Streamlit imports or calls.
- `storage.py` — saves, lists, and reloads invoices as JSON.
- `pdf_export.py` — creates a printable PDF with ReportLab.
- `app.py` — Streamlit interface and session-state line items.
- `test_calculations.py` — automated tests for the calculation layer.

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt
pytest -v
streamlit run app.py
```

## Why discount is applied before tax
The app subtracts the discount from the subtotal first, then calculates tax on the discounted taxable amount. This prevents charging tax on money the customer is not actually paying for the merchandise/services.

## My four added test cases
1. **Empty invoice** — protects against crashes or non-zero totals when there are no line items.
2. **Zero and negative quantity** — confirms zero produces a $0.00 line while a negative quantity is rejected.
3. **Exact half-cent rounding** — checks that `1.005` becomes `1.01` with `ROUND_HALF_UP` instead of binary-float behavior.
4. **100% discount** — verifies the taxable amount, tax, and grand total all become zero.

I also added a large-value precision test to prove the money path stays exact with `Decimal`.

## Session-state interaction test
Manually test this sequence before submission: add a line item → remove it → add another line item. Each item uses a permanent numeric ID rather than its current list position, so widget keys are not accidentally reused after deletion.

## Passing test run
Run `pytest -v` and paste a screenshot of the passing terminal output here before submission.

**Screenshot:** Add a screenshot of the running Streamlit application here, for example `screenshots/app.png`.

## Sample PDF
Generate an invoice in the app, click **Download PDF**, and commit the exported PDF to this repository as `sample-invoice.pdf`.

## AI assistance disclosure
AI assistance was used to help plan and implement the initial application structure and test suite. The required self-identified test cases were reviewed and must be understood by the student for the code-defense checkpoint. Copilot/Claude Code use, if any, should also be disclosed here.
