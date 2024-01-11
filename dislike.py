from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import sqlite3
import datetime

import config
import inline_markups



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




async def dislike_profile(call):

    #  SELECTING DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]
    
    #  CHECK ID
    dislikes_sql.execute(f'SELECT dislikes FROM dislikes_{id_2} WHERE dislikes = ?', (call.message.chat.id,))
    dislikes_id = dislikes_sql.fetchone()

    #  CHECK DISLIKE
    if dislikes_id is not None:
        await bot.send_message(id_1, f"Вы уже ставили <b>дизлайк</b> пользователю  <code>{username_2}</code> ❗️", parse_mode="html", reply_markup=inline_markups.hide_inline)
    
    else:
        dislikes_sql.execute(f'INSERT INTO dislikes_{id_2} (dislikes, username) VALUES (?, ?)', (id_1, username_1))
        dislikes_db.commit()

        main_sql.execute('UPDATE user_statistics SET dislikes = dislikes + 1 WHERE id = ?', (id_2,))
        main_db.commit()

        await bot.send_message(id_1, f"💔  Вы поставили <b>дизлайк</b> пользователю  <code>{username_2}</code>", parse_mode="html", reply_markup=inline_markups.hide_inline)

        #  WRITE TO FILE
        with open("actions/dislikes.txt", "a+") as dislike_file:
            dislike_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
            dislike_file.close()


