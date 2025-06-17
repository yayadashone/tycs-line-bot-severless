# crawler.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from google_sheet import append_event_if_not_exists

def fetch_events():
    url = "https://www.tycs.com.tw/EventList"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    events = []
    for item in soup.select(".event-item"):  # 根據實際 class 調整
        try:
            title = item.select_one(".title").text.strip()
            start_date = item.select_one(".start-date").text.strip()
            reg_start = item.select_one(".reg-start").text.strip()
            reg_end = item.select_one(".reg-end").text.strip()

            # 日期格式轉換
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
            if start_date_dt < datetime.now():
                continue  # 跳過已過期活動

            reg_start_dt = datetime.strptime(reg_start, "%Y-%m-%d %H:%M")
            reg_end_dt = datetime.strptime(reg_end, "%Y-%m-%d %H:%M")

            append_event_if_not_exists({
                "title": title,
                "start_date": start_date_dt.strftime("%Y-%m-%d"),
                "reg_start": reg_start_dt.strftime("%Y-%m-%d %H:%M"),
                "reg_end": reg_end_dt.strftime("%Y-%m-%d %H:%M"),
            })
        except Exception as e:
            print(f"跳過錯誤項目: {e}")
