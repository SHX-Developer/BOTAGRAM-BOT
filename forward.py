import telebot
import sqlite3
import datetime

import config

import inline_markups
import reply_markups


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

bot = telebot.TeleBot(config.token)

date_time = datetime.datetime.now().date()






#  TEXT

def forward_message(message):

    if message.text == "❌  Отмена  ❌":

        bot.send_message(message.chat.id, '❌  Отменено  ❌', parse_mode="html", reply_markup=reply_markups.forward_button)

    else:

        bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html", reply_markup=reply_markups.forward_button)

        main_sql.execute('SELECT id FROM user_profile')
        data = main_sql.fetchall()

        main_sql.execute('SELECT COUNT(id) FROM user_profile')
        all_users = main_sql.fetchone()[0]

        total = 0

        for users in data:

            try:

                bot.send_message(users[0], message.text, parse_mode="html", reply_markup=None)

                total += 1

                print(f"[{users[0]}]: получил сообщение  ✅")

            except Exception:

                print(f"[{users[0]}]: заблокировал бота  ❌")

        else:

            blocked_users = all_users - total

            bot.send_message(message.chat.id, f"<b>✅  Ваше сообщение успешно отправлено:  {total}  пользователям из:  {all_users}   </b>", parse_mode="html", reply_markup=None)
            bot.send_message(message.chat.id, f"<b>❌  Заблокировавшие пользователи:  {blocked_users} </b>", parse_mode="html", reply_markup=None)





#  UPDATE

def forward_update(message):

    bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html")

    main_sql.execute('SELECT id FROM user_profile')
    data = main_sql.fetchall()

    main_sql.execute('SELECT COUNT(id) FROM user_profile')
    all_users = main_sql.fetchone()[0]

    total = 0

    for users in data:

        try:

            bot.send_message(users[0],  '<b>🎉 Новое обновление - BOTAGRAM v9 🎉</b>'
                                        '\n\n\n🏙  Добавлен новый алгоритм <b>"ПОИСК ПО ГОРОДУ"</b>, теперь пользователи могут изменить <b>"ПРЕДПОЧИТАЕМЫЙ ГОРОД"</b> в разделе <b>"НАСТРОЙКИ"</b>.'
                                        '\n\n❤️  Добавлен автоматический переход на следующий профиль после нажатия на <b>"ЛАЙК"</b> или <b>"ДИЗЛАЙК"</b>.'
                                        '\n\n🌐  Добавлены новые функции в <b>"ЧАТ"</b>, теперь в чате можно делиться <b>(Голосовыми сообщениями, Стикерами, Фотографиями, Видео и Аудио)</b>.'
                                        '\n\n⚙️  Добавлены новые функции в <b>"НАСТРОЙКИ"</b>, теперь можно менять и удалять <b>("ПРЕДПОЧИТАЕМЫЙ ("ПОЛ" и "ГОРОД")"</b>, а так же добавлен новый раздел <b>"ВЕРИФИКАЦИЯ"</b>.'
                                        '\n\n🛠 Исправлены баги в функции <b>"ПОКИНУТЬ ЧАТ"</b>.'
                                        '\n\n⚖️  Оптимизация функции <b>"Смотреть профили"</b>.'
                                        '\n\n❗️ Добавлены правила в <b>"ЧАТЕ"</b>, теперь пользователям нужно стараться избегать такие темы как <b>"ПОЛИТИКА", "ПРОПАГАНДА ("РЕЛИГИИ" & "НАЦИЗМА")</b>.'
                                        '\n\n❌  <i>За нарушение правил, пользователь может быть исключен из чата или вовсе заблокирован в боте</i>.'
                                        '\n\n\n<b>Всем искренне приносим благодарности за вашу активность и тестирование бота  ❤️‍🔥</b>'
                                        '\n\n<b><i>После одного обновления, официально выкладываем бота на публику с версией - BOTAGRAM 1.0  🥳</i></b>',
                                        parse_mode="html", reply_markup=None)

            total += 1

            print(f"[{users[0]}]: получил сообщение  ✅")

        except Exception:

            print(f"[{users[0]}]: заблокировал бота  ❌")

    else:

        blocked_users = all_users - total

        bot.send_message(message.chat.id, f"<b>✅  Ваше сообщение успешно отправлено:  {total}  пользователям из:  {all_users}   </b>", parse_mode="html", reply_markup=None)
        bot.send_message(message.chat.id, f"<b>❌  Заблокировавшие пользователи:  {blocked_users} </b>", parse_mode="html", reply_markup=None)






#  CHAT

def forward_chat(message):

    bot.send_message(message.chat.id, "<b> Рассылка началась  ✅ </b>", parse_mode="html")

    main_sql.execute("SELECT id FROM user_profile")
    data = main_sql.fetchall()

    main_sql.execute("SELECT COUNT(id) FROM user_profile")
    all_users = main_sql.fetchone()[0]

    main_sql.execute('SELECT COUNT(id) FROM user_chat WHERE status = ?', ("Yes",))
    chat_users = main_sql.fetchone()[0]

    total = 0

    for users in data:

        try:

            bot.send_message(users[0], f"<b>👋  Доброго времени суток !</b>\n\n😍  Хотим пригласить вас в наш чат для общения и знакомства с пользователями бота.\n\n<i>Пользователей в чате:  <b>13</b></i>", parse_mode="html", reply_markup=inline_markups.join_chat_inline_2)

            total += 1

            print(f"[{users[0]}]: получил сообщение  ✅")

        except:

            print(f"[{users[0]}]: заблокировал бота  ❌")

    else:

        blocked_users = all_users - total

        bot.send_message(message.chat.id, f"<b>✅  Ваше сообщение успешно отправлено:  {total}  пользователям из:  {all_users}   </b>", parse_mode="html", reply_markup=None)
        bot.send_message(message.chat.id, f"<b>❌  Заблокировавшие пользователи:  {blocked_users} </b>", parse_mode="html", reply_markup=None)























