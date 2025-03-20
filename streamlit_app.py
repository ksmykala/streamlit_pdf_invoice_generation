import streamlit as st
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from datetime import datetime, timedelta
from pathlib import Path


PDF_TEMPLATE_DIR = './assets'
PDF_OUTPUT_DIR = './generated_invoices'


def app():
    st.set_page_config(page_title='🖨 PrintIT!')
    st.title('PrintIT!🖨️')

    client_name = st.text_input('Client Name')
    invoice_price = st.number_input('Invoice Price', value=75.5)
    invoice_quantity = st.number_input('Invoice Quantity', value=40)

    if st.button('Generate PDF'):
        with st.spinner('Generating PDF...'):
            pdf_path = generate_inovice_pdf(
                invoice_details={
                    'client_name': client_name,
                    'invoice_price': invoice_price,
                    'invoice_quantity': invoice_quantity
                },
            )
            st.success('PDF Generated Successfully!')
            st.balloons()

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    'Download PDF', pdf_file, file_name=pdf_path.name)


# TODO: use jinja2 for templating
def generate_invoice_content(client_name, invoice_price, invoice_quantity):
    invoice_template = open(f'{PDF_TEMPLATE_DIR}/invoice.html').read()
    invoice_template = invoice_template.replace(
        'client_name', client_name)
    invoice_template = invoice_template.replace(
        'invoice_price', str(invoice_price))
    invoice_template = invoice_template.replace(
        'invoice_quantity', str(invoice_quantity))
    invoice_template = invoice_template.replace(
        'invoice_total', str(invoice_price * invoice_quantity))
    invoice_template = invoice_template.replace(
        'invoice_date', datetime.now().strftime('%Y-%m-%d'))
    invoice_template = invoice_template.replace(
        'invoice_due_date',
        (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))

    return invoice_template


def generate_inovice_pdf(invoice_details):
    invoice_content = generate_invoice_content(**invoice_details)

    pdf_filename = f'{PDF_OUTPUT_DIR}/invoice_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
    font_config = FontConfiguration()
    html = HTML(string=invoice_content)
    css = CSS(
        string=open(f'{PDF_TEMPLATE_DIR}/invoice.css').read(),
        font_config=font_config)
    html.write_pdf(pdf_filename, stylesheets=[css], font_config=font_config)

    return Path(pdf_filename)


if __name__ == '__main__':
    app()
