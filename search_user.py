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








#  SEARCH USER

async def search(message):
    try:
        #  SELECTING USER DATA
        main_sql.execute('SELECT * FROM user_profile WHERE username = ?', (message.text,))
        data = main_sql.fetchone()
        id_2 = data[0]

        #  UPDATE USER ACTION DATA
        main_sql.execute('UPDATE user_action SET (id_2) = ? WHERE id_1 = ?', (id_2, message.chat.id))
        main_db.commit()

        #  SELECTING IDS
        main_sql.execute('SELECT id_1 FROM user_action WHERE id_1 = ?', (message.chat.id,))
        id_1 = main_sql.fetchone()[0]
        main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
        username_1 = main_sql.fetchone()[0]

        #  VERIFICATION
        main_sql.execute('SELECT verification FROM user_verification WHERE username = ?', (message.text,))
        found_user_verification = main_sql.fetchone()[0]

        #  UPDATE USER STATISTICS
        main_sql.execute('UPDATE user_statistics SET views = views + 1 WHERE id = ?', (id_2,))
        main_db.commit()

        #  FOLLOWERS / LIKES
        followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
        found_user_followers = followers_sql.fetchone()[0]
        likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}')
        found_user_likes = likes_sql.fetchone()[0]

        #  CHECK FOLLOWERS
        followers_sql.execute(f'SELECT followers FROM followers_{id_2} WHERE followers = ?', (id_1,))
        followers_id = followers_sql.fetchone()

        #  PROFILE DATA
        profile_data = (
        f"👤  <b>Юзернейм:</b>    <code>{data[1]}</code>"
        f"{'  ☑️' if found_user_verification == 'Yes' else ''}"
        f"\n\n🪪  <b>Имя:</b>    {data[2]}"
        f"\n🔞  <b>Возраст:</b>    {data[3]}"
        f"\n🏙️  <b>Город:</b>    {data[4]}"
        f"\n\n👫  <b>Пол:</b>    {data[5]}"
        f"\n👩‍❤️‍👨  <b>Статус:</b>    {data[6]}"
        f"\n\n💬  <b>О себе:</b>    {data[7]}"
        f"\n\n👥  <b>Подписчиков:</b>  {found_user_followers}"
        f"\n❤️  <b>Лайков:</b>  {found_user_likes}")

        #  BUTTONS
        follow_inline = InlineKeyboardMarkup()
        follow_inline.row(InlineKeyboardButton(text = "➕ Подписаться", callback_data = f"replyfollow_{id_2}"),
                            InlineKeyboardButton(text = "💌  Написать", callback_data = f"replymessage_{id_2}"))
        follow_inline.row(InlineKeyboardButton(text = "❤️  Лайк", callback_data = f"replylike_{id_2}"),
                            InlineKeyboardButton(text = "💔  Дизлайк", callback_data = f"replydislike_{id_2}"))

        unfollow_inline = InlineKeyboardMarkup()
        unfollow_inline.row(InlineKeyboardButton(text = "➖  Отписаться", callback_data = f"replyunfollow_{id_2}"),
                            InlineKeyboardButton(text = "💌  Написать", callback_data = f"replymessage_{id_2}"))
        unfollow_inline.row(InlineKeyboardButton(text = "❤️  Лайк", callback_data = f"replylike_{id_2}"),
                            InlineKeyboardButton(text = "💔  Дизлайк", callback_data = f"replydislike_{id_2}"))

        #  SUCCESS SEARCH
        await bot.send_message(message.chat.id, "✅  Пользователь найден !", parse_mode="html", reply_markup=reply_markups.menu_button)
        await delete_message(message)

        #  DISPLAY PROFILE
        with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
            button = unfollow_inline if followers_id is not None else follow_inline
            await bot.send_photo(
                chat_id = message.chat.id, 
                photo = profile_photo, 
                caption = profile_data,
                parse_mode = "html", 
                reply_markup = button)

            #  VIEWS DATA
            views_sql.execute(f'SELECT views FROM views_{id_2} WHERE views = ?', (id_1,))
            views_id = views_sql.fetchone()

            if views_id is not None:
                pass
            else:
                #  INSERT VIEWS
                views_sql.execute(f'INSERT INTO views_{id_2} (views, username) VALUES (?, ?)', (id_1, username_1,))
                views_db.commit()
    except:
        await bot.send_message(message.chat.id, '❗️ Произошла ошибка.', parse_mode = "html", reply_markup = reply_markups.cancel_button)
        await delete_message(message)
    



#  DELETE MESSAGES
async def delete_message(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass




