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










#  REPLY MESSAGE

async def reply_message(message):

    #  CHAT STATUS
    main_sql.execute(f'SELECT status FROM user_chat WHERE id = {message.chat.id}')
    user_chat_status = main_sql.fetchone()[0]

    #  SELECTING DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  INLINE BUTTON
    reply_inline = InlineKeyboardMarkup()
    reply_inline.row(InlineKeyboardButton("👤  Посмотреть профиль", callback_data=f"profile_{id_1}"))
    reply_inline.row(types.InlineKeyboardButton("💌  Ответить", callback_data=f"replymessage_{id_1}"))

    #  SEND MESSAGE
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





#  FOLLOW

async def follow_profile(call):

    #  SELECTING IDS
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAMES
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    main_sql.execute('SELECT gender FROM user_profile WHERE id = ?', (id_1,))
    user_gender = main_sql.fetchone()[0]

    #  SELECTING DATA
    main_sql.execute('SELECT * FROM user_profile WHERE id = ?', (id_2,))
    data = main_sql.fetchone()

    #  UPDATE STATISTICS
    main_sql.execute('UPDATE user_statistics SET followers = followers + 1 WHERE id = ?', (id_2,))
    main_sql.execute(f'UPDATE user_statistics SET follows = follows + 1 WHERE id = ?', (id_1,))
    main_db.commit()

    #  INSERT FOLLOWERS
    followers_sql.execute(f'INSERT INTO followers_{id_2} (followers, username) VALUES (?, ?)', (id_1, username_1))
    followers_db.commit()
    follows_sql.execute(f'INSERT INTO follows_{id_1} (follows, username) VALUES (?, ?)', (id_2, username_2))
    follows_db.commit()

    #  FOLLOWERS / LIKES
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
    found_user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}')
    found_user_likes = likes_sql.fetchone()[0]

    #  VERIFICATION
    main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (id_2,))
    found_user_verification = main_sql.fetchone()[0]

    #  BUTTONS
    unfollow_inline = InlineKeyboardMarkup()
    unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"replyunfollow_{id_2}"),
                        InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
    unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                        InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))

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

    #  DISPLAY PROFILE
    with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
        await bot.edit_message_media(
            media = types.InputMedia(
            type = 'photo',
            media = profile_photo,
            caption = profile_data,
            parse_mode = "html"),
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            reply_markup = unfollow_inline)

    #  SEND MESSAGE
    await bot.send_message(id_1, f'✅  Вы подписались к пользователю  <code>{username_2}</code>', parse_mode="html", reply_markup=inline_markups.hide_inline)

    #  WRITE TO FILE
    with open("actions/follows.txt", "a+") as follow_file:
        follow_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
        follow_file.close()

    #  INLINE BUTTON
    follow_inline = InlineKeyboardMarkup()
    follow_inline.row(InlineKeyboardButton("👤  Посмотреть профиль", callback_data=f"profile_{id_1}"))
    
    try:
        if user_gender == "Парень":
            await bot.send_message(id_2, f'🎉  У вас новый подписчик\n\n✅  На вас подписался  <code>{username_1}</code>', parse_mode = "html", reply_markup = follow_inline)

        elif user_gender == "Девушка":
            await bot.send_message(id_2, f'🎉  У вас новый подписчик\n\n✅  На вас подписалась  <code>{username_1}</code>', parse_mode = "html", reply_markup = follow_inline)

        elif user_gender == "Другое":
            await bot.send_message(id_2, f'🎉  У вас новый подписчик\n\n✅  На вас подписалось  <code>{username_1}</code>', parse_mode = "html", reply_markup = follow_inline)

        elif user_gender == "-":
            await bot.send_message(id_2, f'🎉  У вас новый подписчик\n\n✅  На вас подписался(ась)  <code>{username_1}</code>', parse_mode = "html", reply_markup = follow_inline)

    except Exception as e:
        await bot.send_message(284929331, f"Произошла ошибка при отправке сообщения - {username_2}\n\nОшибка - {e}")





#  UNFOLLOW

async def unfollow_profile(call):

    #  SELECTING IDS
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAMES
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  DELETE FOLLOWERS
    followers_sql.execute(f'DELETE FROM followers_{id_2} WHERE followers = ?', (id_1,))
    followers_db.commit()
    follows_sql.execute(f'DELETE FROM follows_{id_1} WHERE follows = ?', (id_2,))
    follows_db.commit()

    #  SELECTING DATA
    main_sql.execute(f'SELECT * FROM user_profile WHERE id = ?', (id_2,))
    data = main_sql.fetchone()

    #  FOLLOWERS / LIKES
    followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
    found_user_followers = followers_sql.fetchone()[0]
    likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}')
    found_user_likes = likes_sql.fetchone()[0]

    #  UPDATE STATISTICS
    main_sql.execute('UPDATE user_statistics SET followers = followers - 1 WHERE id = ?', (id_2,))
    main_sql.execute('UPDATE user_statistics SET follows = follows - 1 WHERE id = ?', (id_1,))
    main_db.commit()

    #  VERIFICATION
    main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (id_2,))
    found_user_verification = main_sql.fetchone()[0]

    #  BUTTONS
    follow_inline = InlineKeyboardMarkup()
    follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"replyfollow_{id_2}"),
                      InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
    follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                      InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))

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

    #  DISPLAY PROFILE
    with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
        await bot.edit_message_media(
            media = types.InputMedia(
            type = 'photo',
            media = profile_photo,
            caption = profile_data,
            parse_mode = "html"),
            chat_id = call.message.chat.id,
            message_id = call.message.message_id,
            reply_markup = follow_inline)
    
    #  SEND MESSAGE
    await bot.send_message(id_1, f'❌  Вы отписались от пользователя  <code>{username_2}</code>', parse_mode="html", reply_markup=inline_markups.hide_inline)

    #  WRITE TO FILE
    with open("actions/unfollows.txt", "a+") as unfollow_file:
        unfollow_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
        unfollow_file.close()





#  LIKE

async def like_profile(call):

    #  SELECTING IDS
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAMES
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    main_sql.execute('SELECT gender FROM user_profile WHERE id = ?', (id_1,))
    user_gender = main_sql.fetchone()[0]

    #  LINKS
    main_sql.execute('SELECT username FROM user_access WHERE id = ?', (id_1,))
    user_link_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_access WHERE id = ?', (id_2,))
    user_link_2 = main_sql.fetchone()[0]

    #  CHECK LIKE
    likes_sql.execute(f'SELECT likes FROM likes_{id_2} WHERE likes = ?', (id_1,))
    in_likes = likes_sql.fetchone()

    if in_likes is not None:
        await bot.send_message(id_1, f"Вы уже ставили <b>лайк</b> пользователю  <code>{username_2}</code> ❗️", parse_mode="html", reply_markup=inline_markups.hide_inline)

    else:
        #  INSERT DATA
        likes_sql.execute(f'INSERT INTO likes_{id_2} (likes, username) VALUES (?, ?)', (id_1, username_1))
        likes_db.commit()
        main_sql.execute(f'UPDATE user_statistics SET likes = likes + 1 WHERE id = ?', (id_2,))
        main_db.commit()

        #  SELECTING DATA
        main_sql.execute(f'SELECT * FROM user_profile WHERE id = ?', (id_2,))
        data = main_sql.fetchone()

        #  USER FOLLOWERS / FOLLOWS
        followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
        user_followers = followers_sql.fetchone()[0]
        likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}''')
        user_likes = likes_sql.fetchone()[0]

        #  VERIFICATION
        main_sql.execute('SELECT verification FROM user_verification WHERE id = ?', (id_2,))
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
        follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"replyfollow_{id_2}"),
                          InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
        follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                          InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))
        
        unfollow_inline = InlineKeyboardMarkup()
        unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"replyunfollow_{id_2}"),
                            InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
        unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                            InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))

        #  DISPLAY PROFILE
        with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
            button = unfollow_inline if followers_id is not None else follow_inline
            await bot.edit_message_media(
                media = types.InputMedia(
                type = 'photo',
                media = profile_photo,
                caption = profile_data,
                parse_mode = "html"),
                chat_id = call.message.chat.id,
                message_id = call.message.message_id,
                reply_markup = button)

        #  SELECT LIKES
        likes_sql.execute(f'SELECT likes FROM likes_{id_1} WHERE likes = ?', (id_2,))
        in_my_likes = likes_sql.fetchone()

        if in_my_likes is not None:

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





#  DISLIKE

async def dislike_profile(call):

    #  SELECTING IDS
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    #  USERNAMES
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  CHECK ID
    dislikes_sql.execute(f'SELECT dislikes FROM dislikes_{id_2} WHERE dislikes = ?', (call.message.chat.id,))
    dislikes_id = dislikes_sql.fetchone()

    #  CHECK DISLIKES
    if dislikes_id is not None:
        await bot.send_message(id_1, f"Вы уже ставили <b>дизлайк</b> пользователю  <code>{username_2}</code> ❗️", parse_mode="html", reply_markup=inline_markups.hide_inline)
        
    else:
        #  INSERT DATA
        dislikes_sql.execute(f'INSERT INTO dislikes_{id_2} (dislikes, username) VALUES (?, ?)', (id_1, username_1))
        dislikes_db.commit()
        main_sql.execute('UPDATE user_statistics SET dislikes = dislikes + 1 WHERE id = ?', (id_2,))
        main_db.commit()

        await bot.send_message(id_1, f"💔  Вы поставили <b>дизлайк</b> пользователю  <code>{username_2}</code>", parse_mode="html", reply_markup=inline_markups.hide_inline)
        
        #  WRITE TO FILE
        with open("actions/dislikes.txt", "a+") as dislike_file:
            dislike_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
            dislike_file.close()









#  PROFILE

async def reply_profile(call):

    try:
        #  USER ACTION DATA
        main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
        data = main_sql.fetchone()
        id_1 = data[0]
        id_2 = data[1]

        main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
        username_1 = main_sql.fetchone()[0]

        #  SELECTING DATA
        main_sql.execute(f'SELECT * FROM user_profile WHERE id = ?', (id_2,))
        data = main_sql.fetchone()

        #  FOLLOWERS
        followers_sql.execute(f'SELECT COUNT(followers) FROM followers_{id_2}')
        found_user_followers = followers_sql.fetchone()[0]
        likes_sql.execute(f'SELECT COUNT(likes) FROM likes_{id_2}')
        found_user_likes = likes_sql.fetchone()[0]

        #  FOLLOWERS DATA
        followers_sql.execute(f'SELECT followers FROM followers_{id_2} WHERE followers = ?', (id_1,))
        followers_id = followers_sql.fetchone()

        #  VERIFICATION
        main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (id_2,))
        user_verification = main_sql.fetchone()[0]

        #  UPDATE VIEWS
        main_sql.execute(f'UPDATE user_statistics SET views = views + 1 WHERE id = ?', (id_2,))
        main_db.commit()

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
        f"\n\n👥  <b>Подписчиков:</b>  {found_user_followers}"
        f"\n❤️  <b>Лайков:</b>  {found_user_likes}")

        #  BUTTONS
        follow_inline = InlineKeyboardMarkup()
        follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"replyfollow_{id_2}"),
                          InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
        follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                          InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))

        unfollow_inline = InlineKeyboardMarkup()
        unfollow_inline.row(InlineKeyboardButton(text="➖  Отписаться", callback_data=f"replyunfollow_{id_2}"),
                            InlineKeyboardButton(text="💌  Написать", callback_data=f"replymessage_{id_2}"))
        unfollow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"replylike_{id_2}"),
                            InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"replydislike_{id_2}"))

        #  DISPLAY PROFILE
        with open(f"photo/{id_2}.jpg", "rb") as profile_photo:
            button = unfollow_inline if followers_id is not None else follow_inline
            await bot.send_photo(
                chat_id = call.message.chat.id, 
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
                views_sql.execute(f'INSERT INTO views_{id_2} (views, username) VALUES (?, ?)', (id_1, username_1))
                views_db.commit()

    except:
        await bot.send_message(call.message.chat.id, "Профили не найдены ❗")






#  SEND GREETING

async def send_greeting(call):

    #  SELECT USERS IN "CHAT"
    main_sql.execute('SELECT * FROM user_chat WHERE id != ? AND status = ?', (call.message.chat.id, "Yes"))
    data = main_sql.fetchall()

    main_sql.execute('SELECT id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    id_2 = main_sql.fetchone()[0]

    main_sql.execute('SELECT username FROM user_chat WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    main_sql.execute('SELECT status FROM user_chat WHERE id = ?', (id_2,))
    user_status = main_sql.fetchone()[0]

    if user_status == "Yes":
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.send_message(call.message.chat.id, f"✅  Вы поприветствовали  <code>{username_2}</code>", parse_mode = "html")

        for row in data:
            
            try:
                main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (call.message.chat.id,))
                user_username = main_sql.fetchone()[0]

                await bot.send_message(row[0], f"<code>{user_username}</code>\n\n<b>Привет  <code>{username_2}</code>  !</b>", parse_mode = "html")
            
            except:
                pass

    else:
        await bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
        await bot.send_message(call.message.chat.id, f"❗️ <code>{username_2}</code>  не находится в чате.", parse_mode = "html")








#  DELETE MESSAGES
async def delete_message(message):
    try:
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        await bot.delete_message(chat_id = message.chat.id, message_id = message.message_id - 1)
    except:
        pass




