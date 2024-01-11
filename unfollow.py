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




async def unfollow_profile(call):

    #  SELECTING ACTION DATA
    main_sql.execute('SELECT id_1, id_2 FROM user_action WHERE id_1 = ?', (call.message.chat.id,))
    data = main_sql.fetchone()
    id_1 = data[0]
    id_2 = data[1]

    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_1,))
    username_1 = main_sql.fetchone()[0]
    main_sql.execute('SELECT username FROM user_profile WHERE id = ?', (id_2,))
    username_2 = main_sql.fetchone()[0]

    #  DELETE FOLLOWERS / FOLLOWS
    followers_sql.execute(f'DELETE FROM followers_{id_2} WHERE followers = ?', (id_1,))
    followers_db.commit()
    follows_sql.execute(f'DELETE FROM follows_{id_1} WHERE follows =  ?', (id_2,))
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
    main_sql.execute(f'UPDATE user_statistics SET followers = followers - 1 WHERE id = ?', (id_2,))
    main_sql.execute(f'UPDATE user_statistics SET follows = follows - 1 WHERE id = ?', (id_1,))
    main_db.commit()

    #  VERIFICATION
    main_sql.execute(f'SELECT verification FROM user_verification WHERE id = ?', (id_2,))
    found_user_verification = main_sql.fetchone()[0]

    #  BUTTONS
    follow_inline = InlineKeyboardMarkup()
    follow_inline.row(InlineKeyboardButton(text="➕ Подписаться", callback_data=f"follow_{id_2}"),
                      InlineKeyboardButton(text="💌  Написать", callback_data=f"message_{id_2}"))
    follow_inline.row(InlineKeyboardButton(text="❤️  Лайк", callback_data=f"like_{id_2}"),
                      InlineKeyboardButton(text="💔  Дизлайк", callback_data=f"dislike_{id_2}"))
    follow_inline.row(InlineKeyboardButton(text="🚀  Следующий профиль", callback_data="next_profile"))
    
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

    await bot.send_message(id_1, f'❌  Вы отписались от пользователя  <code>{username_2}</code>', parse_mode="html", reply_markup=inline_markups.hide_inline)

    #  WRITE TO FILE
    with open("actions/unfollows.txt", "a+") as unfollow_file:
        unfollow_file.write(f"[{date_time}]:  {username_1}  -  {username_2}\n\n")
        unfollow_file.close()







