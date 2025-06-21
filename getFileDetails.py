import requests, time

TOKEN = "bot token here"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
last_update_id = 0

while True:
    res = requests.get(url, params={"offset": last_update_id + 1})
    data = res.json()

    for result in data.get("result", []):
        last_update_id = result["update_id"]
        print(result)  # Check here for 'file_id' inside 'photo', 'document', etc.

    time.sleep(2)
