import requests

TOKEN = "BOT_TOKEN"
CHAT_ID = "CHAT_ID"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def check_kesinti():
    url = "https://www.yedas.com.tr"  # sonra detaylandıracağız
    r = requests.get(url)

    if "kesinti" in r.text.lower():
        send_message("⚠️ Bafra'da planlı kesinti olabilir. Kontrol et!")

check_kesinti()
