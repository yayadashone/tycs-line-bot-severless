# worker.py
from crawler import crawl_events
from push import push_today_events
from google_sheet import append_event_if_not_exists, get_sheet
import time
import sys

def run_crawler():
    print("CRAWLER start...")
    event_list = crawl_events()
    append_event_if_not_exists(event_list)
    print(f"CRAWLER completed.")

def run_push():
    print("PUSH start...")
    push_today_events()
    print("PUSH completed")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("crawler or push")
        sys.exit(1)

    task = sys.argv[1].lower()
    if task == "crawler":
        run_crawler()
    elif task == "push":
        run_push()
    else:
        print("未知的任務參數，請使用 crawler 或 push")
        sys.exit(1)
