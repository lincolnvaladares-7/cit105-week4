from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal('0.01')


def money(value):
    """Convert input to Decimal currency rounded to cents using half-up rounding."""
    if isinstance(value, Decimal):
        amount = value
    else:
        amount = Decimal(str(value))
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)


def line_total(quantity, unit_price):
    qty = Decimal(str(quantity))
    if qty < 0:
        raise ValueError('Quantity cannot be negative.')
    price = money(unit_price)
    if price < 0:
        raise ValueError('Unit price cannot be negative.')
    return money(qty * price)


def subtotal(items):
    return money(sum((line_total(i['quantity'], i['unit_price']) for i in items), Decimal('0')))


def calculate_discount(subtotal_amount, discount_percent):
    rate = Decimal(str(discount_percent))
    if rate < 0 or rate > 100:
        raise ValueError('Discount must be between 0 and 100 percent.')
    return money(money(subtotal_amount) * rate / Decimal('100'))


def calculate_tax(taxable_amount, tax_percent):
    rate = Decimal(str(tax_percent))
    if rate < 0:
        raise ValueError('Tax rate cannot be negative.')
    return money(money(taxable_amount) * rate / Decimal('100'))


def invoice_totals(items, discount_percent=0, tax_percent=0):
    sub = subtotal(items)
    discount = calculate_discount(sub, discount_percent)
    taxable = money(sub - discount)  # Discount is applied BEFORE tax.
    tax = calculate_tax(taxable, tax_percent)
    grand = money(taxable + tax)
    return {'subtotal': sub, 'discount': discount, 'taxable': taxable, 'tax': tax, 'grand_total': grand}
