import requests

TELEGRAM_BOT_TOKEN = "7081128195:AAHqLP88FQr_RheuaMnJVzfi8i6rm_XDvNc" 
TELEGRAM_CHAT_ID = "6780115616"

def test_alert():
    print(f"Testing Telegram Alert...")
    print(f"Token: {TELEGRAM_BOT_TOKEN}")
    print(f"Chat ID: {TELEGRAM_CHAT_ID}")

    message = "🔔 This is a TEST message from SentinAI."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    try:
        print("Sending request...")
        response = requests.post(url, data=data, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_alert()
