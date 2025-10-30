# TYCS Line Bot 自動推播服務

# tycs-line-bot-severless 

本專案為一個以 LINE Bot + Google Sheets 為後端的登山活動自動推播工具。每天自動爬取 TYCS 活動網 的活動資訊，並根據報名起始、截止與取消截止時間，自動推送提醒訊息給訂閱者。

## 功能介紹

✅ 自動爬取活動資訊並儲存到 Google Sheets
✅ 使用唯一 key 儲存事件資訊，避免重複寫入
✅ 根據活動時程自動推播 LINE 訊息
✅ 推播後紀錄時間戳，避免重複通知
✅ 支援 GitHub Actions 自動排程

## 專案架構

tycs-line-bot-severless/
├── crawler.py # 爬蟲程式
├── push.py # 推播邏輯
├── worker.py # 執行入口 (可指定 crawler 或 push)
├── google_sheet.py # Google Sheets API 封裝
├── requirements.txt # 相依套件
├── .github/workflows/ # GitHub Actions 設定
│ └── schedule.yml

## 使用方式

1. 環境設定

使用 .env 或 GitHub Secrets 設定下列參數：

LINE_CHANNEL_ACCESS_TOKEN=xxx
GOOGLE_SHEET_ID=xxx

2. 安裝套件

pip install -r requirements.txt

3. 手動執行

python worker.py crawler
python worker.py push

## 自動化排程 (GitHub Actions)

on:
workflow_dispatch:
schedule: - cron: '0 10 \* \* _' # 台灣時間 18:00 爬蟲 - cron: '0 11 _ \* \*' # 台灣時間 19:00 推播

GitHub Actions 使用 UTC 時區，請自行轉換時區。

📊 Google Sheet 欄位說明

欄位 說明

key 唯一欄位，名稱+date

title 活動名稱

start_date 出發日期

level 難度等級

reg_start 報名開始

reg_end 報名截止

cancel_end 取消截止

pushed_start 推播報名開始時間

pushed_end 推播報名截止時間

push_cancel 推播取消截止時間

## 📱 LINE Bot 功能

Push example 推送訊息範例：
📣 活動通知
活動：114102601 高雄藤枝山+...
出發日期：2025-10-26
報名起始：2025-06-23 20:00
🔗 https://www.tycs.com.tw/EventList/...

## To Do List📌 待辦項目

用戶活動等級選擇/ 星期選擇

## 👊 貢獻方式

Welcome fork 或開 issue 提供意見與修正！
