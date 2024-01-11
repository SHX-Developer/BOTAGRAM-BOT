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





#  STATISTICS
async def bot_statistics(message):

    main_sql.execute('SELECT COUNT(id) FROM user_profile')
    users_count = main_sql.fetchone()[0]

    main_sql.execute('SELECT COUNT(id) FROM user_verification WHERE verification = ?', ("Yes",))
    verify_count = main_sql.fetchone()[0]

    main_sql.execute('SELECT COUNT(id) FROM user_profile WHERE photo = ?', ("Yes",))
    photo_count = main_sql.fetchone()[0]

    await bot.send_message(
        chat_id = 284929331,
        text = 
        f'<b>Количество пользователей:</b>  {users_count}'
        f'\n\n<b>Верифицированные пользователи:</b>  {verify_count}'
        f'\n\n<b>Имеют фото в профиле:</b>  {photo_count}',
        parse_mode="html", reply_markup=inline_markups.admin_statistics_inline)


#  SHOW ALL USERS
async def show_all_users(message):

    main_sql.execute('SELECT * FROM user_profile')
    data = main_sql.fetchall()

    number = 0
    buttons = []
    message_text = "<b>Список пользователей в боте:</b>\n\n"

    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
        buttons.append([InlineKeyboardButton(text = row[1], callback_data = f"user_{row[0]}")])
    username_inline = InlineKeyboardMarkup(buttons)
    await bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)


#  SHOW VERIFIED USERS
async def show_verified_users(message):

    main_sql.execute('SELECT * FROM user_verification WHERE verification = ?', ("Yes"))
    data = main_sql.fetchall()

    message_text = "<b>Список верифицированных пользователей:</b>\n\n"
    number = 0

    for row in data:

        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"

    await bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)


#  SHOW PHOTO USERS
async def show_photo_users(message):

    main_sql.execute('SELECT * FROM user_profile WHERE photo = ?', ("Yes"))
    data = main_sql.fetchall()

    message_text = "<b>Список пользователей с фото в профиле:</b>\n\n"
    number = 0

    for row in data:
        number += 1
        message_text += f"<b>{number}.</b>   <code>{row[1]}</code>\n"
    await bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)










#  VERIFY
async def verify_user(message):
    try:
        main_sql.execute('UPDATE user_verification SET verification = ? WHERE username = ?', ("Yes", message.text))
        main_sql.execute('UPDATE user_settings SET verification = ? WHERE username = ?', ("Включена", message.text))
        main_db.commit()

        main_sql.execute('SELECT id FROM user_verification WHERE username = ?', (message.text,))
        id_2 = main_sql.fetchone()[0]

        await bot.send_message(message.chat.id, f"Вы выдали <b>ПОДТВЕРЖДЕНИЕ</b> пользователю  <code>{message.text}</code>  ✅", parse_mode="html")
        await bot.send_message(id_2, '🎉  Поздравляем, ваш профиль был <b>ПОДТВЕРЖДЕН</b>  ✅\n\nТеперь ваш профиль стал <b>ПОДТВЕРЖДЕННЫМ</b> и имеет специальную <b>галочку</b>  "☑️"', parse_mode="html")

    except:
        await bot.send_message(message.chat.id, "Неправильный <b>ЮЗЕРНЕЙМ</b> !", parse_mode="html")

#  UNVERIFY
async def unverify_user(message):
    try:
        main_sql.execute('UPDATE user_verification SET verification = ? WHERE username = ?', ("No", message.text))
        main_sql.execute('UPDATE user_settings SET verification = ? WHERE username = ?', ("Отключена", message.text))
        main_db.commit()

        main_sql.execute('SELECT id FROM user_verification WHERE username = ?', (message.text,))
        id_2 = main_sql.fetchone()[0]

        await bot.send_message(message.chat.id, f"Вы отняли <b>ПОДТВЕРЖДЕНИЕ</b> у пользователя  <code>{message.text}</code>  ❌", parse_mode="html")
        await bot.send_message(id_2, '❗️ Ваш профиль больше не является <b>ПОДТВЕРЖДЕННЫМ</b>  ❌\n\nНа вашем профиле теперь не будет отображаться специальная <b>галочка</b>  "☑️"', parse_mode="html")

    except:
        await bot.send_message(message.chat.id, "Неправильный <b>ЮЗЕРНЕЙМ</b> !", parse_mode="html")








#  DELETE USER FROM CHAT

async def delete_chat_user(message):
    try:
        #  SELECT ID
        main_sql.execute('SELECT id FROM user_profile WHERE username = ?', (message.text,))
        id_2 = main_sql.fetchone()[0]

        #  CHAT STATUS
        main_sql.execute('SELECT status FROM user_chat WHERE username = ?', (message.text,))
        user_chat_status = main_sql.fetchone()[0]

        if user_chat_status == "Yes":

            #  CHAT USERS
            main_sql.execute('SELECT id FROM user_chat WHERE status = ? AND id != ?', ("Yes", id_2))
            data = main_sql.fetchall()

            main_sql.execute('UPDATE user_chat SET status = ? WHERE id = ?', ("No", id_2))
            main_db.commit()

            main_sql.execute('SELECT id FROM user_chat WHERE id = ?', (id_2,))
            id_2 = main_sql.fetchone()[0]

            await bot.send_message(message.chat.id, f"❌  Вы удалили пользователя <code>{message.text}</code> из чата", parse_mode="html")
            await bot.send_message(id_2, "❌  Вас исключили из чата", reply_markup=reply_markups.menu_button)

            for row in data:
                try:
                    await bot.send_message(row[0], f"❌  <code>{message.text}</code> исключен(а) из чата", parse_mode="html", reply_markup=inline_markups.hide_inline)
                except:
                    pass
        else:
            await bot.send_message(message.chat.id, f"Пользователь <code>{message.text}</code> не находится в чате !", parse_mode="html")
    except:
        await bot.send_message(message.chat.id, f"Неправильный <b>ЮЗЕРНЕЙМ</b> !", parse_mode="html")





#  DELETE ALL USERS FROM CHAT

def delete_all_chat_users(message):

    #  SELECT ID

    main_sql.execute(f'SELECT id FROM user_chat WHERE status = ("Yes")')
    data = main_sql.fetchall()

    for chat_users in data:

        try:

            main_sql.execute(f'UPDATE user_chat SET (status) = ("No") WHERE id = "{chat_users[0]}"')
            main_db.commit()

            bot.send_message(chat_users[0], "❗️ Чат был очищен", reply_markup=None)
            bot.send_message(chat_users[0], "❌  Вы покинули чат", reply_markup=reply_markups.menu_button)

        except:

            pass

    else:

        bot.send_message(message.chat.id, "✅  Чат очищен", parse_mode="html")









#   DELETE USER DATA

def delete_user_data(message):

    try:

        #  SELECT ID

        main_sql.execute('SELECT id FROM user_profile WHERE username = ?', (message.text,))
        id_2 = main_sql.fetchone()[0]

        #  DELETE USER DATA

        main_sql.execute('DELETE FROM user_action WHERE id_1 = ?', (id_2,))
        main_sql.execute('DELETE FROM user_profile WHERE id = ?', (id_2,))
        main_sql.execute('DELETE FROM user_settings WHERE id = ?', (id_2,))
        main_sql.execute('DELETE FROM user_statistics WHERE id = ?', (id_2,))
        main_sql.execute('DELETE FROM user_chat WHERE id = ?', (id_2,))
        main_sql.execute('DELETE FROM user_verification WHERE id = ?', (id_2,))
        main_sql.execute('DELETE FROM user_photo WHERE id = ?', (id_2,))

        main_db.commit()

        #  DELETE OTHER DB

        followers_sql.execute(f'DROP TABLE IF EXISTS followers_{id_2}')
        followers_db.commit()

        follows_sql.execute(f'DROP TABLE IF EXISTS follows_{id_2}')
        follows_db.commit()

        likes_sql.execute(f'DROP TABLE IF EXISTS likes_{id_2}')
        likes_db.commit()

        dislikes_sql.execute(f'DROP TABLE IF EXISTS dislikes_{id_2}')
        dislikes_db.commit()

        views_sql.execute(f'DROP TABLE IF EXISTS views_{id_2}')
        views_db.commit()

        #  SEND MESSAGE

        bot.send_message(message.chat.id, f"Данные пользователя {message.text} были удалены !")
        bot.send_message(id_2, "❗️ Ваш профиль и все ваши данные были удалены с бота ❗️")
        bot.send_message(id_2, "Чтобы зарегестрироваться заново, нажмите на кнопку ниже.", reply_markup=reply_markups.start_button)

    except Exception as e:

        bot.send_message(message.chat.id, e)