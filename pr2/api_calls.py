import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

sys_prompt = """You are a digital companion for mental health support. You are here to listen, support, and help to understand user's thoughts and feelings.
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."""


async def gpt_query(prompt: str) -> str:
    """
    Функция для запроса к модели gpt-oss-20b

    :param str prompt: запрос пользователя
    :return str: ответ модели
    """

    payload = {
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
        "model": "openai/gpt-oss-20b:fireworks-ai",
    }

    response = await api_call(payload)
    return response["choices"][0]["message"]["content"] if response else "API error"


async def qwen_query(prompt: str) -> str:
    """
    Функция для запроса к модели Qwen3-32B

    :param str prompt: запрос пользователя
    :return str: ответ модели
    """

    payload = {
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt},
        ],
        "model": "Qwen/Qwen3-32B:nscale",
        "enable_thinking": False,
        "temperature": 0.7,
        "top_p": 0.8,
        "top_k": 20,
        "min_p": 0,
    }

    response = await api_call(payload)
    return response["choices"][0]["message"]["content"] if response else "API error"


async def api_call(payload: dict) -> dict:
    """
    Функция для асинхронного обращения к Hugging Face router

    :params dict payload: запрос пользователя
    :return dict: ответ API
    """

    api_url = os.getenv("API_URL")
    headers = {"Authorization": f"Bearer {os.getenv("HF_TOKEN")}"}

    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result
            else:
                error_text = await response.text()
                print(f"Error: {response.status} - {error_text}")
                return None
