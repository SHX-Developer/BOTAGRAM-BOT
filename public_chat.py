from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import sqlite3
import datetime
import time

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





#  JOIN
async def join_chat(call):

    main_sql.execute('UPDATE user_chat SET status = ? WHERE id = ?', ("Yes", call.message.chat.id))
    main_db.commit()

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (call.message.chat.id, "Yes"))
    data = main_sql.fetchall()

    await bot.send_message(call.message.chat.id,  '<b>👋  Добро пожаловать в чат  👋</b>', parse_mode = "html", reply_markup = reply_markups.leave_chat_button)
    await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    await bot.send_message(
        chat_id = call.message.chat.id,
        text =
        '<b>Внимание❗️</b>'
        '\n\n<i>Просим вас быть внимательными и уважительными к другим участникам, избегая оскорблений, связанных с политикой, нацизмом, религией и пропагандой.</i>'
        '\n\n<b><i>Спасибо за понимание !</i></b>',
        parse_mode = "html",
        reply_markup = inline_markups.hide_inline)

    await asyncio.sleep(2)
    await bot.send_message(call.message.chat.id, "👋  Можете воспользоваться кнопкой, чтобы поздароваться с пользователями в чате.", reply_markup = inline_markups.send_hello_inline)

    for row in data:
        try:
            if call.message.chat.id == 284929331:
                pass

            else:
                main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (call.message.chat.id,))
                id_2 = main_sql.fetchone()[0]

                main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (call.message.chat.id,))
                username_2 = main_sql.fetchone()[0]

                send_greeting_inline = InlineKeyboardMarkup()
                send_greeting_inline.row(InlineKeyboardButton(text="👋  Поприветствовать", callback_data=f"sendgreeting_{id_2}"))

                await bot.send_message(
                    chat_id = row[0],
                    text = f"✅  <code>{username_2}</code> присоединился(ась) в чат.",
                    parse_mode = "html",
                    reply_markup = send_greeting_inline)

        except:
            pass


#  LEAVE
async def leave_chat(message):

    main_sql.execute('UPDATE user_chat SET status = ? WHERE id = ?', ("No", message.chat.id))
    main_db.commit()

    main_sql.execute(f"SELECT * FROM user_chat WHERE id != ? AND status = ?", (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    await bot.send_message(message.chat.id, "❌  Вы покинули чат", reply_markup = reply_markups.menu_button)
    await delete_message(message)

    for row in data:
        try:
            if message.chat.id == 284929331:
                pass

            else:
                main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
                user_username = main_sql.fetchone()[0]

                await bot.send_message(
                    chat_id = row[0],
                    text = f"❌  <code>{user_username}</code> покинул(а) чат.",
                    parse_mode = "html",
                    reply_markup = inline_markups.hide_inline)

        except:
            pass




#  DISPLAY CHAT USERS
async def view_chat_users(call):
    main_sql.execute('SELECT * FROM user_chat WHERE status = ?', ("Yes",))
    data = main_sql.fetchall()

    number = 0
    message_text = "<b>Пользователи в чате:</b>\n\n"

    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = message_text,
        parse_mode = "html",
        reply_markup = inline_markups.hide_inline)





#  SEND HELLO
async def send_hello(call):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (call.message.chat.id,))
    user_status = main_sql.fetchone()[0]

    if user_status == "Yes":
        main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (call.message.chat.id, "Yes"))
        data = main_sql.fetchall()

        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.send_message(call.message.chat.id, "✅  Вы поприветствовали всех в чате.", reply_markup = inline_markups.hide_inline)

        for row in data:
            try:
                main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (call.message.chat.id,))
                user_username = main_sql.fetchone()[0]

                await bot.send_message(
                    chat_id = row[0],
                    text = f"<code>{user_username}</code>\n\n<b>Всем привет !</b>",
                    parse_mode="html",
                    reply_markup=None)

            except:
                pass

    else:
        await bot.send_message(call.message.chat.id, "❗️ Вы не находитесь в чате.")
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)










#  SEND MESSAGE
async def send_message(message):

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
    user_username = main_sql.fetchone()[0]

    # bot.send_message(284929331, f"<code>{user_username}</code>\n\n<b>{message.text}</b>", parse_mode = "html", reply_markup = inline_markups.delete_chat_message_inline)

    for row in data:
        try:
            await bot.send_message(
                chat_id = row[0],
                text = f"<code>{user_username}</code>\n\n<b>{message.text}</b>",
                parse_mode = "html",
                reply_markup = None)

        except:
            pass



#  SEND VOICE
async def send_voice(message):

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    for row in data:
        try:
            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
            user_username = main_sql.fetchone()[0]

            await bot.send_voice(
                chat_id = row[0],
                voice = message.voice.file_id,
                caption = f"<code>{user_username}</code>",
                parse_mode = "html",
                reply_markup = None)

        except:
            pass



#  SEND STICKER
async def send_sticker(message):

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    for row in data:
        try:
            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
            user_username = main_sql.fetchone()[0]

            await bot.send_message(
                chat_id = row[0],
                text = f"<code>{user_username}</code> отправляет стикер:",
                parse_mode = "html",
                reply_markup = None)

            await bot.send_sticker(
                chat_id = row[0],
                sticker = message.sticker.file_id,
                reply_markup = None)

        except:
            pass



#  SEND PHOTO
async def send_photo(message):

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    for row in data:
        try:
            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
            user_username = main_sql.fetchone()[0]

            await bot.send_photo(
                chat_id = row[0],
                photo = message.photo[-1].file_id,
                caption = f"<code>{user_username}</code>",
                parse_mode = "html",
                reply_markup = None)

        except:
            pass



#  SEND VIDEO
async def send_video(message):

    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    for row in data:
        try:
            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
            user_username = main_sql.fetchone()[0]

            await bot.send_video(
                chat_id = row[0],
                video = message.video.file_id,
                caption = f"<code>{user_username}</code>",
                parse_mode="html",
                reply_markup=None)

        except:
            pass



#  SEND AUDIO
async def send_audio(message):

    main_sql.execute("SELECT * FROM user_chat WHERE id != ? AND status = ?", (message.chat.id, "Yes"))
    data = main_sql.fetchall()

    for row in data:
        try:
            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
            user_username = main_sql.fetchone()[0]

            await bot.send_audio(
                chat_id = row[0],
                audio = message.audio.file_id,
                caption = f"<code>{user_username}</code>",
                parse_mode = "html",
                reply_markup = None)

        except:
            pass







#  DELETE MESSAGES
async def delete_message(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass






# #  DELETE CHAT MESSAGE

# def delete_chat_message(call):

#     # SELECT USERS IN "CHAT"

#     main_sql.execute('SELECT * FROM user_chat WHERE status = ?', ("Yes",))
#     data = main_sql.fetchall()

#     for row in data:

#         try:

#             bot.delete_message(chat_id=row[0], message_id=call.message.message_id)

#         except:

#             pass







#  SEND CHAT USERS

# def send_chat_users(message):

#     #  SELECT USERS IN "CHAT"

#     main_sql.execute(f"SELECT * FROM user_chat WHERE id != {message.chat.id} AND status = ('Yes')")
#     data = main_sql.fetchall()

#     message_text = "<b>Пользователи в чате:</b>\n\n"
#     number = 0

#     for row in data:

#         number += 1
#         message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"

#         try:

#             #  SELECT "USERNAME" OF "MESSAGE SENDER"

#             main_sql.execute(f"SELECT username FROM user_profile WHERE id = {message.chat.id}")
#             user_username = main_sql.fetchone()[0]

#             bot.send_message(row[0], f"<code>{user_username}</code>\n\n<b>{message.text}</b>", parse_mode="html", reply_markup=None)
#             bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)
#             bot.send_message(row[0], message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

#         except:

#             pass
















