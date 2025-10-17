import os
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)
import asyncio
from dotenv import load_dotenv
from api_calls import gpt_query, qwen_query
from logger import log_interaction


load_dotenv()

bot = AsyncTeleBot(os.getenv("BOT_TOKEN"))
user_models = {}
MAX_MESSAGE_LENGTH = 4000


def create_main_menu() -> ReplyKeyboardMarkup:
    """Функция для создания основного меню"""

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Перезапустить бота"))
    return keyboard


def create_model_menu() -> InlineKeyboardMarkup:
    """Функция для создания меню выбора модели"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("GPT", callback_data="model_gpt"),
        InlineKeyboardButton("Qwen", callback_data="model_qwen"),
    )
    return keyboard


@bot.message_handler(commands=["start"])
async def send_welcome(message: Message):
    """Обработчик команды /start"""

    welcome_text = """
Это цифровой компаньон для поддержки психического здоровья. 
Бот не заменяет профессиональную психологическую помощь. 
    """
    log_interaction(message.chat.id, "START_COMMAND")
    await bot.send_message(
        message.chat.id, welcome_text, reply_markup=create_main_menu()
    )
    await asyncio.sleep(0.2)
    await bot.send_message(
        message.chat.id, "Выберите модель:", reply_markup=create_model_menu()
    )


@bot.message_handler(commands=["help"])
async def send_help(message: Message):
    """Обработчик команды /help"""

    help_text = """
Команды:
/start - запустить бота
/help - показать эту справку
/restart - перезапустить бота

Кнопки меню:
Помощь - показать эту справку
Перезапустить бота - выбрать модель заново

Модели:
GPT - gpt-oss-20b
Qwen - Qwen3-32B

Как использовать:
1. Выберите модель
2. Напишите ваш запрос
3. Получите ответ от выбранной модели
    """
    log_interaction(message.chat.id, "HELP_COMMAND")
    await bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=["restart"])
async def restart_bot(message: Message):
    """Обработчик команды /restart"""

    user_id = message.chat.id
    if user_id in user_models:
        del user_models[user_id]

    log_interaction(user_id, "RESTART_COMMAND")
    await bot.send_message(
        user_id,
        "Бот перезапущен. Выберите модель:",
        reply_markup=create_model_menu(),
    )


@bot.message_handler(
    func=lambda message: message.text in ["Помощь", "Перезапустить бота"]
)
async def handle_main_menu(message: Message):
    """Обработчик нажатий на кнопки меню"""

    text = message.text
    log_interaction(message.chat.id, "MENU_BUTTON", text)
    if text == "Помощь":
        await send_help(message)
    else:
        await restart_bot(message)


@bot.callback_query_handler(func=lambda call: True)
async def handle_model_selection(call: CallbackQuery):
    """Обработчик выбора модели"""

    user_id = call.message.chat.id
    model_type = call.data

    if model_type == "model_gpt":
        user_models[user_id] = "gpt"
        model_name = "GPT"
    elif model_type == "model_qwen":
        user_models[user_id] = "qwen"
        model_name = "Qwen"

    log_interaction(user_id, "MODEL_SELECTED", f"model: {model_name}")
    await bot.answer_callback_query(call.id)
    await bot.send_message(user_id, f"Выбрана модель {model_name}.\nВедите запрос")


async def send_long_message(user_id: int, text: str, max_length=MAX_MESSAGE_LENGTH):
    """Функция для отправки длинного сообщения"""

    parts = []
    while text:
        if len(text) <= max_length:
            parts.append(text)
            break

        break_index = text.rfind("\n", 0, max_length - 1)
        if break_index == -1:
            break_index = text.rfind(" ", 0, max_length - 1)
        if break_index == -1:
            break_index = max_length - 1

        part = text[: break_index + 1].strip()
        parts.append(part)
        text = text[break_index + 1 :].strip()

    for i, part in enumerate(parts):
        await bot.send_message(user_id, part)
        if i < len(parts) - 1:
            await asyncio.sleep(0.4)


@bot.message_handler(func=lambda message: True)
async def handle_user_query(message: Message):
    """Обработчик текстовых сообщений (запросов пользователя)"""
    user_id = message.chat.id
    user_message = message.text
    log_message_preview = (
        user_message[:100] + "..." if len(user_message) > 100 else user_message
    )
    log_interaction(user_id, "USER_MESSAGE", f"text: {log_message_preview}")

    if user_id not in user_models:
        log_interaction(user_id, "MODEL_NOT_SELECTED")
        await bot.send_message(
            user_id, "Сначала выберите модель.", reply_markup=create_model_menu()
        )
    else:
        if user_models[user_id] == "gpt":
            response_text = await gpt_query(user_message)
        else:
            response_text = await qwen_query(user_message)

        log_response_preview = (
            response_text[:100] + "..." if len(response_text) > 100 else response_text
        )
        log_interaction(user_id, "BOT_RESPONSE", f"text: {log_response_preview}")
        if len(response_text) < MAX_MESSAGE_LENGTH:
            await bot.send_message(user_id, response_text)
        else:
            await send_long_message(user_id, response_text)


async def start_bot():
    print("Mental Health Companion Bot is running...")
    await bot.polling()
