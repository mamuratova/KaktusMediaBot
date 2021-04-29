import telebot
from telebot import types
from decouple import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from parsing_kaktus import main

data_list2 = main()

bot = telebot.TeleBot(config('Token'))


desc = 0
phc = 0
ph = 0
des = 0


@bot.message_handler(commands=['start'])
def starting(message):
    main()
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    name = message.from_user.first_name
    bot.send_message(chat_id, f'Привет! {name}, хочешь узнать свежие новости!', reply_markup=yes_no_keyboard())


@bot.callback_query_handler(func=lambda c: True)
def func(c):
    chat_id = c.message.chat.id
    count = 0
    try:
        if c.data == 'no':
            bot.delete_message(chat_id, c.message.message_id)
            bot.send_message(chat_id, 'Ну тогда пока...')
            bot.send_sticker(chat_id, 'CAACAgIAAxkBAALtCGBCF8aJrLdmVL_fxuCxJoMqXRRCAAKyAAOvxlEaD9wDyT-Zj8seBA')
        elif c.data == 'yes':
            bot.send_message(chat_id, 'Новости на сегодня: ', reply_markup=news_keyboard())
            bot.delete_message(chat_id, c.message.message_id)
            
        for i in range(len(data_list2)):
            if c.data == str(i+1):
                bot.delete_message(chat_id, c.message.message_id)
                title = data_list2[i].get('title')
                link = data_list2[i].get('link')
                global photo
                photo = data_list2[i].get('photo')
                global description
                description = data_list2[i].get('description')
                if len(description) > 1300:
                    description = description[:1300] + '...'
                bot.send_message(chat_id, {title}, reply_markup=another_keyboards1(i))
        if c.data == 'photo':
            global ph
            ph = bot.send_message(chat_id, text=photo).message_id
            global phc
            phc += 1

        elif c.data == 'description':
            global des
            des = bot.send_message(chat_id, text=description).message_id
            global desc
            desc += 1

        elif c.data == 'back':
            bot.delete_message(chat_id, c.message.message_id)
            if phc > 0:
                bot.delete_message(chat_id, ph)
                phc -= 1
            if desc > 0:
                bot.delete_message(chat_id, des)
                desc -= 1
            bot.send_message(chat_id, 'Самые свежие новости: ', reply_markup=news_keyboard())

        elif c.data == 'quit':
            bot.delete_message(chat_id, c.message.message_id)
            if phc > 0:
                bot.delete_message(chat_id, ph)
                phc -= 1
            if desc > 0:
                bot.delete_message(chat_id, des)
                desc -= 1
            s = bot.send_message(chat_id, f'Пока {c.from_user.first_name}!').message_id
            ss = bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEBAAGjYFQdhy52A92ne1kebpjSnF73l3QAAhcDAAJWnb0K54YuxMZUxRseBA').message_id

    except Exception as e:
        des = bot.send_message(chat_id, f'Я не знаю что делать!\nУ меня какая-та ошибка!\n{e}').message_id
        desc += 1
     




#---------------------------------------------------------------------Keyboards-------------------------------------------------------------


# Кнопки да или нет
def yes_no_keyboard():
    yes_no = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton('Да', callback_data='yes')
    no = types.InlineKeyboardButton('Нет', callback_data='no')
    yes_no.add(yes, no)
    return yes_no


# кнопки из новостей
def news_keyboard():
    news = types.InlineKeyboardMarkup()
    for i in data_list2:
        news.add(InlineKeyboardButton(text=i.get('title'), callback_data=i.get('count')))
    return news


# кнопки - назад, вперед, фото, ссылка ----1
def another_keyboards1(num):
    another_keybord = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton('Назад', callback_data='back')
    description = types.InlineKeyboardButton('Подробнее', callback_data='description')
    link = types.InlineKeyboardButton('Link', url=data_list2[num].get('link'))
    photo = types.InlineKeyboardButton('Фото', callback_data='photo')
    quit = types.InlineKeyboardButton('Выход', callback_data='quit')
    another_keybord.add(back, description, photo, link, quit)
    return another_keybord


bot.polling(none_stop=True)




