from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import F, Router

kras_router = Router()

class Form_kras(StatesGroup):
    variable_one = State()
    variable_two = State()


 

@kras_router.message(or_f(Command("kras"), (F.text.lower().contains( "красного"))))
async def cmd_start(message: Message, state: FSMContext):
    
    await message.answer("Введите сумму квартплаты по адресу Красногорское шоссе 8:")
    await state.set_state(Form_kras.variable_one)

#Становимся в состояние ожидания ввода variable_one, и проверяем, что бы тип был флот.       
        
@kras_router.message(Form_kras.variable_one)
async def process_variable_one(message: Message, state: FSMContext):
    await state.update_data(variable_one=message.text)

    try:
        variable_one = float(message.text)
    except ValueError:
        await message.answer("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return
    await message.answer("Введите сумму в ЕПД:")
    
    await state.set_state(Form_kras.variable_two)

#Становимся в состояние ожидания ввода variable_two, и проверяем, что бы тип был флот.

@kras_router.message(Form_kras.variable_two)
async def process_variable_two(message: Message, state: FSMContext):
    await state.update_data(variable_two=message.text)

    try:
        variable_two = float(message.text)
    except ValueError:
        await message.reply("Похоже, вы ввели неверное значение. Пожалуйста, попробуйте еще раз.")
        return
    
# Делаем расчет, выводим ответ, и сбрасываем стейт.
    TARIF_APK = 55000
    data = await state.get_data()
    kvartplata = float(data['variable_one'])
    epd = float(data['variable_two'])
    kp = float(kvartplata + epd)
    su = float(TARIF_APK - kp)
    
    await message.answer(f'Квартплата:                 {kvartplata} + {epd} = {kp} \nДоход - квартплата:        {TARIF_APK} - {kp} = {round(su)} \nОстаток делится на троих:   {round(su)} / 3 = {round(su / 3)}')

    await state.clear()
