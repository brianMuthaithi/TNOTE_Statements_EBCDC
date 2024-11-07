import xml.etree.ElementTree as ET
import mysql.connector
from xml_extractor import get_client_data, fetch_financial_message, fetch_account_currency, fetch_cards, fetch_transaction_details

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="brian",
        password="root_brian",
        database="unrelated_statements"
    )

# Insert into database functions with debugging
def insert_clients(cursor, client_data):
    try:
        cursor.execute('''
        INSERT INTO clients (
            F_I, PCAT, CON_CAT, PRODUCT, ACNT_CONTRACT_ID, STMT_DATE_FROM, STMT_DATE_TO, MAIN_CONTRACT,
            PARAMETER_A, PARAMETER_B, PARAMETER_C, PARAMETER_D, PARAMETER_E, PARAMETER_F, PARAMETER_G,
            PARAMETER_H, PAYM_IMM_AMNT_ALL, PAYM_DUE_AMNT_ALL, PAYM_DUE_DATE_ALL, ACNT_CONTRACT_CURR,
            ACNT_CONTRACT_CURR_CODE, CREDIT_LIMIT, TOTAL_BLOCKED, AMOUNT_AVAILABLE, CHECK_AVAILABLE,
            ADDR_LINE_A, ADDR_LINE_B, ADDR_LINE_C, ADDR_LINE_D, ADDR_LINE_E, ADDR_LINE_F, MESSAGE_ACC,
            MESSAGE_SP, ADD_INFO, EMAIL_TO
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
    ''', tuple(client_data.values()))
    except Exception as e:
        print(f"Error inserting client data: {e}")

def insert_financial_messages(cursor, fin_message):
    try:
        cursor.execute("""INSERT INTO financial_messages (MIN_AMOUNT_VALUE, STMT_DUE_DATE, OUTSTANDING_BALANCE, OVERDUE_AMOUNT, OVER_LIMIT, LABEL6)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(fin_message.values()))
    except Exception as e:
        print(f"Error inserting financial message: {e}")

def insert_account_currency(cursor, account_curr):
    try:
        cursor.execute("""INSERT INTO account_currency (ACC_CURR_NAME, CURRENCY, BEG_BAL, PAYM_IMM_AMNT_CURR, PAYM_DUE_AMNT_CURR, PAYM_DUE_DATE_CURR)
            VALUES (%s, %s, %s, %s, %s, %s)""", tuple(account_curr.values()))
    except Exception as e:
        print(f"Error inserting account currency: {e}")

def insert_cards(cursor, card):
    try:
        cursor.execute("""INSERT INTO cards (TRANS_CONTRACT_ORDER, CONTRACT_FOR, TRANS_CARD, TRANS_CON_CAT, TR_CARD_AV, S_PLUS_CARD, S_MINUS_CARD, S_TOTAL_CARD)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", tuple(card.values()))
    except Exception as e:
        print(f"Error inserting card: {e}")

def insert_transaction_details(cursor, trans_detail):
    try:
        cursor.execute('''
        INSERT INTO transaction_details (POSTING_DATE, M_TRANSACTION_ID, PARENT_SERVICE, ENTRY_ID, TRANS_DATE, CR, DR, LOCAL_DATE, TRANS_AMOUNT,
            TRANSACTION_ADD_INFO, TRANS_DETAILS, TRANS_CURR, FEE_AMOUNT, ACC_AMOUNT, ACCOUNT_AMOUNT, TRANS_TIME)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', tuple(trans_detail.values()))
    except Exception as e:
        print(f"Error inserting transaction detail: {e}")

# Main function to read XML and insert data into the database
def xml_to_db(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        print("XML read successfully")

        # Extract client data, financial messages, account currencies, cards, and transactions
        clients = root.findall('.//G_CLIENT')
        print(f"Total clients found: {len(clients)}")

        # Connect to the database
        connection = connect_to_db()
        if connection.is_connected:
            print("Connection successful")
            cursor = connection.cursor()

            for client in clients:
                # Insert client data
                client_data = get_client_data(client)
                insert_clients(cursor, client_data)

                # Insert financial message
                fin_message = fetch_financial_message(client)
                if fin_message:
                    insert_financial_messages(cursor, fin_message)

                # Insert account currency data
                account_curr = fetch_account_currency(client)
                if account_curr:
                    insert_account_currency(cursor, account_curr)

                # Insert cards data
                card_list = fetch_cards(client)
                for card in card_list:
                    insert_cards(cursor, card)

                # Insert transaction details
                trans_list = fetch_transaction_details(client)
                for trans in trans_list:
                    insert_transaction_details(cursor, trans)

            connection.commit()
            print("Data inserted into the database successfully!")

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    xml_to_db("data.xml")

