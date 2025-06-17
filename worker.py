# worker.py
from crawler import fetch_and_store_events
from push import push_today_events
import time
import sys

def run_crawler():
    print("CRAWLER start...")
    events = fetch_and_store_events()
    # 這裡可以加入存到 Google Sheet 或其他處理
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
