from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import datetime

import config
import inline_markups
import reply_markups


#  LIBRARY VARIABLES

main_db = sqlite3.connect("database/user_data.db", check_same_thread = False)
chat_db = sqlite3.connect("database/chat.db", check_same_thread = False)

main_sql = main_db.cursor()
chat_sql = chat_db.cursor()

bot = Bot(config.token)
dp = Dispatcher(bot)

date_time = datetime.datetime.now().date()




#  ADD QUEUE
async def add_queue(call):

    user_id = main_sql.execute('SELECT id FROM user_access WHERE id = ?', (call.message.chat.id,)).fetchone()[0]
    id_1 = chat_sql.execute('SELECT id FROM queue').fetchone()[0]

    if id_1 == "-":

        chat_sql.execute('UPDATE queue SET id = ?', (user_id,))
        chat_db.commit()

        await bot.send_message(user_id, "<b> 🔍  Ищем собеседника . . . </b>", parse_mode = "html", reply_markup = reply_markups.cancel_queue_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    
    else:
        
        chat_sql.execute('UPDATE queue SET id = ?', ("-",))
        chat_sql.execute('INSERT INTO chat (id_1, id_2) VALUES (?, ?)', (id_1, user_id))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("Yes", user_id))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("Yes", id_1))
        chat_db.commit()

        await bot.send_message(user_id, '<b> 🎭  Собеседник найден, начинайте общаться ! </b>', parse_mode = "html", reply_markup = reply_markups.leave_anonym_chat_button)
        await bot.send_message(id_1, '<b> 🎭  Собеседник найден, начинайте общаться ! </b>', parse_mode = "html", reply_markup = reply_markups.leave_anonym_chat_button)
                




# CANCEL QUEUE
async def cancel_queue(message):

    user_id = main_sql.execute('SELECT id FROM user_access WHERE id = ?', (message.chat.id,)).fetchone()[0]
    id_1 = chat_sql.execute('SELECT id FROM queue').fetchone()[0]

    if id_1 == user_id:

        chat_sql.execute('UPDATE queue SET id = ?', ("-",))
        chat_db.commit()

        await bot.send_message(user_id, "<b> ❌  Вы отменили поиск. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
    
    else:

        await bot.send_message(user_id, "<b> Вы не находитесь в очереди ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.menu_button)





#  LEAVE
async def leave_chat(message):

    user_id = main_sql.execute('SELECT id FROM user_access WHERE id = ?', (message.chat.id,)).fetchone()[0]
    id_1 = chat_sql.execute('SELECT id_1 FROM chat WHERE id_1 = ?', (user_id,)).fetchall()

    if id_1:
        
        id_2 = chat_sql.execute('SELECT id_2 FROM chat WHERE id_1 = ?', (user_id,)).fetchone()[0]
        chat_sql.execute('DELETE FROM chat WHERE id_1 = ?', (user_id,))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", user_id))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", id_2))
        chat_db.commit()
        
        await bot.send_message(user_id, "<b> ❌  Вы покинули чат. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
        await bot.send_message(id_2, "<b> Собеседник покинул чат ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
        
    else:

        id_2 = chat_sql.execute('SELECT id_1 FROM chat WHERE id_2 = ?', (user_id,)).fetchone()[0]
        chat_sql.execute('DELETE FROM chat WHERE id_2 = ?', (user_id,))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", user_id))
        chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", id_2))
        chat_db.commit()

        await bot.send_message(user_id, "<b> ❌  Вы покинули чат. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
        await bot.send_message(id_2, "<b> Собеседник покинул чат ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)