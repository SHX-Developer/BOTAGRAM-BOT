from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import datetime

import config
import inline_markups
import reply_markups



#  LIBRARY VARIABLES  #

main_db = sqlite3.connect("database/user_data.db", check_same_thread=False)
followers_db = sqlite3.connect("database/followers.db", check_same_thread=False)
follows_db = sqlite3.connect("database/follows.db", check_same_thread=False)
likes_db = sqlite3.connect("database/likes.db", check_same_thread=False)
dislikes_db = sqlite3.connect("database/dislikes.db", check_same_thread=False)
views_db = sqlite3.connect("database/views.db", check_same_thread=False)

main_sql = main_db.cursor()
followers_sql = followers_db.cursor()
follows_sql = follows_db.cursor()
likes_sql = likes_db.cursor()
dislikes_sql = dislikes_db.cursor()
views_sql = views_db.cursor()

bot = Bot(config.token)
dp = Dispatcher(bot)

date_time = datetime.datetime.now().date()





#  DISPLAY SETTINGS
async def settings(message):

    main_sql.execute(f'SELECT * FROM user_settings WHERE id = ?', (message.chat.id,))
    data = main_sql.fetchone()

    if data[6] == "Включена":
        await bot.send_message(
            chat_id = message.chat.id,   
            text = 
            f"<b>⚙️  Ваши настройки поиска:</b>"
            f"\n\n<b>👫  Пол:</b>    {data[2]}"
            f"\n\n<b>🏙️  Город:</b>    {data[4]}",
            parse_mode="html", reply_markup=inline_markups.settings_inline_2)
    
    elif data[6] == "Отключена":
        await bot.send_message(
            chat_id = message.chat.id, 
            text = 
            f"<b>⚙️  Ваши настройки поиска:</b>"
            f"\n\n<b>👫  Пол:</b>    {data[2]}"
            f"\n\n<b>🏙️  Город:</b>    {data[4]}"
            f"\n\n<b>☑️  Верификация:</b>    {data[6]}",
            parse_mode="html", reply_markup=inline_markups.settings_inline_1)





