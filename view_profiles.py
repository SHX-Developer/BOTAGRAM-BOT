from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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










#  VIEW PROFILES
async def view_profiles(message):

    main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (message.chat.id,))
    user_id = main_sql.fetchone()[0]

    #  SELECT SETTINGS

    main_sql.execute('SELECT gender, city FROM user_settings WHERE id = ?', (user_id,))
    settings = main_sql.fetchone()


    main_sql.execute('SELECT photo FROM user_profile WHERE id = ?', (user_id,))
    user_photo = main_sql.fetchone()[0]

    if user_photo == "-":
        await bot.send_message(message.chat.id, "❗️ Для поиска других профилей, в вашем профиле должна быть фотография.")

    else:

        #  ALGORITM
        if settings[1] == "Без разницы":

            if settings[0] == "Без разницы":

                #  CITY = FALSE, GENDER = FALSE

                main_sql.execute('SELECT id FROM user_profile WHERE id != ? ORDER BY RANDOM() LIMIT 1', (user_id,))
                random_id = main_sql.fetchone()

            else:

                #  CITY = FALSE, GENDER = TRUE

                main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND gender = "{settings[0]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
                random_id = main_sql.fetchone()

        else:

            if settings[0] == "Без разницы":

                #  CITY = TRUE, GENDER = FALSE

                main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND city = "{settings[1]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
                random_id = main_sql.fetchone()

            else:

                #  CITY = TRUE, GENDER = TRUE

                main_sql.execute('SELECT id FROM user_profile WHERE id != ? AND gender = ? AND city = ? ORDER BY RANDOM() LIMIT 1', (user_id, settings[0], settings[1]))
                random_id = main_sql.fetchone()

        #  RESULT

        if random_id:
            random_id = random_id[0]

            try:

                #  UPDATE USER ACTION DATA

                main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (random_id, user_id))
                main_sql.execute('UPDATE user_statistics SET views = views + 1 WHERE id = ?', (random_id,))
                main_db.commit()

                #  SELECT IDS

                main_sql.execute('SELECT id_1 FROM user_action WHERE id_1 = ?', (user_id,))
                id_1 = main_sql.fetchone()[0]

                main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
                username_1 = main_sql.fetchone()[0]

                #  SELECT USER DATA

                main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (random_id,))
                data = main_sql.fetchone()

                #  SELECT USER FOLLOWERS / FOLLOWS

                followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{random_id}')
                user_followers = followers_sql.fetchone()[0]

                likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{random_id}')
                user_likes = likes_sql.fetchone()[0]

                #  SELECT VERIFICATION

                main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (random_id,))
                user_verification = main_sql.fetchone()[0]

                #  SELECT FOLLOWERS DATA

                followers_sql.execute(f'SELECT followers FROM followers_{random_id} WHERE followers = ?', (user_id,))
                followers_id = followers_sql.fetchone()

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

                #  BUTTONS

                follow_inline = InlineKeyboardMarkup()
                follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"follow_{random_id}"),
                                  InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
                follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                                  InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
                follow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

                unfollow_inline = InlineKeyboardMarkup()
                unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"unfollow_{random_id}"),
                                    InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
                unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                                    InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
                unfollow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

                await bot.send_message(message.chat.id, '🏠  Чтобы вернуться на главное меню, воспользуйтесь кнопкой снизу или командой /menu.', parse_mode="html", reply_markup=reply_markups.view_profiles_button)
                
                #  DISPLAY PROFILE
                with open(f"photo/{random_id}.jpg", "rb") as profile_photo:
                    button = unfollow_inline if followers_id is not None else follow_inline
                    await bot.send_photo(message.chat.id, profile_photo, profile_data,
                    parse_mode="html", reply_markup=button)

                    #  VIEWS DATA

                    views_sql.execute(f'SELECT views FROM views_{random_id} WHERE views = ?', (user_id,))
                    views_id = views_sql.fetchone()

                    if views_id is not None:

                        pass

                    else:

                        #  INSERT VIEWS  #

                        views_sql.execute(f'INSERT INTO views_{random_id} (views, username) VALUES (?, ?)', (id_1, username_1))
                        views_db.commit()

            except Exception as e:

                await bot.send_message(message.chat.id, "Профили не найдены ❗️")
                print(e)

        else:

            await bot.send_message(message.chat.id, "Профили не найдены ❗️")









#  NEXT PROFILE

async def next_profile(message):

    main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (message.chat.id,))
    user_id = main_sql.fetchone()[0]

    #  SELECT SETTINGS

    main_sql.execute(f'SELECT gender, city FROM user_settings WHERE id = ?', (user_id,))
    settings = main_sql.fetchone()


    #  ALGORITM

    if settings[1] == "Без разницы":

        if settings[0] == "Без разницы":

            #  CITY = FALSE, GENDER = FALSE

            main_sql.execute('SELECT id FROM user_profile WHERE id != ? ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

        else:

            #  CITY = FALSE, GENDER = TRUE

            main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND gender = "{settings[0]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

    else:

        if settings[0] == "Без разницы":

            #  CITY = TRUE, GENDER = FALSE

            main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND city = "{settings[1]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

        else:

            #  CITY = TRUE, GENDER = TRUE

            main_sql.execute('SELECT id FROM user_profile WHERE id != ? AND gender = ? AND city = ? ORDER BY RANDOM() LIMIT 1', (user_id, settings[0], settings[1]))
            random_id = main_sql.fetchone()

    #  RESULT

    if random_id:
        random_id = random_id[0]

        try:

            #  UPDATE USER ACTION DATA

            main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (random_id, user_id))
            main_sql.execute('UPDATE user_statistics SET views = views + 1 WHERE id = ?', (random_id,))
            main_db.commit()

            #  SELECT IDS

            main_sql.execute('SELECT id_1 FROM user_action WHERE id_1 = ?', (user_id,))
            id_1 = main_sql.fetchone()[0]

            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
            username_1 = main_sql.fetchone()[0]

            #  SELECT USER DATA

            main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (random_id,))
            data = main_sql.fetchone()

            #  SELECT USER FOLLOWERS / FOLLOWS

            followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{random_id}')
            user_followers = followers_sql.fetchone()[0]

            likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{random_id}')
            user_likes = likes_sql.fetchone()[0]

            #  SELECT VERIFICATION

            main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (random_id,))
            user_verification = main_sql.fetchone()[0]

            #  SELECT FOLLOWERS DATA

            followers_sql.execute(f'SELECT followers FROM followers_{random_id} WHERE followers = ?', (user_id,))
            followers_id = followers_sql.fetchone()

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

            #  BUTTONS

            follow_inline = InlineKeyboardMarkup()
            follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"follow_{random_id}"),
                              InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
            follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                              InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
            follow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

            unfollow_inline = InlineKeyboardMarkup()
            unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"unfollow_{random_id}"),
                                InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
            unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                                InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
            unfollow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

            #  DISPLAY PROFILE

            with open(f"photo/{random_id}.jpg", "rb") as profile_photo:
                button = unfollow_inline if followers_id is not None else follow_inline
                await bot.send_photo(message.chat.id, profile_photo, profile_data,
                parse_mode="html", reply_markup=button)

                #  VIEWS DATA

                views_sql.execute(f'SELECT views FROM views_{random_id} WHERE views = ?', (user_id,))
                views_id = views_sql.fetchone()

                if views_id is not None:

                    pass

                else:

                    #  INSERT VIEWS  #

                    views_sql.execute(f'INSERT INTO views_{random_id} (views, username) VALUES (?, ?)', (id_1, username_1))
                    views_db.commit()

        except Exception as e:

            await bot.send_message(message.chat.id, "Профили не найдены ❗️")
            print(e)

    else:

        await bot.send_message(message.chat.id, "Профили не найдены ❗️")













#  VIEW PROFILES (CALL)

async def view_profiles_call(call):

    main_sql.execute('SELECT id FROM user_profile WHERE id = ?', (call.message.chat.id,))
    user_id = main_sql.fetchone()[0]

    #  SELECT SETTINGS

    main_sql.execute(f'SELECT gender, city FROM user_settings WHERE id = ?', (user_id,))
    settings = main_sql.fetchone()


    #  ALGORITM

    if settings[1] == "Без разницы":

        if settings[0] == "Без разницы":

            #  CITY = FALSE, GENDER = FALSE

            main_sql.execute('SELECT id FROM user_profile WHERE id != ? ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

        else:

            #  CITY = FALSE, GENDER = TRUE

            main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND gender = "{settings[0]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

    else:

        if settings[0] == "Без разницы":

            #  CITY = TRUE, GENDER = FALSE

            main_sql.execute(f'SELECT id FROM user_profile WHERE id != ? AND city = "{settings[1]}" ORDER BY RANDOM() LIMIT 1', (user_id,))
            random_id = main_sql.fetchone()

        else:

            #  CITY = TRUE, GENDER = TRUE

            main_sql.execute('SELECT id FROM user_profile WHERE id != ? AND gender = ? AND city = ? ORDER BY RANDOM() LIMIT 1', (user_id, settings[0], settings[1]))
            random_id = main_sql.fetchone()

    #  RESULT

    if random_id:
        random_id = random_id[0]

        try:

            #  UPDATE USER ACTION DATA

            main_sql.execute('UPDATE user_action SET id_2 = ? WHERE id_1 = ?', (random_id, user_id))
            main_sql.execute('UPDATE user_statistics SET views = views + 1 WHERE id = ?', (random_id,))
            main_db.commit()

            #  SELECT IDS

            main_sql.execute('SELECT id_1 FROM user_action WHERE id_1 = ?', (user_id,))
            id_1 = main_sql.fetchone()[0]

            main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
            username_1 = main_sql.fetchone()[0]

            #  SELECT USER DATA

            main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (random_id,))
            data = main_sql.fetchone()

            #  SELECT USER FOLLOWERS / FOLLOWS

            followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{random_id}')
            user_followers = followers_sql.fetchone()[0]

            likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{random_id}')
            user_likes = likes_sql.fetchone()[0]

            #  SELECT VERIFICATION

            main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (random_id,))
            user_verification = main_sql.fetchone()[0]

            #  SELECT FOLLOWERS DATA

            followers_sql.execute(f'SELECT followers FROM followers_{random_id} WHERE followers = ?', (user_id,))
            followers_id = followers_sql.fetchone()

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

            #  BUTTONS

            follow_inline = InlineKeyboardMarkup()
            follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"follow_{random_id}"),
                              InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
            follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                              InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
            follow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

            unfollow_inline = InlineKeyboardMarkup()
            unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"unfollow_{random_id}"),
                                InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{random_id}"))
            unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{random_id}"),
                                InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{random_id}"))
            unfollow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

            #  DISPLAY PROFILE

            with open(f"photo/{random_id}.jpg", "rb") as profile_photo:
                button = unfollow_inline if followers_id is not None else follow_inline
                await bot.send_photo(call.message.chat.id, profile_photo, profile_data,
                parse_mode="html", reply_markup = button)

                #  VIEWS DATA

                views_sql.execute(f'SELECT views FROM views_{random_id} WHERE views = ?', (user_id,))
                views_id = views_sql.fetchone()

                if views_id is not None:

                    pass

                else:

                    #  INSERT VIEWS  #

                    views_sql.execute(f'INSERT INTO views_{random_id} (views, username) VALUES (?, ?)', (id_1, username_1))
                    views_db.commit()

        except Exception as e:

            await bot.send_message(call.message.chat.id, "Профили не найдены ❗️")
            print(e)

    else:

        await bot.send_message(call.message.chat.id, "Профили не найдены ❗️")






