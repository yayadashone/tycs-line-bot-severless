# push.py
from datetime import datetime, timedelta
from google_sheet import get_all_events, update_push_status
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

#line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))


def get_line_bot_api():
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if not token:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set")
    return LineBotApi(token)

def push_today_events():
    line_bot_api = get_line_bot_api()
    today = datetime.now().date()
    now = datetime.now()
    events = get_all_events()
    
    for row in events:
        title = row["title"]
        start_date = datetime.strptime(row["start_date"], "%Y-%m-%d").date()
        reg_start = datetime.strptime(row["reg_start"], "%Y-%m-%d %H:%M")
        reg_end = datetime.strptime(row["reg_end"], "%Y-%m-%d %H:%M")
        push_start = row["pushed_start"]
        push_end = row["pushed_end"]

        # 推播：報名起始前 1 小時
        if reg_start.date() == today and not push_start:
            if now >= reg_start - timedelta(hours=1):
                message = f"📣 活動通知\n活動：{title}\n出發日期：{start_date}\n報名起始：{reg_start.strftime('%Y-%m-%d %H:%M')}"
                send_to_all_users(message)
                update_push_status(title, 'start')

        # 推播：報名截止前 1 小時
        if reg_end.date() == today and not push_end:
            if now >= reg_end - timedelta(hours=1):
                message = f"⏰ 報名截止提醒\n活動：{title}\n出發日期：{start_date}\n報名截止：{reg_end.strftime('%Y-%m-%d %H:%M')}"
                send_to_all_users(message)
                update_push_status(title, 'end')

def send_to_all_users(message):
    from google_sheet import get_all_users
    user_ids = get_all_users()
    for uid in user_ids:
        try:
            line_bot_api.push_message(uid, TextSendMessage(text=message))
        except Exception as e:
            print(f"發送給 {uid} 失敗：{e}")
