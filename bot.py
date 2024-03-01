import os
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = os.environ.get('API_TOKEN')
TARIF_GV = os.environ.get('TARIF_GV')
TARIF_HV = os.environ.get('TARIF_HV')
TARIF_VV = os.environ.get('TARIF_VV')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    variable_one = State()
    variable_two = State()
    variable_three = State()
    variable_four = State()


# Start command handler
@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Send a message when the command /start is issued.
    """
    await message.reply("Привет! Введите показания электросчетчика:")

    # Set the variable_one state
    await Form.variable_one.set()


# Handle variable_one state
@dp.message_handler(state=Form.variable_one)
async def process_variable_one(message: types.Message, state: FSMContext):
    try:
        variable_one = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return

    # Save variable_one value and ask for variable_two
    await state.update_data(variable_one=variable_one)
    await message.reply("Введите показания счетчика горячей воды:")

    # Set the variable_two state
    await Form.variable_two.set()


# Handle variable_two state
@dp.message_handler(state=Form.variable_two)
async def process_variable_two(message: types.Message, state: FSMContext):
    try:
        variable_two = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return

    # Save variable_two value and ask for variable_three
    await state.update_data(variable_two=variable_two)
    await message.reply("Введите показания счетчика холодной воды:")

    # Set the variable_three state
    await Form.variable_three.set()


# Handle variable_three state
@dp.message_handler(state=Form.variable_three)
async def process_variable_three(message: types.Message, state: FSMContext):
    try:
        variable_three = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return

    # Save variable_three value and ask for variable_four
    await state.update_data(variable_three=variable_three)

   # calculate the sum
    data = await state.get_data()
    electro = data['variable_one']
    gv = data['variable_two']
    hv = data['variable_three']
    vv = round(data['variable_two'] + data['variable_three'])
    sgv = round(data['variable_two'] * float(TARIF_GV))
    shv = round(data['variable_three'] * float(TARIF_HV))
    svv = round(vv * float(TARIF_VV))
    sss = round(sgv + shv + svv)

    # Reset the state and output the result
    await state.finish()
    await message.reply(f"Привет!\nЗа электричество: {electro} руб.\
    \nВода:\nГорячая Вода {int(gv)} * {TARIF_GV} = {sgv} руб.\
    \nХолодная Вода {int(hv)} * {TARIF_HV} = {shv} руб.\
    \nВодоотведение {vv} * {TARIF_VV} = {svv} руб.\
    \nИтого за воду + домофон {sss} / 2 + 48 = {int(sss / 2 + 48)} руб.\
    \n{round((sss / 2) + 48)} / 2 + 27500 = {((sss / 2) / 2) + 27500} руб. Елене\
    \n{(sss / 2) / 2 + 48} + {electro} = {round((sss / 2 + 48) / 2 + electro)} руб. Григорию")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

