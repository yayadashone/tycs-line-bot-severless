from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.tycs.com.tw/EventList')
time.sleep(3)

event_list = []
# 取得所有活動 li 元素
events = driver.find_elements(By.CSS_SELECTOR, 'ul.event-list li')
print(driver.title)

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

# 關閉瀏覽器
driver.quit()

# 印出結果（可省略）
for e in event_list:
    print(e)
