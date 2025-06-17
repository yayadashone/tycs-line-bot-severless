# crawler.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_events():
    url = "https://www.tycs.com.tw/EventList"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    events = []
    for item in soup.select(".event-item"):  # 依真實class調整
        title = item.select_one(".title").text.strip()
        start_date = item.select_one(".start-date").text.strip()  # 活動出發日期
        reg_start = item.select_one(".reg-start").text.strip()   # 報名起始
        reg_end = item.select_one(".reg-end").text.strip()       # 報名截止
        # datetime物件轉換
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        reg_start_dt = datetime.strptime(reg_start, "%Y-%m-%d %H:%M")
        reg_end_dt = datetime.strptime(reg_end, "%Y-%m-%d %H:%M")
        events.append({
            "title": title,
            "start_date": start_date_dt,
            "reg_start": reg_start_dt,
            "reg_end": reg_end_dt,
        })
    return events

