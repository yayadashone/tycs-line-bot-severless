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
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="您好，您已經成功加入桃園市晟崧休閒登山會活動通知機器人！敬請期待 ☺️")
    )

# 接收加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    add_user_if_not_exists(user_id)
    line_bot_api.push_message(
        user_id,
        TextSendMessage(text="👋 歡迎加入桃園市晟崧休閒登山會活動推播服務！\n我們會在活動報名前一小時提醒您。")
    )

# 本地測試入口
if __name__ == "__main__":
    app.run(debug=True)
