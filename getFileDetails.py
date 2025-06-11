import requests, time

TOKEN = "7963658960:AAHNEq9ijhTbsXto_wbMfasU7jmtxnHgmzg"
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
last_update_id = 0

while True:
    res = requests.get(url, params={"offset": last_update_id + 1})
    data = res.json()

    for result in data.get("result", []):
        last_update_id = result["update_id"]
        print(result)  # Check here for 'file_id' inside 'photo', 'document', etc.

    time.sleep(2)