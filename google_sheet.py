import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_data = json.loads(base64.b64decode(os.getenv("GOOGLE_CREDS_B64")))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)
    return client.open("tycs-line-bot-severless LineMembers").worksheet("UserID")

def add_user(user_id):
    sheet = get_sheet()
    users = sheet.col_values(1)
    if user_id not in users:
        sheet.append_row([user_id])

def get_all_user_ids():
    sheet = get_sheet()
    return sheet.col_values(1)[1:]
