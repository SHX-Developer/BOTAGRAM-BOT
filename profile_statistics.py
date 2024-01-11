from aiogram import Bot, Dispatcher, types
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





#  SEND STATISTICS
async def statistics(call):

    main_sql.execute('SELECT * FROM user_statistics WHERE id = ?', (call.message.chat.id,))
    data = main_sql.fetchone()

    with open(f"photo/{call.message.chat.id}.jpg", "rb") as profile_photo:
        await bot.edit_message_media(
            media = types.InputMedia(  
            type = 'photo', 
            media = profile_photo, 
            caption =  
            f"📊 <b>Статистика</b> - <code>{data[1]}</code>"
            f"\n\n👀  <b>Посещений профиля:</b>  {data[6]}"
            f"\n\n👥  <b>Подписчики:</b>  {data[2]}"
            f"\n🫂  <b>Подписки:</b>  {data[3]}"
            f"\n\n❤️  <b>Лайки:</b>  {data[4]}"
            f"\n💔  <b>Дизлайки:</b>  {data[5]}",
            parse_mode = "html"), 
            chat_id = call.message.chat.id, 
            message_id = call.message.message_id, 
            reply_markup = inline_markups.statistics_inline)






#  FOLLOWERS
async def followers_statistics(call):

    followers_sql.execute(f'SELECT * FROM followers_{call.message.chat.id}')
    data = followers_sql.fetchall()

    number = 0
    message_text = "👥  <b>Пользователи которые на вас подписаны:</b>\n\n"
    
    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(call.message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

#  FOLLOWS
async def follows_statistics(call):

    follows_sql.execute(f'SELECT * FROM follows_{call.message.chat.id}')
    data = follows_sql.fetchall()

    number = 0
    message_text = "🫂  <b>Пользователи на которых вы подписаны:</b>\n\n"
    
    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(call.message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

#  LIKES
async def likes_statistics(call):

    likes_sql.execute(f'SELECT * FROM likes_{call.message.chat.id}')
    data = likes_sql.fetchall()

    number = 0
    message_text = "❤️  <b>Пользователи которые оценили ваш профиль:</b>\n\n"
    
    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(call.message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

#  DISLIKES
async def dislikes_statistics(call):

    dislikes_sql.execute(f'SELECT * FROM dislikes_{call.message.chat.id}')
    data = dislikes_sql.fetchall()
    
    number = 0
    message_text = "💔  <b>Пользователи которые ставили дизлайк на ваш профиль:</b>\n\n"
    
    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(call.message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

#  VIEWS
async def views_statistics(call):

    views_sql.execute(f'SELECT * FROM views_{call.message.chat.id}')
    data = views_sql.fetchall()

    number = 0
    message_text = "👀  <b>Пользователи которые посещали ваш профиль:</b>\n\n"
    
    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(call.message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)












