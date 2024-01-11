from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

import sqlite3
import asyncio
import datetime
import time
from emoji import emoji_list
import re
import shutil

import config
import database
import reply_markups
import inline_markups
import view_profiles
import profile_statistics
import search_user
import send_message
import display
import public_chat
import anonym_chat
import settings
import follow
import unfollow
import like
import dislike
import reply_callbacks
import admin
import forward


#  LIBRARY VARIABLES

main_db = sqlite3.connect("database/user_data.db", check_same_thread = False)
followers_db = sqlite3.connect("database/followers.db", check_same_thread = False)
follows_db = sqlite3.connect("database/follows.db", check_same_thread = False)
likes_db = sqlite3.connect("database/likes.db", check_same_thread = False)
dislikes_db = sqlite3.connect("database/dislikes.db", check_same_thread = False)
views_db = sqlite3.connect("database/views.db", check_same_thread = False)
chat_db = sqlite3.connect("database/chat.db", check_same_thread = False)

main_sql = main_db.cursor()
followers_sql = followers_db.cursor()
follows_sql = follows_db.cursor()
likes_sql = likes_db.cursor()
dislikes_sql = dislikes_db.cursor()
views_sql = views_db.cursor()
chat_sql = chat_db.cursor()

storage = MemoryStorage()

bot = Bot(config.token)
dp = Dispatcher(bot, storage = MemoryStorage())

date_time = datetime.datetime.now().date()

symbols =  ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "+", "=", "№", "?",
            "[", "]", "{", "}", "|", "/", ":", ";", '"', "'", ",", "<", ".", ">")



#  REGISTER
class RegisterStates(StatesGroup):
    username = State()
    gender = State()

#  PROFILE
class ProfileStates(StatesGroup):
    username = State()
    firstname = State()
    age = State()
    city = State()
    gender = State()
    status = State()
    bio = State()
    photo = State()

#  SEARCH
class SearchState(StatesGroup):
    username = State()

#  MESSAGE
class MessageState(StatesGroup):
    username = State()
    message = State()

#  REPLY
class ReplyState(StatesGroup):
    message = State()

#  VIEW STATUS
class ViewStatusState(StatesGroup):
    message = State()

#  SETTINGS
class SettingsStates(StatesGroup):
    gender = State()
    city = State()

#  ADMIN
class AdminStates(StatesGroup):
    verify = State()
    unverify = State()
    forward = State()
    delete_from_chat = State()
    delete_profile = State()







#  CREATING DATABASES

main_sql.execute("CREATE TABLE IF NOT EXISTS user_access (id INTEGER, username TEXT, firstname TEXT, lastname TEXT, date TIMESTAMP)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_profile (id INTEGER, username TEXT, firstname TEXT, age TEXT, city TEXT, gender TEXT, status TEXT, bio TEXT, photo BLOB)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_action (id_1 INTEGER, id_2 INTEGER)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_chat (id INTEGER, username TEXT, status TEXT)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_verification (id INTEGER, username TEXT, verification TEXT)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_photo (id INTEGER, count INTEGER)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_statistics (id INTEGER, username TEXT, followers INTEGER, follows INTEGER, likes INTEGER, dislikes INTEGER, views INTEGER)")
main_sql.execute("CREATE TABLE IF NOT EXISTS user_settings (id INTEGER, username TEXT, gender TEXT, age TEXT, city TEXT, notifications TEXT, verification TEXT)")
main_db.commit()

chat_sql.execute('CREATE TABLE IF NOT EXISTS user_status (id INTEGER, status TEXT)')
chat_sql.execute('CREATE TABLE IF NOT EXISTS queue (id INTEGER)')
chat_sql.execute('CREATE TABLE IF NOT EXISTS chat (id_1 INTEGER, id_2 INTEGER)')
chat_db.commit()










#  START COMMAND

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):

    main_sql.execute('INSERT INTO user_access (id, username, firstname, lastname, date) VALUES (?, ?, ?, ?, ?)',
    (str(message.chat.id), str(message.from_user.username), str(message.from_user.first_name), str(message.from_user.last_name), date_time))
    main_db.commit()

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat = main_sql.fetchone()

    if user_chat == None:

        main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (message.chat.id,))
        user_id = main_sql.fetchone()

        if user_id == None:

            await bot.send_message(message.chat.id,   "👋  Приветсвуем вас, новый пользователь !")
            await asyncio.sleep(2)
            await get_username(message)

        else:

            await bot.send_message(message.chat.id, "🏠  Главное меню:", parse_mode="html", reply_markup = reply_markups.menu_button)

    elif user_chat[0] == "Yes":

        await public_chat.leave_chat(message)

    else:

        await bot.send_message(message.chat.id, "🏠  Главное меню:", parse_mode="html", reply_markup = reply_markups.menu_button)

#  GET USERNAME

async def get_username(message):
    await bot.send_message(message.chat.id, "👇  Придумайте себе новый <b>ЮЗЕРНЕЙМ</b>:", parse_mode="html")
    await RegisterStates.username.set()

#  CHECK USERNAME

@dp.message_handler(state = RegisterStates.username)
async def check_useranme(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

        main_sql.execute('SELECT username FROM user_profile WHERE username = ?', (message.text,))
        found_username = main_sql.fetchone()

        #  EXISTS
        if found_username:
            await bot.send_message(message.chat.id, '❗️ Данный <b>ЮЗЕРНЕЙМ</b> уже занят.', parse_mode = "html")
            await delete_message(message)

        #  COMMANDS
        elif message.text == "/start" or message.text == "/menu":
            await bot.send_message(message.chat.id, '❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать символы.', parse_mode = "html")
            await delete_message(message)

        #  SYMBOLS
        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, '❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать символы.', parse_mode = "html")
            await delete_message(message)

        #  EMOJI
        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, '❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать эмодзи.', parse_mode = "html")
            await delete_message(message)

        #  PROBELS
        elif " " in message.text:
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать отступы.", parse_mode = "html")
            await delete_message(message)

        #  LENGTH
        elif len(message.text) < 6:
            await bot.send_message(message.chat.id, '❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать меньше 6 букв.', parse_mode = "html")
            await delete_message(message)

        elif len(message.text) > 15:
            await bot.send_message(message.chat.id, '❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать больше 15 букв.', parse_mode = "html")
            await delete_message(message)

        else:
            #  CREATING PHOTO
            original_photo_path = "photo/profile_photo.jpg"
            new_photo_path = f"photo/{message.chat.id}.jpg"
            shutil.copy2(original_photo_path, new_photo_path)

            await RegisterStates.next()
            await database.add_user_data(message)

#  GET GENDER

async def display_gender(message):
    await bot.send_message(message.chat.id, '✅  Успешно !')
    await delete_message(message)
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, '👫  Давайте определимся, кого вы ищете ?', reply_markup = reply_markups.reg_gender_reply)
    await asyncio.sleep(2)

#  CHECK GENDER

@dp.message_handler(state = RegisterStates.gender)
async def check_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        if message.text == '🙋‍♂️  Парней':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Парень", message.chat.id))
            main_db.commit()
            await state.finish()
            await registration(message)

        elif message.text == '🙋‍♀️  Девушек':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Девушка", message.chat.id))
            main_db.commit()
            await state.finish()
            await registration(message)

        elif message.text == '👻  Без разницы':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Без разницы", message.chat.id))
            main_db.commit()
            await state.finish()
            await registration(message)

        else:
            await bot.send_message(message.chat.id, '👫  Выберите пол:', reply_markup = reply_markups.reg_gender_reply)
            await delete_message(message)

#  REGISTRATION

async def registration(message):

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
    user_username = main_sql.fetchone()[0]

    await bot.send_message(284929331, f'🎉  Зарегестрировался новый пользователь  -  <code>{user_username}</code>  🎉', parse_mode = "html")
    await bot.send_message(message.chat.id, '✅  Определились !')
    await delete_message(message)
    await asyncio.sleep(1)
    await bot.send_message(message.chat.id, '❤️  Добро пожаловать  -  BOTAGRAM !')
    await asyncio.sleep(2)
    await bot.send_message(message.chat.id, '📝  Давайте заполним ваш профиль:', reply_markup = reply_markups.menu_button)
    await asyncio.sleep(2)
    await display.display_new_profile(message)



#  MENU COMMAND

@dp.message_handler(commands=["menu"])
async def menu_command(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.leave_chat(message)
    else:
        await bot.send_message(message.chat.id, '🏠  Главное меню:', parse_mode="html", reply_markup=reply_markups.menu_button)



#  HELP COMMAND

@dp.message_handler(commands=["help"])
async def help_command(message):

    inline = InlineKeyboardMarkup()
    inline.row(InlineKeyboardButton(text = "Прочитать", url = "https://telegra.ph/BOTAGRAM-08-26"))

    await bot.send_message(message.chat.id, 'Информация и Инструкция использования бота:', parse_mode="html", reply_markup=inline)





#  FORWARD 1
@dp.message_handler(commands=["forward_1"])
async def rassylka_1(message):

    inline = InlineKeyboardMarkup()
    inline.row(InlineKeyboardButton(text = "Перейти на канал", url = "https://t.me/botagram_channel"))

    if message.chat.id == 284929331:
        await bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html", reply_markup=reply_markups.forward_button)

        main_sql.execute('SELECT * FROM user_profile')
        data = main_sql.fetchall()
        main_sql.execute('SELECT COUNT(id) FROM user_profile')
        all_users = main_sql.fetchone()[0]

        await bot.send_message(284929331, "☑️  Просим вас подписаться на наш официальный канал о проекте, где зараннее будете уведомлены об обновлениях, новостях а также будут проводиться конкурсы на призы  🎁", parse_mode = "html", reply_markup = inline)
        total = 0

        for users in data:
            try:
                await bot.send_message(users[0], "☑️  Просим вас подписаться на наш официальный канал о проекте, где зараннее будете уведомлены об обновлениях, новостях а также будут проводиться конкурсы на призы  🎁", parse_mode = "html", reply_markup = inline)

                total += 1
                print(f"[{users[0]}]: получил сообщение  ✅")

            except Exception:
                print(f"[{users[0]}]: заблокировал бота  ❌")

        else:
            blocked_users = all_users - total
            await bot.send_message(message.chat.id, f"<b>✅  Ваше сообщение успешно отправлено:  {total}  пользователям из:  {all_users}   </b>", parse_mode="html", reply_markup=None)
            await bot.send_message(message.chat.id, f"<b>❌  Заблокировавшие пользователи:  {blocked_users} </b>", parse_mode="html", reply_markup=None)

#  FORWARD 2
@dp.message_handler(commands = ["forward_chat"])
async def rassylka_chat(message):

    if message.chat.id == 284929331:
        await bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html", reply_markup=reply_markups.forward_button)

        main_sql.execute('SELECT * FROM user_profile')
        data = main_sql.fetchall()
        main_sql.execute('SELECT COUNT(id) FROM user_profile')
        all_users = main_sql.fetchone()[0]

        total = 0

        for users in data:
            try:
                with open("chat.jpg", "rb") as photo:
                    await bot.send_photo(users[0], photo, caption = "Совсем скоро . . .")

                print(f"[{users[1]}]: получил(a) сообщение  ✅")
            except Exception:
                print(f"[{users[1]}]: заблокировал(a) бота  ❌")

        else:
            blocked_users = all_users - total
            await bot.send_message(message.chat.id, f"Всего:  <b>{all_users}</b> пользователей.", parse_mode="html", reply_markup=None)
            await bot.send_message(message.chat.id, f"Отправлено:  <b>{total}</b> пользователям.", parse_mode="html", reply_markup=None)
            await bot.send_message(message.chat.id, f"Заблокировали:  <b>{blocked_users}</b> пользователей.", parse_mode="html", reply_markup=None)

#  FORWARD
@dp.message_handler(commands = ["forward"])
async def rassylka(message):

    if message.chat.id == 284929331:
        await bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html", reply_markup=reply_markups.forward_button)

        main_sql.execute('SELECT id FROM user_profile WHERE photo = ?', ("-",))
        data = main_sql.fetchall()
        main_sql.execute('SELECT COUNT(id) FROM user_profile')
        all_users = main_sql.fetchone()[0]

        await bot.send_message(284929331, "😇  Благодарим вас за вашу активность ! Продолжим поиск профилей?!  🔥\n\n😌  Просим вас заполнить свой профиль для лучшего охвата профилей. \n\n🙌  Теперь, чтобы искать профили, нужно хотя бы иметь фотографию в своем профиле (не обязательно свою).", parse_mode="html", reply_markup=None)
        total = 0

        for users in data:
            try:
                await bot.send_message(users[0], "😇  Благодарим вас за вашу активность ! Продолжим поиск профилей?!  🔥\n\n😌  Просим вас заполнить свой профиль для лучшего охвата профилей. \n\n🙌  Теперь, чтобы искать профили, нужно хотя бы иметь фотографию в своем профиле (не обязательно свою).", parse_mode="html", reply_markup=None)

                total += 1
                print(f"[{users[0]}]: получил сообщение  ✅")
            except Exception:
                print(f"[{users[0]}]: заблокировал бота  ❌")

        else:
            blocked_users = all_users - total
            await bot.send_message(message.chat.id, f"<b>✅  Ваше сообщение успешно отправлено:  {total}  пользователям из:  {all_users}   </b>", parse_mode="html", reply_markup=None)
            await bot.send_message(message.chat.id, f"<b>❌  Заблокировавшие пользователи:  {blocked_users} </b>", parse_mode="html", reply_markup=None)















#  VOICE
@dp.message_handler(content_types = ["voice"])
async def send_voice(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.send_voice(message)

#  STICKERS
@dp.message_handler(content_types=["sticker"])
async def send_sticker(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.send_sticker(message)

#  PHOTO
@dp.message_handler(content_types=["photo"])
async def photo(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.send_photo(message)

#  VIDEO
@dp.message_handler(content_types = ["video"])
async def video(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.send_video(message)

#  AUDIO
@dp.message_handler(content_types = ["audio"])
async def send_audio(message):

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
    user_chat_status = main_sql.fetchone()[0]

    if user_chat_status == "Yes":
        await public_chat.send_audio(message)










#  TEXT
@dp.message_handler()
async def text(message: types.Message):

    main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (message.chat.id,))
    user_id = main_sql.fetchone()

    # chat_sql.execute('SELECT status FROM user_status WHERE id = ?', (message.chat.id,))
    # chat_status = main_sql.fetchone()

    if user_id is not None:
        main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
        user_chat_status = main_sql.fetchone()[0]

        if user_chat_status == "Yes":
            if message.text == "❌  Покинуть чат  ❌":
                await public_chat.leave_chat(message)
            else:
                await public_chat.send_message(message)

        elif user_chat_status == "No":
            # if chat_status == "Yes":

            #     if message.text == "❌  Покинуть чат":
            #         user_id = main_sql.execute('SELECT id FROM user_access WHERE id = ?', (message.chat.id,)).fetchone()[0]
            #         id_1 = chat_sql.execute('SELECT id_1 FROM chat WHERE id_1 = ?', (user_id,)).fetchall()

            #         if id_1:
            #             id_2 = chat_sql.execute('SELECT id_2 FROM chat WHERE id_1 = ?', (user_id,)).fetchone()[0]
            #             chat_sql.execute('DELETE FROM chat WHERE id_1 = ?', (user_id,))
            #             chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", user_id))
            #             chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", id_2))
            #             chat_db.commit()

            #             await bot.send_message(user_id, "<b> ❌  Вы покинули чат. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
            #             await bot.send_message(id_2, "<b> Собеседник покинул чат ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)

            #         else:
            #             id_2 = chat_sql.execute('SELECT id_1 FROM chat WHERE id_2 = ?', (user_id,)).fetchone()[0]
            #             chat_sql.execute('DELETE FROM chat WHERE id_2 = ?', (user_id,))
            #             chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", user_id))
            #             chat_sql.execute('UPDATE user_status SET status = ? WHERE id = ?', ("No", id_2))
            #             chat_db.commit()

            #             await bot.send_message(user_id, "<b> ❌  Вы покинули чат. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)
            #             await bot.send_message(id_2, "<b> Собеседник покинул чат ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)

            #     else:
            #         chat_sql.execute('SELECT id_1 FROM chat WHERE id_1 = ?', (user_id,))
            #         id_1 = chat_sql.fetchall()

            #         if id_1:
            #             id_2 = chat_sql.execute('SELECT id_2 FROM chat WHERE id_1 = ?', (user_id,)).fetchone()[0]
            #             await bot.send_message(id_2, message.text)

            #         else:
            #             id_2 = chat_sql.execute('SELECT id_1 FROM chat WHERE id_2 = ?', (user_id,)).fetchone()[0]
            #             await bot.send_message(id_2, message.text)


        #  PROFILE

            if message.text == "👤  Профиль":
                await display.display_profile(message)



        #  VIEW PROFILES

            elif message.text == "🚀  Смотреть профили":
                await view_profiles.view_profiles(message)



        #  SEND MESSAGE

            elif message.text == "💌  Написать":
                await MessageState.username.set()
                await bot.send_message(
                    chat_id = message.chat.id,
                    text = 'Введите <b>"ЮЗЕРНЕЙМ"</b> получателя:',
                    parse_mode = "html",
                    reply_markup = reply_markups.cancel_button)



        #  SEARCH

            elif message.text == "🔍  Поиск":
                await SearchState.username.set()
                await bot.send_message(
                    chat_id = message.chat.id,
                    text = 'Введите <b>"ЮЗЕРНЕЙМ"</b> пользователя:',
                    parse_mode = "html",
                    reply_markup = reply_markups.cancel_button)



        #  FAVORITES

            elif message.text == "🏆  Фавориты":
                await display.display_favorites(message)



        #  SETTINGS

            elif message.text == "⚙️  Настройки":
                await settings.settings(message)



        #  CHAT

            elif message.text == "🌐  Чат":
                await display.display_public_chat(message)

            elif message.text == "🎭  Публичный чат":
                await display.display_public_chat(message)

            elif message.text == "👻  Анонимный чат":
                await display.display_anonym_chat(message)




            elif message.text == "❌  Отменить поиск":
                user_id = main_sql.execute('SELECT id FROM user_access WHERE id = ?', (message.chat.id,)).fetchone()[0]
                id_1 = chat_sql.execute('SELECT id FROM queue').fetchone()[0]

                if id_1 == user_id:
                    chat_sql.execute('UPDATE queue SET id = ?', ("-",))
                    chat_db.commit()

                    await bot.send_message(user_id, "<b> ❌  Вы отменили поиск. </b>", parse_mode = "html", reply_markup = reply_markups.chat_button)

                else:
                    await bot.send_message(user_id, "<b> Вы не находитесь в очереди ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.menu_button)



            elif message.text == "❌  Покинуть чат":
                await bot.send_message(user_id, "<b> Вы не находитесь в чате ❗️ </b>", parse_mode = "html", reply_markup = reply_markups.menu_button)



        #  CANCEL

            elif message.text == "❌  Отмена  ❌":
                await bot.send_message(message.chat.id, "🏠  Главное меню:", reply_markup = reply_markups.menu_button)
                await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
                await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)

        #  MAIN MENU

            elif message.text == "🏠  Главное меню":
                await bot.send_message(message.chat.id, "🏠  Главное меню:", reply_markup = reply_markups.menu_button)
                await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)





        #  ADMIN

            elif message.text == 'Админ' or message.text == 'админ' or message.text == 'flvby' or message.text == 'Flvby':
                if message.chat.id == 284929331:
                    await bot.send_message(284929331, "<b> Вы зашли в меню разработчиков: </b>", parse_mode="html", reply_markup=reply_markups.admin_menu)



        #  STATISTICS

            elif message.text == "Статистика":
                if message.chat.id == 284929331:
                    await admin.bot_statistics(message)

        #  SEND MESSAGE

            elif message.text == "Сообщение":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "В разработке . . .")

        #  FORWARD

            elif message.text == "Рассылка":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "<b> Выберите тип рассылки: </b>", parse_mode="html", reply_markup=reply_markups.forward_button)

            elif message.text == "Рассылка сообщения":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "Введите <b>ТЕКСТ</b> которого хотите <b>РАССЫЛАТЬ</b>:", parse_mode="html", reply_markup=reply_markups.cancel_button)

            elif message.text == "Рассылка обновления":
                if message.chat.id == 284929331:
                    await forward.forward_update(message)

            elif message.text == "Рассылка чата":
                if message.chat.id == 284929331:
                    await forward.forward_chat(message)

        #  VERIFICATION

            elif message.text == "Верификация":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "<b> Выберите раздел: </b>", parse_mode="html", reply_markup=reply_markups.verification_button)

            elif message.text == "Выдать верификацию":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "Введите <b>ЮЗЕРНЕЙМ</b> пользователя которого хотите <b>ПОДТВЕРДИТЬ</b>:", parse_mode="html")

            elif message.text == "Отменить верификацию":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "Введите <b>ЮЗЕРНЕЙМ</b> пользователя которого хотите <b>ОПРОВЕРГНУТЬ</b>:", parse_mode="html")

        #  DELETE USER

            elif message.text == "Удалить":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "<b> Выберите раздел: </b>", parse_mode="html", reply_markup=reply_markups.delete_user_button)

            elif message.text == "Удалить из чата":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "Введите <b>ЮЗЕРНЕЙМ</b> пользователя которого хотите <b>УДАЛИТЬ</b> из чата:", parse_mode="html")

            elif message.text == "Удалить всех из чата":
                if message.chat.id == 284929331:
                    await admin.delete_all_chat_users(message)

            elif message.text == "Удалить все данные":
                if message.chat.id == 284929331:
                    await bot.send_message(message.chat.id, "Введите <b>ЮЗЕРНЕЙМ</b> пользователя которого хотите <b>УДАЛИТЬ</b>:", parse_mode="html")

        #  BACK TO ADMIN MENU

            elif message.text == "Назад":
                if message.chat.id == 284929331:
                    await bot.send_message(284929331, "<b>Вы в панели разработчика: </b>", parse_mode="html", reply_markup=reply_markups.admin_menu)

        #  EXIT ADMIN MENU

            elif message.text == "Выйти из меню разработчиков":
                if message.chat.id == 284929331:
                    await bot.send_message(284929331, "<b> Вы вышли из меню разработчиков: </b>", parse_mode="html", reply_markup=reply_markups.menu_button)

    else:
        await bot.send_message(message.chat.id, "❗️ Чтобы пользоваться ботом, зарегестрирутесь ❗️", parse_mode="html", reply_markup=reply_markups.start_button)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)









#  CALLBACKS

@dp.callback_query_handler(lambda call: True)
async def callback(call: types.CallbackQuery):



#  VIEW PROFILES

    #  NEXT PROFILE
    if call.data == "next_profile":
        await view_profiles.view_profiles_call(call)





#  PROFILE SETTINGS

    #  DISPLAY PROFILE SETTINGS
    elif call.data == "profile_settings":
        await display.profile_settings(call)


    #  EDIT USERNAME
    elif call.data == "edit_username":
        await ProfileStates.username.set()
        await bot.send_message(call.message.chat.id, "👤  Введите юзернейм:", reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT  FIRSTNAME
    elif call.data == "edit_firstname":
        await ProfileStates.firstname.set()
        await bot.send_message(call.message.chat.id, "🪪  Введите своё имя:", reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT AGE
    elif call.data == "edit_age":
        await ProfileStates.age.set()
        await bot.send_message(call.message.chat.id, "🔞  Введите ваш возраст:", reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT CITY
    elif call.data == "edit_city":
        await ProfileStates.city.set()
        await bot.send_message(call.message.chat.id, "🏙️  Введите свой город:", reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT GENDER
    elif call.data == "edit_gender":
        await ProfileStates.gender.set()
        await bot.send_message(call.message.chat.id, "👫  Выберите свой пол:", reply_markup = reply_markups.edit_gender_reply)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT STATUS
    elif call.data == "edit_status":
        await ProfileStates.status.set()

        main_sql.execute('SELECT gender FROM user_profile WHERE id = ?', (call.message.chat.id,))
        user_gender = main_sql.fetchone()[0]

        if user_gender == "Парень":
            await bot.send_message(call.message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.male_edit_status_reply)
            await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

        elif user_gender == "Девушка":
            await bot.send_message(call.message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.female_edit_status_reply)
            await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

        else:
            await bot.send_message(call.message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.edit_status_reply)
            await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT BIO
    elif call.data == "edit_bio":
        await ProfileStates.bio.set()
        await bot.send_message(call.message.chat.id, "💬  Расскажите о себе:", reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  EDIT PHOTO
    elif call.data == "edit_photo":
        await ProfileStates.photo.set()
        await bot.send_message(call.message.chat.id, '🖼  Отправьте фотографию:', reply_markup = reply_markups.cancel_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)





#  STATISTICS

    #  DISPLAY STATISTICS
    elif call.data == "statistics":
        await profile_statistics.statistics(call)


    #  MY FOLLOWERS
    elif call.data == "my_followers":
        await profile_statistics.followers_statistics(call)

    #  MY FOLLOWS
    elif call.data == "my_follows":
        await profile_statistics.follows_statistics(call)

    #  MY LIKES
    elif call.data == "my_likes":
        await profile_statistics.likes_statistics(call)

    #  MY DISLIKES
    elif call.data == "my_dislikes":
        await profile_statistics.dislikes_statistics(call)

    #  MY VIEWS
    elif call.data == "my_views":
        await profile_statistics.views_statistics(call)





#  BACK TO PROFILE

    elif call.data == "back_to_profile":
        await display.back_to_profile(call)





#  SETTINGS

    #  DISPLAY GENDERS
    elif call.data == "set_gender":
        await SettingsStates.gender.set()
        await bot.send_message(call.message.chat.id, "👫  Какого пола вы ищете?", reply_markup = reply_markups.gender_settings_reply)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  DISPLAY CITY SETTINGS
    elif call.data == "set_city":
        await SettingsStates.city.set()
        await bot.send_message(call.message.chat.id, "🏙️  Введите город, с которого хотите искать людей:", reply_markup=reply_markups.cancel_city_button)
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)

    #  DISPLAY NOTIFICATION SETTINGS
    elif call.data == "set_age":
        await bot.send_message(call.message.chat.id, "В разработке . . .", reply_markup = None)

    #  DISPLAY NOTIFICATION SETTINGS
    elif call.data == "set_notifications":
        await bot.send_message(call.message.chat.id, "В разработке . . .", reply_markup = None)





#  ACTIONS

    #  FOLLOW
    elif call.data.startswith("follow_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await follow.follow_profile(call)

    #  UNFOLLOW
    elif call.data.startswith("unfollow_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await unfollow.unfollow_profile(call)

    #  LIKE
    elif call.data.startswith("like_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await like.like_profile(call)

    #  DISLIKE
    elif call.data.startswith("dislike_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await dislike.dislike_profile(call)

    #  SEND MESSAGE
    elif call.data.startswith("message_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await bot.send_message(call.message.chat.id, "Введите своё сообщение:", reply_markup=reply_markups.cancel_button)
        await ViewStatusState.message.set()



#  REPLY ACTIONS

    #  ANSWER
    elif call.data.startswith("replymessage_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await bot.send_message(call.message.chat.id, "Введите своё сообщение:", reply_markup = reply_markups.cancel_button)
        await ReplyState.message.set()

    #  FOLLOW
    elif call.data.startswith("replyfollow_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.follow_profile(call)

    #  UNFOLLOW
    elif call.data.startswith("replyunfollow_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.unfollow_profile(call)

    #  LIKE
    elif call.data.startswith("replylike_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.like_profile(call)

    #  DISLIKE
    elif call.data.startswith("replydislike_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.dislike_profile(call)

    #  PROFILE
    elif call.data.startswith("profile_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.reply_profile(call)











#  CHAT

#  PUBLIC CHAT

    #  JOIN CHAT
    elif call.data == "join_chat":
        await public_chat.join_chat(call)

    #  VIEW CHAT USERS
    elif call.data == "view_chat_users":
        await public_chat.view_chat_users(call)

    #  SEND HELLO
    elif call.data == "send_hello":
        await public_chat.send_hello(call)

    #  SEND GREETING
    elif call.data.startswith("sendgreeting_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.send_greeting(call)

    #  DELETE CHAT MESSAGE
    elif call.data == "delete_chat_message":
        if call.message.chat.id == 284929331:
            await public_chat.delete_chat_message(call)

#  ANONYM CHAT

    #  SEARCH ANONYM USER
    elif call.data == "search_anonym_user":

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
            try:
                await bot.delete_message(chat_id = user_id, message_id = call.message.message_id)
                await bot.delete_message(chat_id = id_1, message_id = call.message.message_id - 1)
            except:
                pass




#  VERIFICATION

    #  DISPLAY VERIFICATION
    elif call.data == "verification":
        await bot.send_message(
            chat_id = call.message.chat.id,
            text =
            "<b> ☑️ Верификация - подтверждение личности пользователя ☑️</b>"
            "\n\nВерифицированные пользователи отличаются от неверифицированных со специальными галочками в профиле."
            "\n\n<b>Требования верификации:</b>"
            "\n<b>1.</b> Заполнить все поля в своем профиле."
            "\n<b>2.</b> В профиле должна быть своя фотография с лицом."
            "\n<b>3.</b> Имя в профиле должно быть настоящее."
            "\n\nЕсли ваш профиль соблюдает всем требованиям выше, можете подать заявку на верификацию  😊",
            parse_mode="html", reply_markup = inline_markups.verification_inline)

    #  SEND VERIFICATION
    elif call.data == "send_verification":
        main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (call.message.chat.id,))
        user_username = main_sql.fetchone()[0]
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.send_message(call.message.chat.id, "✅  Ваша заявка на верификацию успешно отправлена на проверку администраторам !", parse_mode="html")
        await bot.send_message(284929331, f"Новая заявка на верификацию от пользователя  <code>{user_username}</code>", parse_mode="html")





#  HIDE MESSAGE  #

    elif call.data == "hide_message":
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)










#  ADMIN MENU

    #  DISPLAY ALL USERS
    elif call.data == "show_all_users":
        if call.message.chat.id == 284929331:
            await admin.show_all_users(call.message)

    #  DISPLAY VERIFIED USERS
    elif call.data == "show_verified_users":
        if call.message.chat.id == 284929331:
            await admin.show_verified_users(call.message)

    #  DISPLAY USERS WITH PHOTO
    elif call.data == "show_photo_users":
        if call.message.chat.id == 284929331:
            await admin.show_photo_users(call.message)

    #  ADMIN - VIEW PROFILE
    elif call.data.startswith("user_"):
        user_id = call.data.split("_")[1]
        main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (user_id, call.message.chat.id))
        main_db.commit()
        await reply_callbacks.reply_profile(call)









#  PROFILE SETTINGS

#  EDIT USERNAME
@dp.message_handler(state = ProfileStates.username)
async def edit_username(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text
        message.text = str.lower(message.text)

        main_sql.execute('SELECT username FROM user_profile WHERE username = ?', (message.text,))
        found_username = main_sql.fetchone()

        if message.text == '❌  отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif found_username:
            await bot.send_message(message.chat.id, "❗️ Данный <b>ЮЗЕРНЕЙМ</b> уже занят.", parse_mode="html")
            await delete_message(message)

        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать символы.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать эмодзи.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif " " in message.text:
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать отступы.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif len(message.text) > 15:
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать более 15 букв.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif len(message.text) < 6:
            await bot.send_message(message.chat.id, "❗️ <b>ЮЗЕРНЕЙМ</b> не должен содержать меньше 6 букв.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            main_sql.execute('UPDATE user_profile SET username = ? WHERE id = ?', (message.text, message.chat.id))
            main_sql.execute('UPDATE user_chat SET username = ? WHERE id = ?', (message.text, message.chat.id))
            main_sql.execute('UPDATE user_verification SET username = ? WHERE id = ?', (message.text, message.chat.id))
            main_sql.execute('UPDATE user_statistics SET username = ? WHERE id = ?', (message.text, message.chat.id))
            main_sql.execute('UPDATE user_settings SET username = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()

            await bot.send_message(message.chat.id, "✅  Ваш <b>ЮЗЕРНЕЙМ</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

#  EDIT FIRSTNAME
@dp.message_handler(state = ProfileStates.firstname)
async def edit_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, "❗️ <b>ИМЯ</b> не должно содержать символы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ИМЯ</b> не должно содержать эмодзи.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif re.findall(r"\d+", message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ИМЯ</b> не должно содержать числа.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif " " in message.text:
            await bot.send_message(message.chat.id, "❗️ <b>ИМЯ</b> не должно содержать отступы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif len(message.text) > 15:
            await bot.send_message(message.chat.id, "❗️ <b>ИМЯ</b> не должно содержать более 15 букв.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            message.text = str.title(message.text)
            main_sql.execute('UPDATE user_profile SET firstname = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваше <b>ИМЯ</b> обновлено !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

#  EDIT AGE
@dp.message_handler(state = ProfileStates.age)
async def edit_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, "❗️ <b>ВОЗРАСТ</b> не должен содержать символы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ВОЗРАСТ</b> не должен содержать эмодзи.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif any(char.isalpha() for char in message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ВОЗРАСТ</b> не должен содержать буквы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif " " in message.text:
            await bot.send_message(message.chat.id, "❗️ <b>ВОЗРАСТ</b> не должен содержать отступы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif len(message.text) > 2:
            await bot.send_message(message.chat.id, "❗️ <b>ВОЗРАСТ</b> не должен содержать более 2 чисел.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            main_sql.execute('UPDATE user_profile SET age = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>ВОЗРАСТ</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

#  EDIT CITY
@dp.message_handler(state = ProfileStates.city)
async def edit_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать символы.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать эмодзи.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif re.findall(r"\d+", message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать числа.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        elif len(message.text) > 20:
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать более 20 букв.", parse_mode = "html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            message.text = str.title(message.text)
            main_sql.execute('UPDATE user_profile SET city = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>ГОРОД</b> обновлен  !", parse_mode="html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

#  EDIT GENDER
@dp.message_handler(state = ProfileStates.gender)
async def edit_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == '🙋‍♂️  Парень':
            main_sql.execute('UPDATE user_profile SET gender = ? WHERE id = ?', ("Парень", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>ПОЛ</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == '🙋‍♀️  Девушка':
            main_sql.execute('UPDATE user_profile SET gender = ? WHERE id = ?', ("Девушка", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>ПОЛ</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == '👻  Другое':
            main_sql.execute('UPDATE user_profile SET gender = ? WHERE id = ?', ("Другое", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>ПОЛ</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        else:
            await bot.send_message(message.chat.id, "👫  Выберите свой пол:", reply_markup = reply_markups.edit_gender_reply)
            await delete_message(message)

#  STATUS
@dp.message_handler(state = ProfileStates.status)
async def edit_status(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['status'] = message.text

        main_sql.execute('SELECT gender FROM user_profile WHERE id = ?', (message.chat.id,))
        user_gender = main_sql.fetchone()[0]

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == 'В отношениях':
            main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("В отношениях", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == 'В разводе':
            main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("В разводе", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif message.text == 'В активном поиске':
            main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("В активном поиске", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        else:

            #  MALE
            if user_gender == "Парень":
                if message.text == 'Свободен':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Свободен", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                elif message.text == 'В отношениях':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("В отношениях", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                elif message.text == 'Женат':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Женат", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                else:
                    await bot.send_message(message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.cancel_button)
                    await delete_message(message)

            #  FEMALE
            elif user_gender == "Девушка":

                if message.text == 'Свободна':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Свободна", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                elif message.text == 'Замужем':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Замужем", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                else:
                    await bot.send_message(message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.cancel_button)
                    await delete_message(message)

            #  UNKNOWN
            else:

                if message.text == 'Свободен(на)':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Свободен(на)", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                elif message.text == 'Женат / Замужем':
                    main_sql.execute('UPDATE user_profile SET status = ? WHERE id = ?', ("Женат / Замужем", message.chat.id))
                    main_db.commit()
                    await bot.send_message(message.chat.id, "✅  Ваш <b>СТАТУС</b> обновлён  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
                    await state.finish()
                    await delete_message(message)
                    await asyncio.sleep(1)
                    await display.display_profile_settings(message)

                else:
                    await bot.send_message(message.chat.id, "👩‍❤️‍👨  Выберите свой статус:", reply_markup = reply_markups.cancel_button)
                    await delete_message(message)

#  EDIT BIO
@dp.message_handler(state = ProfileStates.bio)
async def edit_bio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

        elif len(message.text) > 300:
            await bot.send_message(message.chat.id, "❗️ <b>О СЕБЕ</b> не должен содержать более 300 букв.", parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            main_sql.execute('UPDATE user_profile SET bio = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваше <b>О СЕБЕ</b> обновлено  !", parse_mode="html", reply_markup=reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await display.display_profile_settings(message)

#  EDIT PHOTO
@dp.message_handler(content_types = types.ContentTypes.ANY, state = ProfileStates.photo)
async def edit_photo(message: types.Message, state: FSMContext):

    if message.text == '❌  Отмена  ❌':
        await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
        await state.finish()
        await delete_message(message)
        await asyncio.sleep(1)
        await display.display_profile_settings(message)

    elif message.photo:

        main_sql.execute('SELECT count FROM user_photo WHERE id = ?', (message.chat.id,))
        user_photo_count = main_sql.fetchone()[0]

        #  CLONING PHOTO
        original_photo_path = f"photo/{message.chat.id}.jpg"
        new_photo_path = f"photo/backup/{message.chat.id} ({user_photo_count + 1}).jpg"
        shutil.copy2(original_photo_path, new_photo_path)

        await message.photo[-1].download(destination_file = f"photo/{message.chat.id}.jpg")

        main_sql.execute('UPDATE user_profile SET photo = ? WHERE id = ?', ("Yes", message.chat.id))
        main_sql.execute('UPDATE user_photo SET count = count + 1 WHERE id = ?', (message.chat.id,))
        main_db.commit()

        await bot.send_message(message.chat.id, "✅  Ваша <b>ФОТОГРАФИЯ</b> была обновлена  !", parse_mode="html", reply_markup=reply_markups.menu_button)
        await state.finish()
        await delete_message(message)
        await asyncio.sleep(1)
        await display.display_profile_settings(message)

    else:
        await bot.send_message(message.chat.id, '🖼  Отправьте фотографию:', reply_markup = reply_markups.cancel_button)




#  SEND MESSAGE
@dp.message_handler(state = MessageState.username)
async def check_message_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

        main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
        user_username = main_sql.fetchone()[0]

        if message.text == "❌  Отмена  ❌":
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', parse_mode="html", reply_markup=reply_markups.menu_button)
            await state.finish()
            await delete_message(message)

        elif message.text == user_username:
            await bot.send_message(message.chat.id, '❗️ Нельзя писать самому себе.', parse_mode="html", reply_markup = reply_markups.cancel_button)
            await delete_message(message)

        else:
            main_sql.execute('SELECT username FROM user_profile WHERE username = ?', (message.text,))
            success_username = main_sql.fetchone()

            if success_username:
                main_sql.execute('SELECT id FROM user_profile WHERE username = ?', (message.text,))
                id_2 = main_sql.fetchone()[0]
                main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (id_2, message.chat.id))
                main_db.commit()
                await bot.send_message(message.chat.id, "Введите ваше сообщение:", reply_markup = reply_markups.cancel_button)
                await state.finish()
                await MessageState.message.set()

            else:
                await bot.send_message(message.chat.id, '❗️ Пользователь с таким <b>ЮЗЕРНЕЙМ</b> не найден.', parse_mode="html", reply_markup = reply_markups.cancel_button)
                await delete_message(message)

@dp.message_handler(state = MessageState.message)
async def send_message_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

        if message.text == "❌  Отмена  ❌":
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', parse_mode="html", reply_markup=reply_markups.menu_button)
            await state.finish()
            await delete_message(message)

        else:
            await state.finish()
            await send_message.send_message(message)


#  REPLY MESSAGE
@dp.message_handler(state = ReplyState.message)
async def reply_message_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

        if message.text == "❌  Отмена  ❌":
            main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (message.chat.id,))
            user_chat_status = main_sql.fetchone()[0]

            if user_chat_status == "Yes":
                await bot.send_message(message.chat.id, '❌  Отменено', parse_mode = "html", reply_markup = reply_markups.leave_chat_button)
                await state.finish()
                await delete_message(message)

            else:
                await bot.send_message(message.chat.id, '❌  Отменено', parse_mode = "html", reply_markup = reply_markups.menu_button)
                await state.finish()
                await delete_message(message)

        else:
            await state.finish()
            await reply_callbacks.reply_message(message)


#  VIEW STATUS SEND MESSAGE
@dp.message_handler(state = ViewStatusState.message)
async def reply_message_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text

        if message.text == "❌  Отмена  ❌":
            await bot.send_message(message.chat.id, '❌  Отменено', parse_mode = "html", reply_markup = reply_markups.view_profiles_button)
            await state.finish()
            await delete_message(message)

        else:
            await state.finish()
            await send_message.view_status_send_message(message)






#  SEARCH
@dp.message_handler(state = SearchState.username)
async def check_message_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['username'] = message.text

        main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (message.chat.id,))
        user_username = main_sql.fetchone()[0]

        if message.text == "❌  Отмена  ❌":
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', parse_mode="html", reply_markup=reply_markups.menu_button)
            await state.finish()
            await delete_message(message)

        elif message.text == user_username:
            await state.finish()
            await delete_message(message)
            await display.display_own_profile(message)

        else:
            main_sql.execute('SELECT username FROM user_profile WHERE username = ?', (message.text,))
            found_username = main_sql.fetchone()

            if found_username:
                await state.finish()
                await search_user.search(message)

            else:
                await bot.send_message(message.chat.id, '❗️ Пользователь с таким <b>ЮЗЕРНЕЙМ</b> не найден.', parse_mode="html", reply_markup = reply_markups.cancel_button)
                await delete_message(message)






#  SETTINGS

#  GENDER
@dp.message_handler(state = SettingsStates.gender)
async def gender_settings(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        elif message.text == '🙋‍♂️  Парней':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Парень", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваши настройки <b>ПОЛА</b> обновлены  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        elif message.text == '🙋‍♀️  Девушек':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Девушка", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваши настройки <b>ПОЛА</b> обновлены  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        elif message.text == '👻  Без разницы':
            main_sql.execute('UPDATE user_settings SET gender = ? WHERE id = ?', ("Без разницы", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Вашм настройки <b>ПОЛА</b> обновлены  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        else:
            await bot.send_message(message.chat.id, "👫  Какого пола вы ищете?", reply_markup = reply_markups.gender_settings_reply)

#  CITY
@dp.message_handler(state = SettingsStates.city)
async def city_settings(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text

        if message.text == '❌  Отмена  ❌':
            await bot.send_message(message.chat.id, '❌  Отменено  ❌', reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        elif message.text == "Без разницы":
            main_sql.execute('UPDATE user_settings SET city = ? WHERE id = ?', ("Без разницы", message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваши настройки <b>ГОРОДА</b> обновлены  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)

        elif any(symbol in message.text for symbol in symbols):
            await bot.send_message(message.chat.id, "❗️ <b>Город</b> не должен содержать символы.", parse_mode = "html", reply_markup = reply_markups.cancel_city_button)
            await delete_message(message)

        elif emoji_list(message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать эмодзи.", parse_mode = "html", reply_markup = reply_markups.cancel_city_button)
            await delete_message(message)

        elif re.findall(r"\d+", message.text):
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать числа.", parse_mode = "html", reply_markup = reply_markups.cancel_city_button)
            await delete_message(message)

        elif len(message.text) > 20:
            await bot.send_message(message.chat.id, "❗️ <b>ГОРОД</b> не должен содержать более 20 букв.", parse_mode = "html", reply_markup = reply_markups.cancel_city_button)
            await delete_message(message)

        else:
            message.text = str.title(message.text)
            main_sql.execute('UPDATE user_settings SET city = ? WHERE id = ?', (message.text, message.chat.id))
            main_db.commit()
            await bot.send_message(message.chat.id, "✅  Ваши настройки <b>ГОРОДА</b> обновлены  !", parse_mode = "html", reply_markup = reply_markups.menu_button)
            await state.finish()
            await delete_message(message)
            await asyncio.sleep(1)
            await settings.settings(message)



#  DELETE MESSAGES
async def delete_message(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass



#  ON START UP
async def start_bot(_):
    await bot.send_message(284929331, 'Бот успешно включён !')




#  LAUNCH
if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates = True, on_startup = start_bot)
    except Exception as e:
        print(e)