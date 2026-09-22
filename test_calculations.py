from decimal import Decimal
import pytest
from calculations import line_total, invoice_totals, money


def test_normal_invoice_discount_before_tax():
    items = [{'quantity': '2', 'unit_price': '10.00'}, {'quantity': '1', 'unit_price': '5.00'}]
    t = invoice_totals(items, '10', '8')
    assert t['subtotal'] == Decimal('25.00')
    assert t['discount'] == Decimal('2.50')
    assert t['tax'] == Decimal('1.80')
    assert t['grand_total'] == Decimal('24.30')

# Four self-identified cases documented in README:
def test_empty_invoice_is_zero():
    t = invoice_totals([], '0', '7')
    assert t['grand_total'] == Decimal('0.00')


def test_zero_quantity_allowed_but_negative_rejected():
    assert line_total('0', '19.99') == Decimal('0.00')
    with pytest.raises(ValueError):
        line_total('-1', '19.99')


def test_half_cent_rounds_half_up():
    assert money(Decimal('1.005')) == Decimal('1.01')


def test_100_percent_discount_makes_tax_and_total_zero():
    t = invoice_totals([{'quantity': '1', 'unit_price': '123.45'}], '100', '9.5')
    assert t['discount'] == Decimal('123.45')
    assert t['tax'] == Decimal('0.00')
    assert t['grand_total'] == Decimal('0.00')


def test_large_total_keeps_exact_decimal_precision():
    t = invoice_totals([{'quantity': '999999', 'unit_price': '999999999.99'}], '0', '0')
    assert t['grand_total'] == Decimal('999998999990000.01')
