# push.py
from datetime import datetime, timedelta
from google_sheet import get_all_events, update_push_status, get_sheet, get_all_user_ids 
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

def get_line_bot_api():
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    print(f"✅ Token loaded, length: {len(token)}") 
    if not token:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")
    return LineBotApi(token)



def push_today_events():
    line_bot_api = get_line_bot_api()
    today = datetime.now().date()
    events = get_all_events()
    tycs_url = "https://www.tycs.com.tw"
    for row in events:
        title = row["title"]
        key = row["key"]
        event_url = tycs_url+row["event_url"]

        #str to datetime
        start_date = datetime.strptime(row["start_date"], "%Y/%m/%d").date()
        cancel_end = datetime.strptime(row["cancel_end"], "%Y-%m-%d").date() if row["cancel_end"] else None
        reg_start = datetime.strptime(row["reg_start"], "%Y-%m-%d").date() if row["reg_start"] else None
        reg_end = datetime.strptime(row["reg_end"], "%Y-%m-%d").date() if row["reg_end"] else None
        push_start = row["pushed_start"]
        push_end = row["pushed_end"]

        # 推播：報名起始前 1 小時
        if reg_start == today and not push_start:
            message = (f"📣 今晚報名活動通知\n"
                        f"活動：{title}\n"
                        f"出發日期：{start_date}\n"
                        f"報名起始：{reg_start.strftime('%Y-%m-%d 20:00')}\n"
                        f"👉 活動連結：{event_url}")
            send_to_all_users(message)
            update_push_status(key, 'start')

        # 推播：報名截止前 1 小時 
        # 2025/7/20後 暫停發送此訊息, 免費額度已滿
        if reg_end == today and not push_end:
            message = (f"⏰ 今晚報名截止提醒\n"
                       f"活動：{title}\n"
                       f"出發日期：{start_date}\n"
                       f"報名截止：{reg_end.strftime('%Y-%m-%d 20:00')}\n"
                       f"👉 活動連結：{event_url}")
            #send_to_all_users(message)
            update_push_status(key, 'end')

        # 推播：取消截止前 1 小時
        if not row.get("push_cancel") and cancel_end == today:
            message = (f"🚨 今晚取消報名截止提醒\n"
                       f"活動：{title}\n"
                       f"出發日期：{start_date}\n"
                       f"取消截止：{cancel_end.strftime('%Y-%m-%d 20:00')}\n"
                       f"👉 活動連結：{event_url}")
            send_to_all_users(message)
            update_push_status(key, 'cancel')

def send_to_all_users(message):
    from google_sheet import get_all_user_ids
    line_bot_api = get_line_bot_api()
    user_ids = get_all_user_ids()
    print(f"共 {len(user_ids)} 位使用者將收到訊息")
    for uid in user_ids:
        try:
            print(f"發送給 {uid} 的訊息：{message}")
            line_bot_api.push_message(uid, TextSendMessage(text=message))
        except Exception as e:
            print(f"發送給 {uid} 失敗：{e}")