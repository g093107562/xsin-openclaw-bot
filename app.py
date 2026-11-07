import os
import random
import requests
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from google import genai

app = Flask(__name__)

# --- 1. 環境變數設定 ---
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.environ.get('LINE_CHANNEL_SECRET')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
NGROK_URL = os.environ.get('NGROK_URL', 'https://xxxx-xxxx.ngrok-free.app/trigger-post')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 初始化新版 Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# --- 2. Webhook 接收點 ---
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# --- 3. 完整核心對話與指令邏輯 ---
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text.strip()
    
    # 🎯 指令 1：觸發本機電腦發文 (Threads) - 已強化 Header 避免 ngrok 攔截
    if user_msg in ["發文", "啟動發文", "龍蝦發文", "紅鑽發文"]:
        try:
            payload = {"key": "xsin_lobster_secret"}
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true",
                "User-Agent": "CustomBotAgent"
            }
            res = requests.post(NGROK_URL, json=payload, headers=headers, timeout=8)
            if res.status_code == 200:
                reply_text = "🦞 收到小姐姐指令！龍蝦已成功觸發本機電腦開始執行 Threads 自動發文囉！✨"
            else:
                reply_text = f"⚠️ 電腦回應異常：{res.text[:100]}"
        except Exception as e:
            reply_text = f"❌ 連線失敗：{str(e)}"
            
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    # 🎯 指令 2：威力彩 5 組隨機推薦
    if "威力彩" in user_msg or "威力" in user_msg:
        sets_text = ""
        for i in range(1, 6):
            sec1 = sorted(random.sample(range(1, 39), 6))
            sec2 = random.randint(1, 8)
            sets_text += f"第 {i} 組：第一區 {sec1} ｜ 第二區 [{sec2}]\n"
        
        reply_text = (
            "🤖【AI 威力彩 5 組精選推薦】\n"
            "───────────────────\n"
            f"{sets_text}\n"
            "💡 祝小姐姐期期中大獎、直接抱走億萬頭獎！💰"
        )
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    # 🎯 指令 3：大樂透 5 組隨機推薦
    if "大樂透" in user_msg or "大樂" in user_msg:
        sets_text = ""
        for i in range(1, 6):
            nums = sorted(random.sample(range(1, 50), 6))
            special = random.randint(1, 49)
            while special in nums:
                special = random.randint(1, 49)
            sets_text += f"第 {i} 組：{nums} ｜ 特別號 [{special}]\n"
        
        reply_text = (
            "🤖【AI 大樂透 5 組精選推薦】\n"
            "───────────────────\n"
            f"{sets_text}\n"
            "💡 祝小姐姐財源滾滾、把頭獎通通抱回家！💎💰"
        )
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))
        return

    # 🎯 指令 4：Gemini AI 對話 (100字以內限制)
    try:
        if not GEMINI_API_KEY or not client:
            reply_text = "⚠️ 錯誤：Heroku 上的 GEMINI_API_KEY 變數未設定！"
        else:
            prompt = (
                f"你是『宇宙金庫超級龍蝦』，是小姐姐最忠誠、聰明又可愛的 AI 助手。"
                f"講話風格要活潑、貼心、熱情，稱呼對方為『小姐姐』。"
                f"請控制在 100 字以內，精簡扼要又幽默地回應使用者以下這句話：\n{user_msg}"
            )
            response = client.models.generate_content(
               model='gemini-3.5-flash',
               contents=prompt
            )
            reply_text = response.text if hasattr(response, 'text') else str(response)
    except Exception as e:
        reply_text = f"⚠️ Gemini 錯誤詳情：{str(e)}"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
