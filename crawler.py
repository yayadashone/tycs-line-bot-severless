from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from google_sheet import append_event_if_not_exists, get_sheet

def crawl_events(pages=5):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.tycs.com.tw/EventList')
    time.sleep(3)

    event_list = []

    for page in range(1,pages+1):

        url = f'https://www.tycs.com.tw/EventList/{page}'
        print(f"抓取第 {page} 頁活動，網址：{url}")
        driver.get(url)
        time.sleep(3)

        # 取得所有活動 li 元素
        events = driver.find_elements(By.CSS_SELECTOR, 'ul.event-list li')

        for event in events:
            try:
                level = event.find_element(By.CLASS_NAME, 'level').text.strip()
                name = event.find_element(By.CLASS_NAME, 'event-name').text.strip()
                date_event = event.find_element(By.CLASS_NAME, 'date-event').text.strip()
                date_apply = event.find_element(By.CLASS_NAME, 'date-apply').text.strip().replace('\n', ' ')
                date_cancel = event.find_element(By.CLASS_NAME, 'date-cancel').text.strip()

                event_url = event.find_element(By.CSS_SELECTOR, '.event-info a').get_attribute('href')
                print(f"活動名稱: {name}, 活動日期: {date_event}, 報名日期: {date_apply}, 取消日期: {date_cancel}, 活動網址: {event_url}")



                event_data = {
                    "level": level,
                    "name": name,
                    "date_event": date_event,
                    "date_apply": date_apply,
                    "date_cancel": date_cancel,
                    "event_url": event_url

                }

                event_list.append(event_data)
               
            except Exception as e:
                print("錯誤:", e)
                continue

    driver.quit()

    # 返回抓取到的活動列表
    #print(f"共抓取到 {len(event_list)} 個活動")
    return event_list
    
