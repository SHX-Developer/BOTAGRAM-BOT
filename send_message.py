from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import datetime

import config
import inline_markups
import reply_markups


#  LIBRARY VARIABLES

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






#  SEND MESSAGE

async def send_message(message):

    #  CHAT STATUS
    main_sql.execute(f'SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    #  SELECTING DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAME
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  INLINE BUTTON
    reply_inline = InlineKeyboardMarkup()
    reply_inline.row(InlineKeyboardButton("👤  Посмотреть профиль", callback_data=f"profile_{id_1}"))
    reply_inline.row(InlineKeyboardButton("💌  Ответить", callback_data=f"replymessage_{id_1}"))

    if user_chat_status == "Yes":
        await bot.send_message(id_1, f'✅  Ваше сообщение отправлено пользователю  <code>{username_2}</code>\n\n💬  Ваше сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_markups.leave_chat_button)
        await delete_message(message)
        
        #  WRITE TO FILE
        with open("actions/messages.txt", "a+") as message_file:
            message_file.write(f"[{date_time}]:  {username_1}  -  {username_2}  -  {message.text}\n\n")
            message_file.close()
        try:
            await bot.send_message(id_2, f'🔔  У вас новое сообщение от пользователя  <code>{username_1}</code>\n\n💬  Сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_inline)
        except Exception as e:
            await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")

    else:
        await bot.send_message(id_1, f'✅  Ваше сообщение отправлено пользователю  <code>{username_2}</code>\n\n💬  Ваше сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_markups.menu_button)   
        await delete_message(message)

        #  WRITE TO FILE
        with open("actions/messages.txt", "a+") as message_file:
            message_file.write(f"[{date_time}]:  {username_1}  -  {username_2}  -  {message.text}\n\n")
            message_file.close()
        try:
            await bot.send_message(id_2, f'🔔  У вас новое сообщение от пользователя  <code>{username_1}</code>\n\n💬  Сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_inline)
        except Exception as e:
            await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")









#  VIEW STATUS SEND MESSAGE

async def view_status_send_message(message):

    #  CHAT STATUS
    main_sql.execute(f'SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    #  SELECTING DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAME
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  INLINE BUTTON
    reply_inline = InlineKeyboardMarkup()
    reply_inline.row(InlineKeyboardButton("👤  Посмотреть профиль", callback_data=f"profile_{id_1}"))
    reply_inline.row(InlineKeyboardButton("💌  Ответить", callback_data=f"replymessage_{id_1}"))

    if user_chat_status == "Yes":
        await bot.send_message(id_1, f'✅  Ваше сообщение отправлено пользователю  <code>{username_2}</code>\n\n💬  Ваше сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_markups.leave_chat_button)
        await delete_message(message)
        
        #  WRITE TO FILE
        with open("actions/messages.txt", "a+") as message_file:
            message_file.write(f"[{date_time}]:  {username_1}  -  {username_2}  -  {message.text}\n\n")
            message_file.close()
        try:
            await bot.send_message(id_2, f'🔔  У вас новое сообщение от пользователя  <code>{username_1}</code>\n\n💬  Сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_inline)
        except Exception as e:
            await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")

    else:
        await bot.send_message(id_1, f'✅  Ваше сообщение отправлено пользователю  <code>{username_2}</code>\n\n💬  Ваше сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_markups.view_profiles_button)   
        await delete_message(message)
        
        #  WRITE TO FILE
        with open("actions/messages.txt", "a+") as message_file:
            message_file.write(f"[{date_time}]:  {username_1}  -  {username_2}  -  {message.text}\n\n")
            message_file.close()
        try:
            await bot.send_message(id_2, f'🔔  У вас новое сообщение от пользователя  <code>{username_1}</code>\n\n💬  Сообщение:  <code>{message.text}</code>', parse_mode="html", reply_markup=reply_inline)
        except Exception as e:
            await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")





#  DELETE MESSAGES
async def delete_message(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass