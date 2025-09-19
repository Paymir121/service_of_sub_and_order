import asyncio
import logging
import os
import time
from time import sleep

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties

from db import Connection
from api import automapped


load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logging.info(f"BOT.1:  start")
BOT_TOKEN = os.getenv("telegram_token", "")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
conn = Connection()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    logging.info(f"BOT.2: cmd_start")
    await message.answer("Привет! Я бот. Скинь свой номерок")

@dp.message()
async def echo(message: types.Message):
    logging.info(f"BOT.3: echo")
    telegram_id = message.from_user.id
    phone = message.text.strip()
    user = await search_user(phone=phone)
    logging.info(f"BOT.5: phone={phone}")
    logging.info(f"BOT.6: user={user}")
    if user:
        await update_user(user=user, telegram_id=telegram_id)
        logging.info(f"user={user}")
        await message.answer(f"BOT.7: Ты в Базе, за тобой уже следит Товарищ Майор")


async def search_user(phone: str):
    logging.info(f"7: search_user")
    try:
        user = conn.session.query(automapped.classes['users_customuser']).filter_by(phone=phone).first()
        return user
    except Exception as e:
        conn.session.rollback()

async def update_user(user, telegram_id: int):
    logging.info(f"BOT.8: update_use")
    logging.info(f"BOT.9: user={user}")
    try:
        user.telegram_id = telegram_id
        conn.session.commit()
    except Exception as e:
        logging.error(f"BOT.9/1: Ошибка при Обновлении ТГ-ид: {e}")
        conn.session.rollback()
    finally:
        return user

async def send_notification(telegram_id: int, message: str):
    try:
        await bot.send_message(telegram_id, message)
        logging.info(f"BOT.10: Уведомление отправлено пользователю {telegram_id}")
    except Exception as e:
        logging.error(f"BOT.11: Ошибка при отправке уведомления: {e}")

async def notify_new_order(order_id: int):
    """Отправка уведомления о новом заказе"""
    logging.info(f"BOT.12: order_id={order_id}")
    try:
        order = conn.session.query(automapped.classes['products_order']).filter_by(id=order_id).first()
        user = conn.session.query(automapped.classes['users_customuser']).filter_by(id=order.customer_id).first()

        message = f"Вам пришёл новый заказ! user.id={user.id}, order = {order.id}"
        logging.error(f"BOT.13: message  = {message}")
        if user and user.telegram_id:
            await send_notification(user.telegram_id, message)
            return True
        return False
    except Exception as e:
        logging.error(f"BOT.14: Ошибка при отправке уведомления о заказе: {e}")
        return False
    finally:
        conn.session.close()

async def bot_main():
    try:
        logging.info("BOT.15: Бот запускается...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"BOT.16: Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        logging.info("BOT.17: Бот остановлен")