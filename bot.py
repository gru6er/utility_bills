import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher, types


from handlers.poly import poly_router
from handlers.kras import kras_router
from common.bot_cmds_list import kvart

logging.basicConfig(level=logging.INFO)

ALLOWED_UPDATES = ['message, edited_message']

# Инициализируем бота, диспечера и роутеров

async def main():
    bot = Bot(token=getenv('TOKEN'))

    dp = Dispatcher()

    dp.include_router(poly_router)
    dp.include_router(kras_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=kvart, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

if __name__ == "__main__":
    asyncio.run(main())

