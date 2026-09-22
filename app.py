from datetime import date
from decimal import Decimal, InvalidOperation
import streamlit as st

from calculations import invoice_totals, line_total, money
from storage import save_invoice, load_invoice, list_invoices
from pdf_export import build_invoice_pdf

st.set_page_config(page_title='CIT 105 Invoice App', page_icon='🧾', layout='wide')
st.title('🧾 Invoice Builder')

if 'items' not in st.session_state:
    st.session_state.items = [{'id': 0, 'description': '', 'quantity': '1', 'unit_price': '0.00'}]
if 'next_id' not in st.session_state:
    st.session_state.next_id = 1


def add_item():
    st.session_state.items.append({'id': st.session_state.next_id, 'description': '', 'quantity': '1', 'unit_price': '0.00'})
    st.session_state.next_id += 1


def remove_item(item_id):
    st.session_state.items = [item for item in st.session_state.items if item['id'] != item_id]


def load_selected(name):
    data = load_invoice(name)
    st.session_state.client_name = data.get('client_name', '')
    st.session_state.address = data.get('address', '')
    st.session_state.invoice_number = data.get('invoice_number', '')
    st.session_state.invoice_date = date.fromisoformat(data.get('date'))
    st.session_state.discount_percent = str(data.get('discount_percent', '0'))
    st.session_state.tax_percent = str(data.get('tax_percent', '0'))
    st.session_state.items = []
    for idx, item in enumerate(data.get('items', [])):
        st.session_state.items.append({'id': idx, 'description': item.get('description',''), 'quantity': str(item.get('quantity','1')), 'unit_price': str(item.get('unit_price','0.00'))})
    st.session_state.next_id = len(st.session_state.items)

with st.sidebar:
    st.header('Saved invoices')
    saved = list_invoices()
    selected = st.selectbox('Choose an invoice', [''] + saved)
    if st.button('Load selected', disabled=not selected):
        load_selected(selected)
        st.rerun()

c1, c2 = st.columns(2)
with c1:
    client_name = st.text_input('Client name', key='client_name')
    address = st.text_area('Client address', key='address')
with c2:
    invoice_number = st.text_input('Invoice number', value='INV-001', key='invoice_number')
    invoice_date = st.date_input('Invoice date', value=date.today(), key='invoice_date')

st.subheader('Line items')
for item in list(st.session_state.items):
    cols = st.columns([4, 1, 2, 1])
    item['description'] = cols[0].text_input('Description', value=item['description'], key=f"desc_{item['id']}")
    item['quantity'] = cols[1].text_input('Qty', value=item['quantity'], key=f"qty_{item['id']}")
    item['unit_price'] = cols[2].text_input('Unit price', value=item['unit_price'], key=f"price_{item['id']}")
    if cols[3].button('Remove', key=f"remove_{item['id']}"):
        remove_item(item['id'])
        st.rerun()

st.button('➕ Add line item', on_click=add_item)

r1, r2 = st.columns(2)
with r1:
    discount_percent = st.text_input('Discount %', value='0', key='discount_percent')
with r2:
    tax_percent = st.text_input('Tax %', value='0', key='tax_percent')

try:
    clean_items = []
    for item in st.session_state.items:
        qty = Decimal(item['quantity'].strip() or '0')
        price = money(item['unit_price'].strip() or '0')
        total = line_total(qty, price)
        clean_items.append({'description': item['description'], 'quantity': str(qty), 'unit_price': str(price), 'line_total': str(total)})
    totals = invoice_totals(clean_items, Decimal(discount_percent or '0'), Decimal(tax_percent or '0'))
    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric('Subtotal', f"${totals['subtotal']}")
    m2.metric('Discount', f"-${totals['discount']}")
    m3.metric('Tax', f"${totals['tax']}")
    m4.metric('Grand total', f"${totals['grand_total']}")

    invoice = {'client_name': client_name, 'address': address, 'invoice_number': invoice_number, 'date': invoice_date.isoformat(), 'discount_percent': str(Decimal(discount_percent or '0')), 'tax_percent': str(Decimal(tax_percent or '0')), 'items': clean_items}
    b1, b2 = st.columns(2)
    if b1.button('💾 Save invoice'):
        if not invoice_number.strip():
            st.error('Invoice number is required.')
        else:
            path = save_invoice(invoice)
            st.success(f'Saved {path.name}')
    pdf_bytes = build_invoice_pdf(invoice, totals)
    b2.download_button('📄 Download PDF', pdf_bytes, file_name=f'{invoice_number or "invoice"}.pdf', mime='application/pdf')
except (InvalidOperation, ValueError) as exc:
    st.error(f'Please check the quantity, price, discount, and tax fields: {exc}')
