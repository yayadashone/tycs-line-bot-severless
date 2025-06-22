import os
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent

from google_sheet import add_user_if_not_exists
import logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# 初始化 LINE Bot API 與 Webhook Handler
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/", methods=["GET"])
def home():
    print("Health check passed.")
    return "OK", 200

# 設定 Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    logging.info(f"Received body: {body}") 

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 接收訊息事件
#@handler.add(MessageEvent, message=TextMessage)
#def handle_message(event):
#    line_bot_api.reply_message(
#       event.reply_token,
#        TextSendMessage(text="您好，感謝您的訊息！\n\n很抱歉，本帳號無法個別回覆用戶的訊息。\n"
#                        "敬請期待我們下次發送的內容喔!\n"
#                        "此line服務由晟崧山友自行創立善意自動推播活動通知，並非官方服務且無營利服務。\n"
#                        "如推播活動資訊有任何問題，僅以桃園市晟崧休閒登山會網站內容為主\n")
#    )

#接收加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    logging.info(f"New follower: {event.source.user_id}")
    # 當用戶加入好友時，將其加入 Google Sheet
    user_id = event.source.user_id
    add_user_if_not_exists(user_id)

# 本地測試入口
if __name__ == "__main__":
    app.run(debug=True)
