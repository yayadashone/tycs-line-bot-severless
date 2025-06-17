import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_events():
    url = "https://www.tycs.com.tw/EventList"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    events = []
    for item in soup.select(".event-item"):
        title = item.select_one(".title").text.strip()
        start_date = item.select_one(".start-date").text.strip()
        end_date = item.select_one(".end-date").text.strip()
        events.append({
            "title": title,
            "start": datetime.strptime(start_date, "%Y-%m-%d").date(),
            "end": datetime.strptime(end_date, "%Y-%m-%d").date(),
        })
    return events
