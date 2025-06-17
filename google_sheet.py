import gspread
import json
import base64
import os
import gc
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_data = json.loads(base64.b64decode(os.getenv("GOOGLE_CREDS_B64")))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)
    sh = gc.open("tycs-line-bot-severless")
    return sh.worksheet(sheet_name)

def add_user_if_not_exists(user_id: str):
    sheet = get_sheet("Users")
    user_ids = sheet.col_values(1)
    if user_id not in user_ids:
        sheet.append_row([user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

def get_all_user_ids():
    sheet = get_sheet("Users")
    return sheet.col_values(1)[1:]


# 活動相關
def append_event_if_not_exists(event):
    sheet = get_sheet("Events")
    titles = sheet.col_values(1)
    key = f"{event['title']}-{event['start_date']}"
    if key not in titles:
        sheet.append_row([
            key, event['title'], event['start_date'],
            event['reg_start'], event['reg_end'],
            "", ""  # pushed_start, pushed_end
        ])

def get_all_events():
    sheet = get_sheet("Events")
    records = sheet.get_all_records()
    result = []
    for r in records:
        result.append({
            "key": r["key"],
            "title": r["title"],
            "start_date": r["start_date"],
            "reg_start": r["reg_start"],
            "reg_end": r["reg_end"],
            "pushed_start": r["pushed_start"] != "",
            "pushed_end": r["pushed_end"] != "",
        })
    return result

def update_push_status(key, which):  # which = "start" or "end"
    sheet = get_sheet("Events")
    records = sheet.get_all_values()
    for i, row in enumerate(records):
        if i == 0:
            continue  # skip header
        if row[0] == key:
            col = 6 if which == "start" else 7
            sheet.update_cell(i+1, col, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            break

