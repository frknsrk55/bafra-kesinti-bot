import requests
import time

TOKEN = "8754447980:AAHBCzZca9l6FQCu-lKO0Pa-HnT6tCoCkFI"
CHAT_ID = "7935307223"

LAST_UPDATE_ID = None


def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


def check_yedek_saski():
    results = []

    try:
        yedas = requests.get("https://www.yedas.com/planli-kesinti", timeout=10).text.lower()
        saski = requests.get("https://www.saski.gov.tr/sukesintileri/index.aspx", timeout=10).text.lower()

        if "altinyaprak" in yedas:
            results.append("⚡ YEDAŞ: ALTINYAPRAK bölgesinde elektrik kesintisi var/olabilir.")

        if "altinyaprak" in saski:
            results.append("💧 SASKİ: ALTINYAPRAK bölgesinde su kesintisi var/olabilir.")

        if not results:
            return "✅ ALTINYAPRAK için şu an planlı kesinti görünmüyor."

        return "\n".join(results)

    except Exception as e:
        return f"⚠️ Veri çekme hatası: {e}"


def get_updates():
    global LAST_UPDATE_ID

    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 10}

    if LAST_UPDATE_ID:
        params["offset"] = LAST_UPDATE_ID + 1

    r = requests.get(url, params=params).json()

    for update in r.get("result", []):
        LAST_UPDATE_ID = update["update_id"]

        message = update.get("message", {})
        text = message.get("text", "")

        if text == "/sorgu":
            result = check_yedek_saski()
            send_message(result)


print("Bot çalışıyor...")

while True:
    get_updates()
    time.sleep(2)
