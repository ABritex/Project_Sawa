import json
import httpx
from utils.api_loader import DEEPLX_API_URL

def translate_text(text, source_lang="EN", target_lang="JA"):
    data = {
        "text": [text],
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    post_data = json.dumps(data)
    headers = {"Content-Type": "application/json"}
    response = httpx.post(url=DEEPLX_API_URL, data=post_data, headers=headers)
    if response.status_code == 200:
        translated_text = response.json()["translations"][0]["text"]
        return translated_text
    else:
        response.raise_for_status()
