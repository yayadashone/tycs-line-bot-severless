import gspread
import json
import base64
import os
import random
import string
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

def get_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_data = json.loads(base64.b64decode(os.getenv("GOOGLE_CREDS_B64")))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_data, scope)
    client = gspread.authorize(creds)
    sh = client.open("tycs-line-bot-severless")
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
def append_event_if_not_exists(event_list):
    sheet = get_sheet("Events")
    existing_keys = set(sheet.col_values(1))
    today = datetime.today().date()
    
    for event in event_list:   
        # 取出事件名稱跟出發時間（去掉前面的標籤）
        title = event['name']
        start_date = event['date_event'].replace('出發時間 : ', '').strip()

        if start_date < today:
                print(f"跳過已過期活動: {title} ({start_date})")
                continue
        
        level = event.get('level', '')
        # key 用事件名稱 + 出發時間
        key = f"{title}-{start_date}"
        if key not in existing_keys:
            # 拆分報名時間成開始跟結束時間，格式是 "報名時間 : yyyy-mm-dd hh:mm ~ yyyy-mm-dd hh:mm"
            reg_start, reg_end , cancel_end= "", "", ""
            try:
                reg_period = event['date_apply'].replace('報名時間 : ', '').strip()
                reg_start, reg_end = [s.strip()[:10] for s in reg_period.split('~')]
                cancel_end = event['date_cancel'].split(':')[1].strip().replace(' 前', '')[:10]

            except Exception:
                pass
                
                # 新增一列
            sheet.append_row([
                key,
                title,
                start_date,
                level,
                reg_start,
                reg_end,
                cancel_end,
                "","" # pushed_start, pushed_end
            ])
            existing_keys.add(key) 



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

