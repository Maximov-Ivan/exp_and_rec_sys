import asyncio
from tg_bot import start_bot
from logger import setup_logging


if __name__ == "__main__":
    setup_logging()
    asyncio.run(start_bot())
