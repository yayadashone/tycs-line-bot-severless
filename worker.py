# worker.py
from crawler import fetch_and_store_events
from push import push_today_events
import time

if __name__ == "__main__":
    fetch_and_store_events()
    push_today_events()
