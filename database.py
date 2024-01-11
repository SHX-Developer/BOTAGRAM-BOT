from aiogram import Bot, Dispatcher, executor, types

import asyncio
import sqlite3
import datetime

import config
import botagram


#  LIBRARY VARIABLES

main_db = sqlite3.connect("database/user_data.db", check_same_thread=False)
followers_db = sqlite3.connect("database/followers.db", check_same_thread=False)
follows_db = sqlite3.connect("database/follows.db", check_same_thread=False)
likes_db = sqlite3.connect("database/likes.db", check_same_thread=False)
dislikes_db = sqlite3.connect("database/dislikes.db", check_same_thread=False)
views_db = sqlite3.connect("database/views.db", check_same_thread=False)
chat_db = sqlite3.connect("database/chat.db", check_same_thread = False)

main_sql = main_db.cursor()
followers_sql = followers_db.cursor()
follows_sql = follows_db.cursor()
likes_sql = likes_db.cursor()
dislikes_sql = dislikes_db.cursor()
views_sql = views_db.cursor()
chat_sql = chat_db.cursor()

bot = Bot(config.token)
dp = Dispatcher(bot)

date_time = datetime.datetime.now().date()






async def add_gender(message):

    main_sql.execute('INSERT INTO user_settings (id, username, gender, age, notifications) VALUES (?, ?, ?, ?, ?)',
    (str(message.chat.id), (message.text), "Без разницы", "Без разницы", "Включены"))
    main_db.commit()

    await botagram.display_gender(message)



async def add_user_data(message):

    message.text = str.lower(message.text)

    #  CREATING followers / follows TABLES

    followers_sql.execute(f'CREATE TABLE IF NOT EXISTS followers_{message.chat.id} (followers INTEGER, username TEXT)')
    followers_db.commit()

    follows_sql.execute(f'CREATE TABLE IF NOT EXISTS follows_{message.chat.id} (follows INTEGER, username TEXT)')
    follows_db.commit()

    likes_sql.execute(f'CREATE TABLE IF NOT EXISTS likes_{message.chat.id} (likes INTEGER, username TEXT)')
    likes_db.commit()

    dislikes_sql.execute(f'CREATE TABLE IF NOT EXISTS dislikes_{message.chat.id} (dislikes INTEGER, username TEXT)')
    dislikes_db.commit()

    views_sql.execute(f'CREATE TABLE IF NOT EXISTS views_{message.chat.id} (views INTEGER, username TEXT)')
    views_db.commit()

    #  INSERT USER DATA

    main_sql.execute('INSERT INTO user_profile (id, username, firstname, age, city, gender, status, bio, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
    (message.chat.id, message.text, "-", "-", "-", "-", "-", "-", "-"))

    main_sql.execute('INSERT INTO user_action (id_1, id_2) VALUES (?, ?)',
    (message.chat.id, "-"))

    main_sql.execute('INSERT INTO user_chat (id, username, status) VALUES (?, ?, ?)',
    (message.chat.id, message.text, "No"))

    main_sql.execute('INSERT INTO user_photo (id, count) VALUES (?, ?)',
    (message.chat.id, -1))

    main_sql.execute('INSERT INTO user_settings (id, username, gender, age, city, notifications, verification) VALUES (?, ?, ?, ?, ?, ?, ?)''',
    (message.chat.id, message.text, "Без разницы", "Без разницы", "Без разницы", "Включены", "Отключена"))

    main_sql.execute('INSERT INTO user_statistics (id, username, followers, follows, likes, dislikes, views) VALUES (?, ?, ?, ?, ?, ?, ?)',
    (message.chat.id, message.text, 0, 0, 0, 0, 0))

    main_sql.execute('INSERT INTO user_verification (id, username, verification) VALUES (?, ?, ?)',
    (message.chat.id, message.text, "No"))

    main_db.commit()

    # chat_sql.execute('INSERT INTO user_status (id, status) VALUES (?, ?)', (message.chat.id, "No"))
    # chat_db.commit()

    await botagram.display_gender(message)






