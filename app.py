import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)
config = Configuration(access_token=os.environ["LINE_TOKEN"])
handler = WebhookHandler(os.environ["LINE_SECRET"])


@app.route("/", methods=["GET"])
def home():
    return "Bot LINE dang chay!"


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text(event):
    text = event.message.text.strip()

    # ---- Sua cau tra loi o day ----
    if text.lower() in ("hi", "hello", "xin chao", "xin chào", "chào"):
        reply = "Xin chào! Mình có thể giúp gì cho bạn?"
    else:
        reply = f"Bạn vừa nói: {text}"
    # --------------------------------

    with ApiClient(config) as client:
        MessagingApi(client).reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)],
            )
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
