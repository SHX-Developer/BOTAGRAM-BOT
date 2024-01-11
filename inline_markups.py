from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton




#  REG GENDER

reg_gender_inline = InlineKeyboardMarkup()
reg_gender_inline.row(InlineKeyboardButton(text="Парней", callback_data="reg_male_gender"),
                      InlineKeyboardButton(text="Девушек", callback_data="reg_female_gender"))
reg_gender_inline.row(InlineKeyboardButton(text="Без разницы", callback_data="reg_random_gender"))



#  PROFILE

new_profile_inline = InlineKeyboardMarkup()
new_profile_inline.row(InlineKeyboardButton(text="⚙️  Настройки профиля", callback_data="profile_settings"))

profile_inline_1 = InlineKeyboardMarkup()
profile_inline_1.row(InlineKeyboardButton(text="⚙️  Настройки профиля", callback_data="profile_settings"))
profile_inline_1.row(InlineKeyboardButton(text="📊  Статистика профиля", callback_data="statistics"))
profile_inline_1.row(InlineKeyboardButton(text="☑️  Верификация", callback_data="verification"))

profile_inline_2 = InlineKeyboardMarkup()
profile_inline_2.row(InlineKeyboardButton(text="⚙️  Настройки профиля", callback_data="profile_settings"))
profile_inline_2.row(InlineKeyboardButton(text="📊  Статистика профиля", callback_data="statistics"))



#  PROFILE SETTINGS
profile_settings_inline = InlineKeyboardMarkup()
profile_settings_inline.row(InlineKeyboardButton(text="🖼  Фото", callback_data="edit_photo"),
                            InlineKeyboardButton(text="👤  Юзернейм", callback_data="edit_username"))
profile_settings_inline.row(InlineKeyboardButton(text="🪪  Имя", callback_data="edit_firstname"),
                            InlineKeyboardButton(text="🔞  Возраст", callback_data="edit_age"))
profile_settings_inline.row(InlineKeyboardButton(text="🏙️  Город", callback_data="edit_city"),
                            InlineKeyboardButton(text="👫  Пол", callback_data="edit_gender"))
profile_settings_inline.row(InlineKeyboardButton(text="👩‍❤️‍👨  Статус", callback_data="edit_status"),
                            InlineKeyboardButton(text="💬  О себе", callback_data="edit_bio"))
profile_settings_inline.row(InlineKeyboardButton(text="🔙  Назад", callback_data="back_to_profile"))



#  STATUS

#  MALE
male_status_inline = InlineKeyboardMarkup()
male_status_inline.row(InlineKeyboardButton(text="Свободен", callback_data="single"),
                       InlineKeyboardButton(text="В отношениях", callback_data="relationship"))
male_status_inline.row(InlineKeyboardButton(text="Женат", callback_data="married"),
                       InlineKeyboardButton(text="В разводе", callback_data="engaged"))
male_status_inline.row(InlineKeyboardButton(text="В активном поиске", callback_data="actively_searching"))
male_status_inline.row(InlineKeyboardButton(text="🗑  Очистить", callback_data="clear_status"))

#  FEMALE
female_status_inline = InlineKeyboardMarkup()
female_status_inline.row(InlineKeyboardButton(text="Свободна", callback_data="single"),
                         InlineKeyboardButton(text="В отношениях", callback_data="relationship"))
female_status_inline.row(InlineKeyboardButton(text="Замужем", callback_data="married"),
                         InlineKeyboardButton(text="В разводе", callback_data="engaged"))
female_status_inline.row(InlineKeyboardButton(text="В активном поиске", callback_data="actively_searching"))
female_status_inline.row(InlineKeyboardButton(text="🗑  Очистить", callback_data="clear_status"))

#  OTHER
unknown_status_inline = InlineKeyboardMarkup()
unknown_status_inline.row(InlineKeyboardButton(text="Свободен(на)", callback_data="single"),
                          InlineKeyboardButton(text="В отношениях", callback_data="relationship"))
unknown_status_inline.row(InlineKeyboardButton(text="Женат / Замужем", callback_data="married"),
                          InlineKeyboardButton(text="В разводе", callback_data="engaged"))
unknown_status_inline.row(InlineKeyboardButton(text="В активном поиске", callback_data="actively_searching"))
unknown_status_inline.row(InlineKeyboardButton(text="🗑  Очистить", callback_data="clear_status"))




#  STATISTICS
statistics_inline = InlineKeyboardMarkup()
statistics_inline.row(InlineKeyboardButton(text="👀  Просмотры профиля", callback_data="my_views"))
statistics_inline.row(InlineKeyboardButton(text="👥  Подписчики", callback_data="my_followers"),
                      InlineKeyboardButton(text="🫂  Подписки", callback_data="my_follows"))
statistics_inline.row(InlineKeyboardButton(text="❤️  Лайки", callback_data="my_likes"),
                      InlineKeyboardButton(text="💔  Дизлайки", callback_data="my_dislikes"))
statistics_inline.row(InlineKeyboardButton(text="🔙  Назад", callback_data="back_to_profile"))



#  SETTINGS
settings_inline_1 = InlineKeyboardMarkup()
settings_inline_1.row(InlineKeyboardButton(text="👫  Изменить пол", callback_data="set_gender"))
settings_inline_1.row(InlineKeyboardButton(text="🏙️  Изменить город", callback_data="set_city"))
settings_inline_1.row(InlineKeyboardButton(text="☑️  Верификация", callback_data="verification"))

settings_inline_2 = InlineKeyboardMarkup()
settings_inline_2.row(InlineKeyboardButton(text="👫  Изменить пол", callback_data="set_gender"))
settings_inline_2.row(InlineKeyboardButton(text="🏙️  Изменить город", callback_data="set_city"))

#  GENDER
set_gender_inline = InlineKeyboardMarkup()
set_gender_inline.row(InlineKeyboardButton(text="🙋‍♂️  Парней", callback_data="set_male_gender"),
                      InlineKeyboardButton(text="🙋‍♀️  Девушек", callback_data="set_female_gender"))
set_gender_inline.row(InlineKeyboardButton(text="👻  Без разницы", callback_data="set_random_gender"))





#  PUBLIC CHAT

join_chat_inline_1 = InlineKeyboardMarkup()
join_chat_inline_1.row(InlineKeyboardButton(text="Посмотреть пользователей", callback_data="view_chat_users"))
join_chat_inline_1.row(InlineKeyboardButton(text="Присоединиться", callback_data="join_chat"))

join_chat_inline_2 = InlineKeyboardMarkup()
join_chat_inline_2.row(InlineKeyboardButton(text="Присоединиться", callback_data="join_chat"))

send_hello_inline = InlineKeyboardMarkup()
send_hello_inline.row(InlineKeyboardButton(text="👋  Поздароваться", callback_data="send_hello"))
send_hello_inline.row(InlineKeyboardButton(text="Скрыть сообщение", callback_data="hide_message"))



#  ANONYM CHAT

anonym_chat_inline = InlineKeyboardMarkup()
anonym_chat_inline.row(InlineKeyboardButton(text = "🔍  Поиск собеседника", callback_data="search_anonym_user"))




#  VERIFICATION
verification_inline = InlineKeyboardMarkup()
verification_inline.row(InlineKeyboardButton(text="☑️  Подать заявку", callback_data="send_verification"))
verification_inline.row(InlineKeyboardButton(text="❌  Скрыть сообщение", callback_data="hide_message"))




#  HIDE MESSAGE
hide_inline = InlineKeyboardMarkup()
hide_inline.row(InlineKeyboardButton(text="Скрыть сообщение", callback_data="hide_message"))



#  MESSAGES
hint_messages_inline = InlineKeyboardMarkup()
hint_messages_inline.row(InlineKeyboardButton(text="Привет !", callback_data="message_1"))
hint_messages_inline.row(InlineKeyboardButton(text="Познакомимся ?", callback_data="message_2"))
hint_messages_inline.row(InlineKeyboardButton(text="Написать своё сообщение", callback_data="message_3"))






#  ADMIN MENU
admin_statistics_inline = InlineKeyboardMarkup()
admin_statistics_inline.row(InlineKeyboardButton(text="Показать пользователей", callback_data="show_all_users"))
admin_statistics_inline.row(InlineKeyboardButton(text="Верифицированные пользователи", callback_data="show_verified_users"))
admin_statistics_inline.row(InlineKeyboardButton(text="Пользователи с фото в профиле", callback_data="show_photo_users"))

#  DELETE CHAT MESSAGE
delete_chat_message_inline = InlineKeyboardMarkup()
delete_chat_message_inline.row(InlineKeyboardButton(text="❌  Удалить сообщение", callback_data="delete_chat_message"))





#  DELETE CHAT MESSAGE
cancel_inline = InlineKeyboardMarkup()
cancel_inline.row(InlineKeyboardButton(text="Отменить", callback_data="cancel"))





















