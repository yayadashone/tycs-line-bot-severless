from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.tycs.com.tw/EventList')
time.sleep(3)

event_list = []
for page in range(3):  # 抓前三頁
    print(f"抓取第 {page + 1} 頁")
    
    events = driver.find_elements(By.CSS_SELECTOR, 'ul.event-list li')

    for event in events:
        try:
            level = event.find_element(By.CLASS_NAME, 'level').text.strip()
            name = event.find_element(By.CLASS_NAME, 'event-name').text.strip()
            date_event = event.find_element(By.CLASS_NAME, 'date-event').text.strip()
            date_apply = event.find_element(By.CLASS_NAME, 'date-apply').text.strip().replace('\n', ' ')
            date_cancel = event.find_element(By.CLASS_NAME, 'date-cancel').text.strip()

            event_data = {
                "level": level,
                "name": name,
                "date_event": date_event,
                "date_apply": date_apply,
                "date_cancel": date_cancel
            }

            event_list.append(event_data)
        except Exception as e:
            print("錯誤:", e)
            continue
    
    # 如果不是最後一頁，點下一頁
    if page < 2:
        try:
            next_button = driver.find_element(By.LINK_TEXT, '下一頁')
            next_button.click()
            time.sleep(3)  # 等待頁面載入
        except NoSuchElementException:
            print("找不到下一頁按鈕，結束抓取。")
            break

driver.quit()

for e in event_list:
    print(e)