import os
import requests
from dotenv import load_dotenv

# Загрузка переменных среды
load_dotenv()


def api_ninjas(text_1: str, text_2: str) -> float:
    """
    Функция обращения к api сервису api-ninjas

    params: text_1 и text2 - сравниваемые тексты
    return: вещественное число - схожесть текстов
    """

    body = {"text_1": text_1, "text_2": text_2}
    api_url = os.getenv("API1_URL")
    api_key = os.getenv("API1_KEY")

    response = requests.post(api_url, headers={"X-Api-Key": api_key}, json=body)

    if response.status_code == requests.codes.ok:
        return round(response.json()["similarity"], 6)
    else:
        print("Error:", response.status_code, response.text)
        return -1
