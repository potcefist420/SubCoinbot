from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from loader import dp, bot
from filters import IsPrivate, IsBan, IsUsr
from utils.messages import info, statistikamsg
from utils.sqlite import statistika
from data.config import admin, pays  # админ и выплаты

# ----------------------------------------
# Кастомное меню
# ----------------------------------------
class InfoMenuCustom:
    def info_main(self):
        keyboard = types.InlineKeyboardMarkup()
        
        # Статистика
        keyboard.add(types.InlineKeyboardButton(text='📊 Статистика', callback_data='statistika'))
        
        # Канал и выплаты
        keyboard.add(
            types.InlineKeyboardButton(text='🗞 Канал', url='https://t.me/subcoinnnews'),
            types.InlineKeyboardButton(text='💸 Выплаты', url=f'https://t.me/{pays}')
        )

        # Админ
        keyboard.add(
            types.InlineKeyboardButton(text='👤 Админ', url=f'https://t.me/{admin}')
        )

        return keyboard

# ----------------------------------------
# Обработчик нажатия на "💬 Информация"
# ----------------------------------------
@dp.message_handler(IsPrivate(), IsBan(), IsUsr(), is_forwarded=False, text="💬 Информация", state="*")
async def information_menu(m: types.Message, state: FSMContext):
    # Удаляем старое сообщение с dat-меню
    await m.delete()

    # Отправляем своё кастомное меню
    await bot.send_message(
        m.chat.id,
        info,
        parse_mode='html',
        reply_markup=InfoMenuCustom().info_main()
    )

# ----------------------------------------
# Callback для кнопки "📊 Статистика"
# ----------------------------------------
@dp.callback_query_handler(IsBan(), IsUsr(), text='statistika')
async def statistika_msg(c: CallbackQuery):
    val = await statistika()
    await c.message.edit_text(statistikamsg(val), parse_mode='html')
