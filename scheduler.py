from datetime import date
from crawler import fetch_events
from push import send_push

def main():
    today = date.today()
    events = fetch_events()
    messages = []
    for event in events:
        if today == event["start"]:
            messages.append(f"今天開始報名：{event['title']}")
        elif today == event["end"]:
            messages.append(f"今天是報名截止：{event['title']}")
    if messages:
        user_ids = []  # TODO: 讀取 Google Sheet 或資料庫
        full_message = "\n".join(messages)
        send_push(user_ids, full_message)

if __name__ == "__main__":
    main()
