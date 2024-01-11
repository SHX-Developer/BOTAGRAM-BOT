from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio
import sqlite3
import datetime
import shutil

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





#  DISPLAY NEW PROFILE
async def display_new_profile(message):

    #  SELECTING ID
    main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (message.chat.id,))
    id_1 = main_sql.fetchone()[0]

    #  SELECTING DATA
    main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (id_1,))
    data = main_sql.fetchone()

    #  FOLLOWERS / LIKES
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{message.chat.id}')
    user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{message.chat.id}')
    user_likes = likes_sql.fetchone()[0]

    #  DISPLAY NEW PROFILE
    with open(f"photo/{id_1}.jpg", 'rb') as profile_photo:
        await bot.send_photo(
            chat_id = message.chat.id, 
            photo = profile_photo,
            caption =   
            f"👤  <b>Юзернейм:</b>    <code>{data[1]}</code>"
            f"\n\n🪪  <b>Имя:</b>    {data[2]}"
            f"\n🔞  <b>Возраст:</b>    {data[3]}"
            f"\n🏙️  <b>Город:</b>    {data[4]}"
            f"\n\n👫  <b>Пол:</b>    {data[5]}"
            f"\n👩‍❤️‍👨  <b>Статус:</b>    {data[6]}"
            f"\n\n💬  <b>О себе:</b>    {data[7]}"
            f"\n\n👥  <b>Подписчиков:</b>  {user_followers}"
            f"\n❤️  <b>Лайков:</b>  {user_likes}",
            parse_mode = "html", reply_markup = inline_markups.new_profile_inline)



#  DISPLAY PROFILE
async def display_profile(message):

    #  SELECTING DATA
    main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (message.chat.id,))
    data = main_sql.fetchone()

    #  FOLLOWERS / LIKES
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{message.chat.id}')
    user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{message.chat.id}''')
    user_likes = likes_sql.fetchone()[0]

    #  VERIFICATION
    main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (message.chat.id,))
    user_verification = main_sql.fetchone()[0]

    #  PROFILE DATA
    profile_data = (
    f"👤  <b>Юзернейм:</b>    <code>{data[1]}</code>"
    f"{'  ☑️' if user_verification == 'Yes' else ''}"
    f"\n\n🪪  <b>Имя:</b>    {data[2]}"
    f"\n🔞  <b>Возраст:</b>    {data[3]}"
    f"\n🏙️  <b>Город:</b>    {data[4]}"
    f"\n\n👫  <b>Пол:</b>    {data[5]}"
    f"\n👩‍❤️‍👨  <b>Статус:</b>    {data[6]}"
    f"\n\n💬  <b>О себе:</b>    {data[7]}"
    f"\n\n👥  <b>Подписчиков:</b>  {user_followers}"
    f"\n❤️  <b>Лайков:</b>  {user_likes}")

    #  DISPLAY PROFILE
    with open(f"photo/{message.chat.id}.jpg", "rb") as profile_photo:
        button = inline_markups.profile_inline_2 if user_verification == 'Yes' else inline_markups.profile_inline_1
        await bot.send_photo(
            chat_id = message.chat.id, 
            photo = profile_photo, 
            caption = profile_data,
            parse_mode="html", 
            reply_markup=button)



#  DISPLAY OWN PROFILE
async def display_own_profile(message):

    #  SELECTING DATA
    main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (message.chat.id,))
    data = main_sql.fetchone()

    #  FOLLOWERS / LIKES
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{message.chat.id}')
    user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{message.chat.id}''')
    user_likes = likes_sql.fetchone()[0]

    #  VERIFICATION
    main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (message.chat.id,))
    user_verification = main_sql.fetchone()[0]

    #  PROFILE DATA 
    profile_data = (
    f"👤  <b>Юзернейм:</b>    <code>{data[1]}</code>"
    f"{'  ☑️' if user_verification == 'Yes' else ''}"
    f"\n\n🪪  <b>Имя:</b>    {data[2]}"
    f"\n🔞  <b>Возраст:</b>    {data[3]}"
    f"\n🏙️  <b>Город:</b>    {data[4]}"
    f"\n\n👫  <b>Пол:</b>    {data[5]}"
    f"\n👩‍❤️‍👨  <b>Статус:</b>    {data[6]}"
    f"\n\n💬  <b>О себе:</b>    {data[7]}"
    f"\n\n👥  <b>Подписчиков:</b>  {user_followers}"
    f"\n❤️  <b>Лайков:</b>  {user_likes}")

    #  DISPLAY PROFILE
    with open(f"photo/{message.chat.id}.jpg", "rb") as profile_photo:
        await bot.send_photo(
            chat_id = message.chat.id, 
            photo = profile_photo, 
            caption = profile_data,
            parse_mode = "html", 
            reply_markup = reply_markups.menu_button)





#  PROFILE SETTINGS

async def profile_settings(call):
    with open(f"photo/{call.message.chat.id}.jpg", "rb") as profile_photo:
        await bot.edit_message_media(
            media = types.InputMedia(
            type = 'photo',
            media = profile_photo,
            caption = "Выберите что хотите изменить в своем профиля:"),
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            reply_markup = inline_markups.profile_settings_inline)

async def display_profile_settings(message):
    with open(f"photo/{message.chat.id}.jpg", "rb") as profile_photo:
        await bot.send_photo(
            chat_id = message.chat.id,
            photo = profile_photo,
            caption = "Выберите что хотите изменить в своем профиля:",
            reply_markup = inline_markups.profile_settings_inline)





#  BACK TO PROFILE
async def back_to_profile(call):

    #  SELECTING DATA
    main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (call.message.chat.id,))
    data = main_sql.fetchone()

    #  USER FOLLOWERS / FOLLOWS
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{call.message.chat.id}')
    user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{call.message.chat.id}')
    user_likes = likes_sql.fetchone()[0]

    #  VERIFICATION
    main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (call.message.chat.id,))
    user_verification = main_sql.fetchone()[0]

    #  PROFILE DATA 
    profile_data = (
    f"👤  <b>Юзернейм:</b>    <code>{data[1]}</code>"
    f"{'  ☑️' if user_verification == 'Yes' else ''}"
    f"\n\n🪪  <b>Имя:</b>    {data[2]}"
    f"\n🔞  <b>Возраст:</b>    {data[3]}"
    f"\n🏙️  <b>Город:</b>    {data[4]}"
    f"\n\n👫  <b>Пол:</b>    {data[5]}"
    f"\n👩‍❤️‍👨  <b>Статус:</b>    {data[6]}"
    f"\n\n💬  <b>О себе:</b>    {data[7]}"
    f"\n\n👥  <b>Подписчиков:</b>  {user_followers}"
    f"\n❤️  <b>Лайков:</b>  {user_likes}")

    #  DISPLAY PROFILE
    with open(f"photo/{call.message.chat.id}.jpg", "rb") as profile_photo:
        button = inline_markups.profile_inline_2 if user_verification == 'Yes' else inline_markups.profile_inline_1
        await bot.edit_message_media(
            media = types.InputMedia(
            type = 'photo',
            media = profile_photo,
            caption = profile_data,
            parse_mode = "html"),
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            reply_markup = button)




#  DISPLAY PUBLIC CHAT
async def display_public_chat(message):

    #  SELECTING COUNT OF "ID's"
    main_sql.execute('SELECT COUNT(id) FROM user_chat WHERE status = ?', ("Yes",))
    chat_users = main_sql.fetchone()[0]

    #  DISPLAY CHAT
    if chat_users > 0:
        await bot.send_message(
            chat_id = message.chat.id,   
            text = 
            f'<b>🎭  PUBLIC CHAT  🎭</b>'
            f'\n\n<b>🤗  Группа, разработанная внутри самого бота, где пользователи могут общаться и знакомиться друг с другом.</b>'
            f'\n\n\n<i><b>🎲  В группе поддерживаются:</b>'
            f'\n\n✉️  Текстовые сообщения'
            f'\n🎙  Голосовые сообщения'
            f'\n🎭  Стикеры'
            f'\n🖼  Фотографии'
            f'\n📹  Видео'
            f'\n🎶  Аудио</i>'
            f'\n\n\n<i>👥  Пользователей в чате:  <b>{chat_users}</b></i>',
            parse_mode="html", reply_markup=inline_markups.join_chat_inline_1)

    else:
        await bot.send_message(
            chat_id = message.chat.id,   
            text = 
            f'<b>🎭  PUBLIC CHAT  🎭</b>'
            f'\n\n<b>🤗  Группа, разработанная внутри самого бота, где пользователи могут общаться и знакомиться друг с другом.</b>'
            f'\n\n\n<i><b>🎲  В группе поддерживаются:</b>'
            f'\n\n✉️  Текстовые сообщения'
            f'\n🎙  Голосовые сообщения'
            f'\n🎭  Стикеры'
            f'\n🖼  Фотографии'
            f'\n📹  Видео'
            f'\n🎶  Аудио</i>'
            f'\n\n\n<i>👥  Пользователей в чате:  <b>{chat_users}</b></i>',
            parse_mode="html", reply_markup=inline_markups.join_chat_inline_2)



#  DISPLAY ANONYM CHAT
async def display_anonym_chat(message):
    await bot.send_message(
        chat_id = message.chat.id,   
        text = 
        f'<b>👻  ANONYM CHAT  👻</b>'
        f'\n\n<b>🤗  Анонимный чат, где пользователи будут попадаться со случайными пользователями и общаться полностью анонимно.</b>'
        f'\n\n\n<i><b>🎲  В группе поддерживаются:</b></i>'
        f'\n\n✉️  Текстовые сообщения',
        parse_mode = "html", reply_markup = inline_markups.anonym_chat_inline)






#  DISPLAY FAVORITES
async def display_favorites(message):

    main_sql.execute("SELECT * FROM user_statistics ORDER BY followers DESC LIMIT 10")
    followers_data = main_sql.fetchall()
    main_sql.execute("SELECT * FROM user_statistics ORDER BY likes DESC LIMIT 10")
    likes_data = main_sql.fetchall()

    #  FOLLOWERS
    number = 0
    message_text = "<b>👥  Лидеры по подписчикам  👥</b>\n\n"

    for row in followers_data:
        number += 1
        message_text += f"{number}.  <b>[ {row[2]} ]</b>  подписчиков  —  <code>{row[1]}</code>\n"
    await bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)

    #  LIKES
    number = 0
    message_text = "<b>❤️  Лидеры по лайкам  ❤️</b>\n\n"

    for row in likes_data:
        number += 1
        message_text += f"{number}.  <b>[ {row[4]} ]</b>   лайков  —  <code>{row[1]}</code>\n"
    await bot.send_message(message.chat.id, message_text, parse_mode="html", reply_markup=inline_markups.hide_inline)