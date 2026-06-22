import requests
import datetime
import threading

# Configuration - REPLACE THESE WITH YOUR REAL CREDENTIALS
# For now, we will use placeholders or you can set them via environment variables
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN_HERE" 
TELEGRAM_CHAT_ID = "TELEGRAM_BOT_CHAT_ID HERE"

def send_telegram_alert_async(payload, attacker_ip):
    """
    Actual blocking function to send the alert, run in a separate thread.
    """
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[WARNING] Telegram Bot Token not set. Alert not sent to Telegram.")
        print(f"[SIMULATION] ALERT TRIGGERED! IP: {attacker_ip}, Payload: {payload}")
        return

    message = (
        f"🚨 <b>SENTINAI ALERT</b> 🚨\n\n"
        f"<b>Time:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"<b>Attacker IP:</b> {attacker_ip}\n"
        f"<b>Malicious Payload:</b> <code>{payload}</code>\n"
        f"<b>Action:</b> BLOCKED ⛔"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        # Added timeout of 5 seconds
        response = requests.post(url, data=data, timeout=5)
        if response.status_code == 200:
            print("[INFO] Telegram alert sent successfully.")
        else:
            print(f"[ERROR] Failed to send Telegram alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception sending Telegram alert: {e}")

def send_telegram_alert(payload, attacker_ip):
    """
    Wrapper to run the alert in a background thread so it doesn't block the request.
    """
    thread = threading.Thread(target=send_telegram_alert_async, args=(payload, attacker_ip))
    thread.daemon = True # Daemon thread continues to run without blocking program exit
    thread.start()
