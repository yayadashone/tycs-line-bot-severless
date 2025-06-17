import schedule
import time
from crawler import fetch_events
from push import send_push
from datetime import datetime

def notify():
    now = datetime.now()
    events = fetch_events()
    messages = []
    for event in events:
        if event["reg_start"].date() == now.date() and event["reg_start"].hour == 20:
            messages.append(f"活動：{event['title']}\\n出發日：{event['start_date'].strftime('%Y-%m-%d')}\\n報名開始：{event['reg_start'].strftime('%H:%M')}")
        if event["reg_end"].date() == now.date() and event["reg_end"].hour == 20:
            messages.append(f"活動：{event['title']}\\n出發日：{event['start_date'].strftime('%Y-%m-%d')}\\n報名截止：{event['reg_end'].strftime('%H:%M')}")

    if messages:
        send_push("\\n\\n".join(messages))

schedule.every().day.at("19:00").do(fetch_events)
schedule.every().day.at("19:30").do(notify)

while True:
    schedule.run_pending()
    time.sleep(30)
