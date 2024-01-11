from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove



#  REGISTER GENDER
reg_gender_reply = ReplyKeyboardMarkup(resize_keyboard = True)
reg_gender_reply.row("🙋‍♂️  Парней", "🙋‍♀️  Девушек")
reg_gender_reply.row("👻  Без разницы")



#  MENU

menu_button = ReplyKeyboardMarkup(resize_keyboard = True)
menu_button.row("🚀  Смотреть профили")
menu_button.row("💌  Написать",  "🌐  Чат",  "🔍  Поиск")
menu_button.row("🏆  Фавориты", "⚙️  Настройки")
menu_button.row("👤  Профиль")



#  VIEW PROFILES


view_profiles_button = ReplyKeyboardMarkup(resize_keyboard = True)
view_profiles_button.row("🏠  Главное меню")


#  CHAT

chat_button = ReplyKeyboardMarkup(resize_keyboard = True)
chat_button.row("🎭  Публичный чат", "👻  Анонимный чат")
chat_button.row("🏠  Главное меню")








#  EDIT GENDER

edit_gender_reply = ReplyKeyboardMarkup(resize_keyboard = True)
edit_gender_reply.row('🙋‍♂️  Парень', '🙋‍♀️  Девушка')
edit_gender_reply.row('👻  Другое')
edit_gender_reply.row('❌  Отмена  ❌')

#  EDIT STATUS

male_edit_status_reply = ReplyKeyboardMarkup(resize_keyboard = True)
male_edit_status_reply.row('Свободен', 'В отношениях')
male_edit_status_reply.row('Женат', 'В разводе')
male_edit_status_reply.row('В активном поиске')
male_edit_status_reply.row('❌  Отмена  ❌')

female_edit_status_reply = ReplyKeyboardMarkup(resize_keyboard = True)
female_edit_status_reply.row('Свободна', 'В отношениях')
female_edit_status_reply.row('Замужем', 'В разводе')
female_edit_status_reply.row('В активном поиске')
female_edit_status_reply.row('❌  Отмена  ❌')

edit_status_reply = ReplyKeyboardMarkup(resize_keyboard = True)
edit_status_reply.row('Свободен(на)', 'В отношениях')
edit_status_reply.row('Женат / Замужем', 'В разводе')
edit_status_reply.row('В активном поиске')
edit_status_reply.row('❌  Отмена  ❌')


#  SETTINGS

gender_settings_reply = ReplyKeyboardMarkup(resize_keyboard = True)
gender_settings_reply.row('🙋‍♂️  Парней', '🙋‍♀️  Девушек')
gender_settings_reply.row('👻  Без разницы')
gender_settings_reply.row('❌  Отмена  ❌')



#  CANCEL

cancel_button = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_button.row("❌  Отмена  ❌")

cancel_city_button = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_city_button.row("Без разницы")
cancel_city_button.row("❌  Отмена  ❌")

cancel_profile_button = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_profile_button.row("❌  Отменить  ❌")



#  LEAVE CHAT
leave_chat_button = ReplyKeyboardMarkup(resize_keyboard = True)
leave_chat_button.row("❌  Покинуть чат  ❌")

leave_anonym_chat_button = ReplyKeyboardMarkup(resize_keyboard = True)
leave_anonym_chat_button.row("❌  Покинуть чат")



#  CANCEL QUEUE
cancel_queue_button = ReplyKeyboardMarkup(resize_keyboard = True)
cancel_queue_button.row("❌  Отменить поиск")








#  START

start_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_button.row("/start")





#  ADMIN

admin_menu = ReplyKeyboardMarkup(resize_keyboard = True)
admin_menu.row("Статистика")
admin_menu.row("Сообщение", "Рассылка")
admin_menu.row("Верификация", "Удалить")
admin_menu.row("Выйти из меню разработчиков")


forward_button = ReplyKeyboardMarkup(resize_keyboard = True)
forward_button.row("Рассылка сообщения")
forward_button.row("Рассылка обновления")
forward_button.row("Рассылка чата")
forward_button.row("Назад")

verification_button = ReplyKeyboardMarkup(resize_keyboard = True)
verification_button.row("Выдать верификацию",  "Отменить верификацию")
verification_button.row("Назад")

delete_user_button = ReplyKeyboardMarkup(resize_keyboard = True)
delete_user_button.row("Удалить из чата")
delete_user_button.row("Удалить всех из чата")
delete_user_button.row("Удалить все данные")
delete_user_button.row("Назад")



