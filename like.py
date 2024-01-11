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





#  LIKE

async def like_profile(call):

    #  SELECTING DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  LINKS
    main_sql.execute('SELECT username FROM user_access WHERE id = ?', (id_1,))
    user_link_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_access WHERE id = ?', (id_2,))
    user_link_2 = main_sql.fetchone()[0]

    main_sql.execute('SELECT gender FROM user_profile WHERE id = ?', (id_1,))
    user_gender = main_sql.fetchone()[0]

    #  CHECK LIKE
    likes_sql.execute(f'SELECT likes FROM likes_{id_2} WHERE likes = ?', (id_1,))
    likes_id = likes_sql.fetchone()

    if likes_id is not None:
        bot.send_message(id_1, f"Вы уже ставили <b>лайк</b> пользователю  <code>{username_2}</code> ❗️", parse_mode="html", reply_markup=inline_markups.hide_inline)
    else:
        likes_sql.execute(f'''INSERT INTO likes_{id_2} (likes, username) VALUES ("{id_1}", "{username_1}")''')
        likes_db.commit()
        main_sql.execute(f'''UPDATE user_statistics SET likes = likes + 1 WHERE id = "{id_2}"''')
        main_db.commit()

        #  SELECTING DATA
        main_sql.execute(f'SELECT * FROM user_profile WHERE id = ?', (id_2,))
        data = main_sql.fetchone()

        #  FOLLOWERS / LIKES
        followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
        user_followers = followers_sql.fetchone()[0]
        likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}''')
        user_likes = likes_sql.fetchone()[0]
        
        #  VERIFICATION
        main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (id_2,))
        user_verification = main_sql.fetchone()[0]

        #  FOLLOWERS DATA
        followers_sql.execute(f'SELECT followers FROM followers_{id_2} WHERE followers = ?', (id_1,))
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
        follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"follow_{id_2}"),
                          InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{id_2}"))
        follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{id_2}"),
                          InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{id_2}"))
        follow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))
        
        unfollow_inline = InlineKeyboardMarkup()
        unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"unfollow_{id_2}"),
                            InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{id_2}"))
        unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{id_2}"),
                            InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{id_2}"))
        unfollow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))

        #  DISPLAY PROFILE
        with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
            button = unfollow_inline if followers_id is not None else follow_inline
            await bot.edit_message_media(
                media = types.InputMedia(
                type='photo',
                media = profile_photo,
                caption = profile_data,
                parse_mode = "html"),
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                reply_markup = button)

        likes_sql.execute(f'SELECT likes FROM likes_{id_1} WHERE likes = ?', (id_2,))
        in_likes = likes_sql.fetchone()

        if in_likes is not None:

            #  LINK BUTTONS
            user_button_1 = InlineKeyboardMarkup()
            user_button_1.row(InlineKeyboardButton(text="💌  Написать", url=f"https://t.me/{user_link_1}"))

            user_button_2 = InlineKeyboardMarkup()
            user_button_2.row(InlineKeyboardButton(text="💌  Написать", url=f"https://t.me/{user_link_2}"))

            #  SEND MESSAGE
            await bot.send_message(id_1, f'💞  Есть взаимная симпатия\n\n✨  У вас взаимная симпатия с пользователем  <code>{username_2}</code>', parse_mode="html", reply_markup=user_button_2)
            
            #  WRITE TO FILE
            with open("actions/sympathies.txt", "a+") as sympathy_file:
                sympathy_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
                sympathy_file.close()

            try:
                await bot.send_message(id_2, f'💞  Есть взаимная симпатия\n\n✨  У вас взаимная симпатия с пользователем  <code>{username_1}</code>', parse_mode="html", reply_markup=user_button_1)
            except Exception as e:
                await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")
        
        else:
            await bot.send_message(id_1, f"❤️  Вы поставили <b>лайк</b> пользователю  <code>{username_2}</code>", parse_mode="html", reply_markup=inline_markups.hide_inline)
            
            #  WRITE TO FILE
            with open("actions/likes.txt", "a+") as like_file:
                like_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
                like_file.close()

            #  INLINE BUTTON
            like_inline = InlineKeyboardMarkup()
            like_inline.row(InlineKeyboardButton("👤  Посмотреть профиль", callback_data=f"profile_{id_1}"))

            #  SEND MESSAGE
            try:
                if user_gender == "Парень":
                    await bot.send_message(id_2, f'❤️  Кому то понравился ваш профиль\n\n✅  Ваш профиль оценил пользователь  <code>{username_1}</code>', parse_mode="html", reply_markup=like_inline)
                
                elif user_gender == "Девушка":
                    await bot.send_message(id_2, f'❤️  Кому то понравился ваш профиль\n\n✅  Ваш профиль оценила пользователь  <code>{username_1}</code>', parse_mode="html", reply_markup=like_inline)
                
                elif user_gender == "Другое":
                    await bot.send_message(id_2, f'❤️  Кому то понравился ваш профиль\n\n✅  Ваш профиль оценил(а) пользователь  <code>{username_1}</code>', parse_mode="html", reply_markup=like_inline)
                
                elif user_gender == "-":
                    await bot.send_message(id_2, f'❤️  Кому то понравился ваш профиль\n\n✅  Ваш профиль оценил(а) пользователь  <code>{username_1}</code>', parse_mode="html", reply_markup=like_inline)

            except Exception as e:
                await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")


