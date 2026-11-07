import os
import google.generativeai as genai

# 請把下面的 '您的API金鑰' 換成您實際用的 GEMINI_API_KEY，或直接設定好環境變數
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

print("正在檢查 API Key 與可用模型...")

try:
    # 測試列出模型，順便驗證 Key 是否有效
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"支援的模型: {m.name}")

    # 測試用 gemini-3.8-flash 發送一個簡單的訊息
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("嗨，請回覆『測試成功』")
    print("\n------------------")
    print(f"🎉 測試結果成功！AI 回應：{response.text}")
    print("------------------")

except Exception as e:
    print("\n------------------")
    print(f"❌ API 測試失敗，錯誤原因：{str(e)}")
    print("------------------")
