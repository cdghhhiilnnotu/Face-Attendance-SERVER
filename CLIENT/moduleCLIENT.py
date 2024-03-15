import requests
import json

BASE_DIR = "http://127.0.0.1:5000/"

try:
    data = requests.get(BASE_DIR).json()
    with open("api.json", "w", encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
except:
    print("FAIL TO GET API")