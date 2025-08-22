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


def remove_expired_events():
    sheet = get_sheet("Events")
    records = sheet.get_all_values()

    header = records[0]
    rows = records[1:]
    today = datetime.today().date()

    # 找出出發日期欄位索引
    try:
        start_date_idx = header.index("start_date")
    except ValueError:
        print("❌ 找不到 'start_date' 欄位")
        return

    # 由後往前刪除，避免索引錯亂
    for i in reversed(range(len(rows))):
        row = rows[i]
        try:
            date_str = row[start_date_idx]
            event_date = datetime.strptime(date_str, "%Y/%m/%d").date()
            if event_date < today:
                sheet.delete_rows(i + 2)  # 加 2：因為有標題列（第 1 列）
                print(f"🗑️ 刪除過期活動：{row[1]}（{date_str}）")
        except Exception as e:
            print(f"⚠️ 無法處理第 {i+2} 列：{e}")



# 活動相關
def append_event_if_not_exists(event_list):
    
    remove_expired_events() 
    sheet = get_sheet("Events")
    existing_keys = set(sheet.col_values(1))
    today = datetime.today().date()
    
    for event in event_list:   
        # 取出事件名稱跟出發時間（去掉前面的標籤）
        title = event['name']
        event_url = event['event_url']
        start_date = event['date_event'].replace('出發時間 : ', '').strip()
        start_date_val = datetime.strptime(start_date, "%Y/%m/%d").date()

        if start_date_val < today:
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


                event_url = event['event_url']


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
                "","", # pushed_start, pushed_end
                link
            ])
            existing_keys.add(key) 
    print(f"共新增 {len(existing_keys)} 個活動")



def get_all_events():
    sheet = get_sheet("Events")
    records = sheet.get_all_records()
    result = []
    for r in records:
        result.append({
            "key": r["key"],
            "title": r["title"],
            "start_date": r["start_date"],
            "level": r["level"],
            "reg_start": r["reg_start"],
            "reg_end": r["reg_end"],
            "cancel_end": r["cancel_end"],
            # pushed_start, pushed_end 會是空字串或時間字串
            "pushed_start": r["pushed_start"],
            "pushed_end": r["pushed_end"],
            "link": r["link"]
        })
    return result


def update_push_status(key, which):  # which = "start", "end", "cancel"
    sheet = get_sheet("Events")
    records = sheet.get_all_values()

    if not records or len(records) < 1:
        print("Google Sheet 無資料")
        return

    headers = records[0]
    col_name_map = {
        "start": "pushed_start",
        "end": "pushed_end",
        "cancel": "pushed_cancel"  # 照你提供的拼字
    }

    if which not in col_name_map:
        raise ValueError("which 必須是 'start', 'end' 或 'cancel'")

    col_name = col_name_map[which]

    try:
        col_index = headers.index(col_name) + 1  # Google Sheets API 是從 1 開始
    except ValueError:
        raise ValueError(f"Google Sheet 找不到欄位名稱: {col_name}")

    for i, row in enumerate(records):
        if i == 0:
            continue  # 跳過標題列
        if row[0] == key:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.update_cell(i + 1, col_index, timestamp)
            print(f"已更新 {which} 推播時間：{timestamp}")
            break


