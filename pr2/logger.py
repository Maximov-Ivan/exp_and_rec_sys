import logging
from datetime import datetime
import os


def setup_logging():
    """Функция настройки логирования"""

    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_format = "%(asctime)s - %(levelname)s - %(message)s"

    file_handler = logging.FileHandler(
        f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log', encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])


def log_interaction(user_id: int, action: str, details=""):
    """Функция для логирования взаимодействий"""

    log_message = f"USER: user_{user_id} - ACTION: {action}"
    if details:
        log_message += f" - DETAILS: {details}"
    logging.info(log_message)
