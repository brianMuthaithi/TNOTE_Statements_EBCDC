import xml.etree.ElementTree as ET

def safe_get_text(element, default=''):
    return element.text if element is not None else default

def get_client_data(client):
    return {
        'F_I': safe_get_text(client.find('F_I')),
        'PCAT': safe_get_text(client.find('PCAT')),
        'CON_CAT': safe_get_text(client.find('CON_CAT')),
        'PRODUCT': safe_get_text(client.find('PRODUCT')),
        'ACNT_CONTRACT_ID': safe_get_text(client.find('ACNT_CONTRACT_ID')),
        'STMT_DATE_FROM': safe_get_text(client.find('STMT_DATE_FROM')),
        'STMT_DATE_TO': safe_get_text(client.find('STMT_DATE_TO')),
        'MAIN_CONTRACT': safe_get_text(client.find('MAIN_CONTRACT')),
        'PARAMETER_A': safe_get_text(client.find('PARAMETER_A')),
        'PARAMETER_B': safe_get_text(client.find('PARAMETER_B')),
        'PARAMETER_C': safe_get_text(client.find('PARAMETER_C')),
        'PARAMETER_D': safe_get_text(client.find('PARAMETER_D')),
        'PARAMETER_E': safe_get_text(client.find('PARAMETER_E')),
        'PARAMETER_F': safe_get_text(client.find('PARAMETER_F')),
        'PARAMETER_G': safe_get_text(client.find('PARAMETER_G')),
        'PARAMETER_H': safe_get_text(client.find('PARAMETER_H')),
        'PAYM_IMM_AMNT_ALL': safe_get_text(client.find('PAYM_IMM_AMNT_ALL')),
        'PAYM_DUE_AMNT_ALL': safe_get_text(client.find('PAYM_DUE_AMNT_ALL')),
        'PAYM_DUE_DATE_ALL': safe_get_text(client.find('PAYM_DUE_DATE_ALL')),
        'ACNT_CONTRACT_CURR': safe_get_text(client.find('ACNT_CONTRACT_CURR')),
        'ACNT_CONTRACT_CURR_CODE': safe_get_text(client.find('ACNT_CONTRACT_CURR_CODE')),
        'CREDIT_LIMIT': safe_get_text(client.find('CREDIT_LIMIT')),
        'TOTAL_BLOCKED': safe_get_text(client.find('TOTAL_BLOCKED')),
        'AMOUNT_AVAILABLE': safe_get_text(client.find('AMOUNT_AVAILABLE')),
        'CHECK_AVAILABLE': safe_get_text(client.find('CHECK_AVAILABLE')),
        'ADDR_LINE_A': safe_get_text(client.find('ADDR_LINE_A')),
        'ADDR_LINE_B': safe_get_text(client.find('ADDR_LINE_B')),
        'ADDR_LINE_C': safe_get_text(client.find('ADDR_LINE_C')),
        'ADDR_LINE_D': safe_get_text(client.find('ADDR_LINE_D')),
        'ADDR_LINE_E': safe_get_text(client.find('ADDR_LINE_E')),
        'ADDR_LINE_F': safe_get_text(client.find('ADDR_LINE_F')),
        'MESSAGE_ACC': safe_get_text(client.find('MESSAGE_ACC')),
        'MESSAGE_SP': safe_get_text(client.find('MESSAGE_SP')),
        'ADD_INFO': safe_get_text(client.find('ADD_INFO')),
        'EMAIL_TO': safe_get_text(client.find('EMAIL_TO')),
    }

def fetch_financial_message(client):
    fin_message = client.find('.//G_FINMESSAGE')
    if fin_message is not None:
        return {
            'MIN_AMOUNT_VALUE': safe_get_text(fin_message.find('VALUE1')),
            'STMT_DUE_DATE': safe_get_text(fin_message.find('VALUE2')),
            'OUTSTANDING_BALANCE': safe_get_text(fin_message.find('VALUE3')),
            'OVERDUE_AMOUNT': safe_get_text(fin_message.find('VALUE4')),
            'OVER_LIMIT': safe_get_text(fin_message.find('VALUE5')),
            'LABEL6': safe_get_text(fin_message.find('VALUE6')),
        }
    return None

def fetch_account_currency(client):
    account_curr = client.find('.//G_ACC_CURR')
    if account_curr is not None:
        return {
            'ACC_CURR_NAME': safe_get_text(account_curr.find('ACC_CURR_NAME')),
            'CURRENCY': safe_get_text(account_curr.find('ACC_CURR')),
            'BEG_BAL': safe_get_text(account_curr.find('BEG_BAL')),
            'PAYM_IMM_AMNT_CURR': safe_get_text(account_curr.find('PAYM_IMM_AMNT_CURR')),
            'PAYM_DUE_AMNT_CURR': safe_get_text(account_curr.find('PAYM_DUE_AMNT_CURR')),
            'PAYM_DUE_DATE_CURR': safe_get_text(account_curr.find('PAYM_DUE_DATE_CURR')),
        }
    return None

def fetch_cards(client):
    cards = client.findall('.//G_TRANS_CARD')
    card_list = []
    for card in cards:
        card_info = {
            'TRANS_CONTRACT_ORDER': safe_get_text(card.find('TRANS_CONTRACT_ORDER')),
            'CONTRACT_FOR': safe_get_text(card.find('CONTRACT_FOR')),
            'TRANS_CARD': safe_get_text(card.find('TRANS_CARD')),
            'TRANS_CON_CAT': safe_get_text(card.find('TRANS_CON_CAT')),
            'TR_CARD_AV': safe_get_text(card.find('TR_CARD_AV')),
            'S_PLUS_CARD': safe_get_text(card.find('S_PLUS_CARD')),
            'S_MINUS_CARD': safe_get_text(card.find('S_MINUS_CARD')),
            'S_TOTAL_CARD': safe_get_text(card.find('S_TOTAL_CARD'))
        }
        card_list.append(card_info)
    return card_list

def fetch_transaction_details(client):
    trans_details = client.findall('.//G_TRANS_DETAILS')
    trans_list = []
    for detail in trans_details:
        trans_info = {
            'POSTING_DATE': safe_get_text(detail.find('POSTING_DATE')),
            'M_TRANSACTION_ID': safe_get_text(detail.find('M_TRANSACTION_ID')),
            'PARENT_SERVICE': safe_get_text(detail.find('PARENT_SERVICE')),
            'ENTRY_ID': safe_get_text(detail.find('ENTRY_ID')),
            'TRANS_DATE': safe_get_text(detail.find('TRANS_DATE')),
            'CR': safe_get_text(detail.find('CR')),
            'DR': safe_get_text(detail.find('DR')),
            'LOCAL_DATE': safe_get_text(detail.find('LOCAL_DATE')),
            'TRANS_AMOUNT': safe_get_text(detail.find('TRANS_AMOUNT')),
            'TRANSACTION_ADD_INFO': safe_get_text(detail.find('TRANSACTION_ADD_INFO')),
            'TRANS_DETAILS': safe_get_text(detail.find('TRANS_DETAILS')),
            'TRANS_CURR': safe_get_text(detail.find('TRANS_CURR')),
            'FEE_AMOUNT': safe_get_text(detail.find('FEE_AMOUNT')),
            'ACC_AMOUNT': safe_get_text(detail.find('ACC_AMOUNT')),
            'ACCOUNT_AMOUNT': safe_get_text(detail.find('ACCOUNT_AMOUNT')),
            'TRANS_TIME': safe_get_text(detail.find('TRANS_TIME')),
        }
        trans_list.append(trans_info)
    return trans_list
