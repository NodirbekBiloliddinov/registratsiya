from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import ReplyKeyboardRemove

from keyboards.default.keyboard import menu
from loader import dp
from states.personalData import PersonalData

from aiogram.dispatcher.filters.builtin import CommandStart

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!")
    await message.answer('To`liq ismingizni kiriting:')
    await PersonalData.fullname.set()

@dp.message_handler(state=PersonalData.fullname)
async def answer_fullname(message: types.Message, state: FSMContext):
    fullname = message.text
    await state.update_data(
        {'name': fullname}
    )

    await message.answer('Sertifikatingizni kiriting:')
    await PersonalData.next()

@dp.message_handler(state=PersonalData.sertificate)
async def answer_sertificate(message: types.Message, state: FSMContext):
    sertificate = message.text
    await state.update_data(
        {'sertificate': sertificate}
    )

    await message.answer('O`qimoqchi bo`lgan davlatingizni kiriting:')
    await PersonalData.next()

@dp.message_handler(state=PersonalData.country)
async def answer_country(message: types.Message, state: FSMContext):
    country = message.text
    await state.update_data(
        {'country': country}
    )

    await message.answer('Telefon raqamingizni kiriting:')
    await PersonalData.next()

@dp.message_handler(state=PersonalData.phone)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(
        {'phone': phone}
    )

    data = await state.get_data()
    name = data.get('name')
    sertificate = data.get('sertificate')
    country = data.get('country')
    phone = data.get('phone')

    msg = "Quyidagi ma'lumotlar qabul qilindi:\n"
    msg += f"👨‍💼 Ism va Familiya: - {name}\n"
    msg += f"📚 Sertifikat - {sertificate}\n"
    msg += f"🇺🇿 O'qimoqchi bo'lgan davlatingiz - {country}\n"
    msg += f"📞 Telefon raqamingiz - {phone}"
    await message.answer(msg, reply_markup=menu)
    await message.answer('Ma`lumotlarni tasdiqlang 👇')

    await state.finish()

@dp.message_handler(text='Tasdiqlash')
async def save_data(message: types.Message):
    await message.answer('Ma`lumotlaringiz qabul qilindi. Tez orada siz bilan bog`lanamiz.', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(text='Qaytadan kiritish')
async def retry_data(message: types.Message):
    await message.answer('To`liq ismingizni kiriting:', reply_markup=ReplyKeyboardRemove())
    await PersonalData.fullname.set()