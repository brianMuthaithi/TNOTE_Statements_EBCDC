import xml.etree.ElementTree as ET
import pandas as pd
from xml_extractor import get_client_data, fetch_financial_message, fetch_account_currency, fetch_cards, fetch_transaction_details

def xml_to_excel(xml_file, output_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print("XML read successfully")

        clientele, messages, account_info, card_deets, trans_deets = [], [], [], [], []

        clients = root.findall('.//G_CLIENT')
        print(f"Total clients found: {len(clients)}")

        for client in clients:
            clientele.append(get_client_data(client))

            fin_msg = fetch_financial_message(client)
            if fin_msg:
                messages.append(fin_msg)

            acc_curr = fetch_account_currency(client)
            if acc_curr:
                account_info.append(acc_curr)

            card_list = fetch_cards(client)
            card_deets.extend(card_list)

            trans_list = fetch_transaction_details(client)
            trans_deets.extend(trans_list)

        clients_df = pd.DataFrame(clientele)
        fin_msg_df = pd.DataFrame(messages)
        accounts_df = pd.DataFrame(account_info)
        card_deets_df = pd.DataFrame(card_deets)
        transactions_df = pd.DataFrame(trans_deets)

        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            clients_df.to_excel(writer, sheet_name='Clients', index=False)
            fin_msg_df.to_excel(writer, sheet_name='Fin Message', index=False)
            accounts_df.to_excel(writer, sheet_name='Account Curr', index=False)
            card_deets_df.to_excel(writer, sheet_name='Cards', index=False)
            transactions_df.to_excel(writer, sheet_name='Trans Details', index=False)

        print(f"Data successfully written to {output_file}")

    except Exception as e:
        print(f"Error: {e}")
        

if __name__ == "__main__":
    xml_to_excel("data.xml", 'statements.xlsx')
