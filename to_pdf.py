import os
from pypdf import PdfReader, PdfWriter
from fpdf import FPDF
import xml.etree.ElementTree as ET
from xml_extractor import get_client_data, fetch_financial_message, fetch_account_currency, fetch_cards, fetch_transaction_details

class PdfFile:
    def __init__(self, output_folder="Statements", password=None, logo_path=None):
        self.output_folder = output_folder
        self.password = password
        self.logo_path = logo_path
        self.create_directory(self.output_folder)

    @staticmethod
    def create_directory(directory):
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

    def generate_pdf(self, client_data, financial_message, account_currency, cards, transactions):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Logo
        if self.logo_path:
            pdf.image(self.logo_path, x=80, y=10, w=50)

        # Title
        pdf.set_xy(10, 40)
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(190, 10, 'CUSTOMER STATEMENT', ln=True, align='C')

        self._add_client_info(pdf, client_data)
        if financial_message:
            self._add_financial_message(pdf, financial_message)
        if account_currency:
            self._add_account_currency(pdf, account_currency)
        if cards:
            self._add_cards(pdf, cards)
        if transactions:
            self._add_transactions(pdf, transactions)

        filename = os.path.join(self.output_folder, f"{client_data.get('EMAIL_TO', 'Client')}.pdf")
        pdf.output(filename)
        print(f"Generated PDF for client {client_data.get('EMAIL_TO', 'Client')} at {filename}")
        return filename

    def _add_client_info(self, pdf, client_data):
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(128, 0, 0)
        pdf.set_xy(10, 50)
        pdf.cell(190, 10, 'Client Information', ln=True, align='L')

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0)
        pdf.cell(95, 8, f"ACCOUNT NUMBER: {client_data['PARAMETER_A']}", border=1)
        pdf.cell(95, 8, f"EMAIL ADDRESS: {client_data['EMAIL_TO']}", border=1, ln=True)
        pdf.cell(95, 8, f"STMT FROM: {client_data['STMT_DATE_FROM']}", border=1)
        pdf.cell(95, 8, f"STMT TO: {client_data['STMT_DATE_TO']}", border=1, ln=True)
        pdf.cell(95, 8, f"ADDRESS: {client_data['ADDR_LINE_A']}, {client_data['ADDR_LINE_B']}", border=1, ln=True)

    def _add_financial_message(self, pdf, financial_message):
        pdf.ln(15)
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(128, 0, 0)
        pdf.set_xy(10, 80)
        pdf.cell(190, 10, 'Financial Summary', ln=True, align='L')

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0)
        pdf.cell(95, 8, f"Minimum Amount Value: {financial_message.get('MIN_AMOUNT_VALUE', 'N/A')}", border=1)
        pdf.cell(95, 8, f"Statement Due Date: {financial_message.get('STMT_DUE_DATE', 'N/A')}", border=1, ln=True)
        pdf.cell(95, 8, f"Outstanding Balance: {financial_message.get('OUTSTANDING_BALANCE', 'N/A')}", border=1)
        pdf.cell(95, 8, f"Amount: {financial_message.get('AMOUNT', 'N/A')}", border=1, ln=True)

    def _add_account_currency(self, pdf, account_currency):
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(128, 0, 0)
        pdf.set_xy(10, 110)
        pdf.cell(190, 10, 'Account Information', ln=True, align='L')

        pdf.set_font("Arial", '', 10)
        pdf.set_text_color(0, 0)
        pdf.cell(95, 8, f"Currency: {account_currency.get('CURRENCY', 'N/A')}", border=1)
        pdf.cell(95, 8, f"Currency Code: {account_currency.get('CURRENCY_CODE', 'N/A')}", border=1, ln=True)

    def _add_cards(self, pdf, cards):
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(200, 10, "Card Information", ln=True)

        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(50, 8, "Card", border=1)
        pdf.cell(40, 8, "Available", border=1)
        pdf.cell(30, 8, "S_Plus", border=1)
        pdf.cell(30, 8, "S_Minus", border=1)
        pdf.cell(30, 8, "S_Total", border=1, ln=True)

        # Table Content
        pdf.set_font("Arial", '', 10)
        for card in cards:
            card_value = card.get('TRANS_CARD', 'N/A') or 'N/A'
            card_available = card.get('TR_CARD_AV', 'N/A') or 'N/A'
            s_plus = card.get('S_PLUS_CARD', 'N/A') or 'N/A'
            s_minus = card.get('S_MINUS_CARD', 'N/A') or 'N/A'
            s_total = card.get('S_TOTAL_CARD', 'N/A') or 'N/A'

            pdf.cell(50, 8, str(card_value), border=1)
            pdf.cell(40, 8, str(card_available), border=1)
            pdf.cell(30, 8, str(s_plus), border=1)
            pdf.cell(30, 8, str(s_minus), border=1)
            pdf.cell(30, 8, str(s_total), border=1, ln=True)
        pdf.ln(5)

    def _add_transactions(self, pdf, transactions):
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(128, 0, 0)
        pdf.cell(200, 10, "Transaction Details", ln=True)

        # Table Header
        pdf.set_font("Arial", 'B', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(40, 8, "Transaction Date", border=1)
        pdf.cell(30, 8, "Transaction ID", border=1)
        pdf.cell(20, 8, "Credit", border=1)
        pdf.cell(20, 8, "Debit", border=1)
        pdf.cell(30, 8, "Trans Amount", border=1)
        pdf.cell(50, 8, "Account Amount", border=1, ln=True)

        # Table Content
        pdf.set_font("Arial", '', 10)
        for trans in transactions:
            trans_date = trans.get('TRANS_DATE', 'N/A') or 'N/A'
            trans_id = trans.get('M_TRANSACTION_ID', 'N/A') or 'N/A'
            cr = trans.get('CR', '0.0') or '0.0'
            dr = trans.get('DR', '0.0') or '0.0'
            trans_amount = trans.get('TRANS_AMOUNT', '0.0') or 'N/A'
            trans_details = trans.get('TRANS_DETAILS', '0.0') or 'N/A'
           

            # Ensure the values are properly formatted as strings
            pdf.cell(40, 8, str(trans_date), border=1)
            pdf.cell(30, 8, str(trans_id), border=1)
            pdf.cell(20, 8, str(cr), border=1)
            pdf.cell(20, 8, str(dr), border=1)
            pdf.cell(30, 8, str(trans_amount), border=1)
            pdf.cell(50, 8, str(trans_details), border=1, ln=True)
        pdf.ln(5)

    def password_protect(self, filename, client_id):
        if client_id:
            pdf_path = os.path.join(self.output_folder, filename)
            reader = PdfReader(pdf_path)
            writer = PdfWriter(clone_from=reader)
            writer.encrypt(client_id, algorithm="AES-256")

            encrypted_pdf_path = os.path.join(self.output_folder, f"Locked_{filename}")
            with open(encrypted_pdf_path, "wb") as f:
                writer.write(f)

            print(f"Password protected {filename} with ACNT_CONTRACT_ID and saved as {encrypted_pdf_path}")

def process_data_and_generate_pdfs(xml_file):
    pdf_gen = PdfFile(password=None, logo_path="resources/equity_logo.jpeg")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    clients = root.findall('.//G_CLIENT')

    for client in clients:
        client_data = get_client_data(client)
        financial_message = fetch_financial_message(client)
        account_currency = fetch_account_currency(client)
        cards = fetch_cards(client)
        transactions = fetch_transaction_details(client)

        filename = f"{client_data.get('EMAIL_TO', 'Client')}.pdf"
        pdf_file_path = pdf_gen.generate_pdf(client_data, financial_message, account_currency, cards, transactions)
        
        pdf_gen.password_protect(filename, client_data['PARAMETER_A'][4:])

if __name__ == "__main__":
    process_data_and_generate_pdfs('data.xml')
