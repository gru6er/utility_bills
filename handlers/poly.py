from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Router

poly_router = Router()

class Form(StatesGroup):
    variable_one = State()
    variable_two = State()
    variable_three = State()

@poly_router.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer("Привет, я виртуальный помощник в подсчете коммунальных платежей.\nПлатежи по какому адресу вас интересуют?")

@poly_router.message(or_f(Command("poly"), (F.text.lower().contains( "поликарп"))))
async def cmd_start(message: Message, state: FSMContext):
    
    await message.answer("Введите сумму за электроэнергию по адресу Поликарпова 9:")
    await state.set_state(Form.variable_one)

#Становимся в состояние ожидания ввода variable_one, и проверяем, что бы тип был флот.       
        
@poly_router.message(Form.variable_one)
async def process_variable_one(message: Message, state: FSMContext):
    await state.update_data(variable_one=message.text)

    try:
        variable_one = float(message.text)
    except ValueError:
        await message.answer("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return
    await message.answer("Сколько кубов горячей воды было израсходавано:")
    
    await state.set_state(Form.variable_two)

#Становимся в состояние ожидания ввода variable_two, и проверяем, что бы тип был флот.

@poly_router.message(Form.variable_two)
async def process_variable_two(message: Message, state: FSMContext):
    await state.update_data(variable_two=message.text)

    try:
        variable_two = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return
    await message.answer("Сколько кубов холодной воды было израсходавано:")
    
    await state.set_state(Form.variable_three)

#Становимся в состояние ожидания ввода variable_three, и проверяем, что бы тип был флот.


@poly_router.message(Form.variable_three)
async def process_variable_two(message: Message, state: FSMContext):
    await state.update_data(variable_three=message.text)

    try:
        variable_two = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return
    
# Делаем расчет, выводим ответ, и сбрасываем стейт.

    TARIF_GV=243.16
    TARIF_HV=50.93
    TARIF_VV=39.97
    TARIF_DF=48
    TARIF_APP=27500
    data = await state.get_data()
    electro = float(data['variable_one'])
    gv = float(data['variable_two'])
    hv = float(data['variable_three'])
    vv = round(gv + hv)
    sgv = round(gv * float(TARIF_GV))
    shv = round(hv * float(TARIF_HV))
    svv = round(vv * float(TARIF_VV))
    sss = round(sgv + shv + svv)

    await message.answer(f"Привет!\nЗа электричество: {electro} руб.\
    \nВода:\nГорячая Вода {int(gv)} * {TARIF_GV} = {sgv} руб.\
    \nХолодная Вода {int(hv)} * {TARIF_HV} = {shv} руб.\
    \nВодоотведение {vv} * {TARIF_VV} = {svv} руб.\
    \nИтого за воду + домофон {sss} / 2 + 48 = {int(sss / 2 + 48)} руб.\
    \n({round((sss / 2) + TARIF_DF)} / 2) + {TARIF_APP} = {round((sss / 2 + TARIF_DF) / 2) + TARIF_APP} руб. Елене\
    \n{round((sss / 2) / 2 + TARIF_DF)} + {electro} + {TARIF_APP} = {round((sss / 2 + TARIF_DF) / 2 + electro + TARIF_APP)} руб. Мне")

    await state.clear()