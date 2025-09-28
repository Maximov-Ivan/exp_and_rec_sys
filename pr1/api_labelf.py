import requests
import urllib3
import os
from dotenv import load_dotenv

# Загрузка переменных среды и отключение предупреждений InsecureRequestWarning
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def api_labelf(text_1: str, text_2: str) -> float:
    """
    Функция обращения к api сервису labelf

    params: text_1 и text2 - сравниваемые тексты
    return: вещественное число - схожесть текстов
    """

    data = {"grant_type": "client_credentials"}
    api_token_url = os.getenv("API2_TOKEN_URL")
    client_id = os.getenv("API2_CLIENT_ID")
    client_secret = os.getenv("API2_CLIENT_SECRET")

    response = requests.post(
        api_token_url, data=data, verify=False, auth=(client_id, client_secret)
    )

    if response.status_code == requests.codes.ok:
        api_token = response.json()["access_token"]
    else:
        print("Error:", response.status_code, response.text)
        return -1

    body = {
        "top_n": 1,
        "base_texts": {"text_1": text_1},
        "compare_to_texts": {"text_2": text_2},
    }
    api_url = os.getenv("API2_URL")

    response = requests.post(
        api_url, headers={"Authorization": f"Bearer {api_token}"}, json=body
    )

    if response.status_code == requests.codes.ok:
        return round(response.json()["text_2"][0]["similarity"], 6)
    else:
        print("Error:", response.status_code, response.text)
        return -1
