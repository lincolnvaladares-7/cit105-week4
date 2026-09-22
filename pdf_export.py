from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def build_invoice_pdf(invoice, totals):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = [Paragraph('INVOICE', styles['Title']), Spacer(1, 10)]
    story.append(Paragraph(f"<b>Invoice #:</b> {invoice['invoice_number']} &nbsp;&nbsp; <b>Date:</b> {invoice['date']}", styles['Normal']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Bill To:</b><br/>{invoice['client_name']}<br/>{invoice['address'].replace(chr(10), '<br/>')}", styles['Normal']))
    story.append(Spacer(1, 18))
    data = [['Description', 'Qty', 'Unit Price', 'Line Total']]
    for item in invoice['items']:
        data.append([item['description'], str(item['quantity']), f"${item['unit_price']}", f"${item['line_total']}"])
    table = Table(data, colWidths=[3.2*inch, .7*inch, 1.1*inch, 1.1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey), ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
        ('GRID',(0,0),(-1,-1),.5,colors.grey), ('ALIGN',(1,1),(-1,-1),'RIGHT'), ('PADDING',(0,0),(-1,-1),6)
    ]))
    story += [table, Spacer(1, 16)]
    summary = [
        ['Subtotal', f"${totals['subtotal']}"],
        [f"Discount ({invoice['discount_percent']}%)", f"-${totals['discount']}"],
        [f"Tax ({invoice['tax_percent']}%)", f"${totals['tax']}"],
        ['Grand Total', f"${totals['grand_total']}"],
    ]
    totals_table = Table(summary, colWidths=[4.9*inch, 1.2*inch], hAlign='RIGHT')
    totals_table.setStyle(TableStyle([('ALIGN',(1,0),(1,-1),'RIGHT'), ('FONTNAME',(0,-1),(-1,-1),'Helvetica-Bold'), ('LINEABOVE',(0,-1),(-1,-1),1,colors.black), ('PADDING',(0,0),(-1,-1),5)]))
    story.append(totals_table)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
