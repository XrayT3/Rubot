#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import telebot
import datetime
import time
import RUconst
from telebot import types

bot = telebot.TeleBot(RUconst.TOKEN)

now_time = datetime.datetime.now()
day = 'day'
raspisanie = 'raspisanie'
raspisanie2 = 'raspisanie2'
tm = 'tm'
month = 'month'
hour = 4
minute = 20
urok = 1
ur = 'ur'


#Блок, который отвечает за дату и время.
def data_and_vremy():
    global day, month, tm, raspisanie, raspisanie2, hour, minute, ur, urok
    now_time = datetime.datetime.now()
    hour = now_time.hour
    minute = now_time.minute
    month = {1: u"Января", 2: u"Февраля", 3: u"Марта", 4: u"Апреля", 5: u"Мая", 6: u"Июня", 7: u"Июля", 8: u'Августа',
              9: u'Сентября', 10: u'Октября', 11: u'Ноября', 12: u'Декабрь'}
    today = datetime.date.today()
    month = str((month[today.month]))
    day = str(today.day)
    days = {0: u"понедельник", 1: u"вторник", 2: u"среда", 3: u"четверг", 4: u"пятница", 5: u"суббота",
            6: u"воскресенье"}
    tm = (days[datetime.date.today().weekday()])
    if tm == 'понедельник':
        raspisanie = RUconst.Pn
        raspisanie2 = RUconst.Vt
    if tm == 'вторник':
        raspisanie = RUconst.Vt
        raspisanie2 = RUconst.Sr
    if tm == 'среда':
        raspisanie = RUconst.Sr
        raspisanie2 = RUconst.Che
    if tm == 'четверг':
        raspisanie = RUconst.Che
        raspisanie2 = RUconst.Pt
    if tm == 'пятница':
        raspisanie = RUconst.Pt
        raspisanie2 = RUconst.Su
    if tm == 'суббота':
        raspisanie = RUconst.Su
        raspisanie2 = RUconst.Vsk
    if tm == 'воскресенье':
        raspisanie = RUconst.Vsk
        raspisanie2 = RUconst.Vt


def urok_nomer():
    data_and_vremy()
    global urok, ur
    if (hour == 8) and (0 <= minute <= 40 + 5):
        urok = 1
        ur = RUconst.ur1
    elif ((hour == 8) and (45 < minute <= 59)) or ((hour == 9) and (0 <= minute <= 25 + 15)):
        urok = 2
        ur = RUconst.ur2
    elif ((hour == 9) and (40 < minute <= 59)) or ((hour == 10) and (0 <= minute <= 20 + 15)):
        urok = 3
        ur = RUconst.ur3
    elif ((hour == 10) and (35 < minute <= 59)) or ((hour == 11) and (0 <= minute <= 15 + 15)):
        urok = 4
        ur = RUconst.ur4
    elif ((hour == 11) and (30 < minute <= 59)) or ((hour == 12) and (0 <= minute <= 10 + 5)):
        urok = 5
        ur = RUconst.ur5
    elif (hour == 12) and (15 < minute <= 55 + 4):
        urok = 6
        ur = RUconst.ur6
    elif (hour == 13) and (0 <= minute <= 40 + 5):
        urok = 7
        ur = RUconst.ur7
    else:
        ur = RUconst.ur10
        urok = 0


def scolco_do_konca_v1():
    data_and_vremy()
    konec = 0
    min = hour*60+minute
    if tm != 'воскресенье':
        if urok == 1:
            konec = 520 - min
        elif urok == 2:
            konec = 565 - min
        elif urok == 3:
            konec = 620 - min
        elif urok == 4:
            konec = 675 - min
        elif urok == 5:
            konec = 730 - min
        elif urok == 6:
            konec = 775 - min
        elif urok == 7:
            konec = 820 - min
        else:
            konec = 0
    else:
        konec = 0
        return konec



#///////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Как тебя зовут?')
    bot.register_next_step_handler(sent, hello)


def hello(message):
    bot.send_message(message.chat.id, 'Привет, {name}. Рад тебя видеть.'.format(name=message.text))
    time.sleep(1)
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('🔔Звонки', '📚Уроки')
    keyboard.row('📝Записать ДЗ')
    # keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Олимпиады', 'Мероприятия']])
    bot.send_message(message.chat.id, 'Что хочешь узнать?', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def zvonki(message) :
    urok_nomer()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Вторая смена']])
    keyboard1 = types.InlineKeyboardMarkup()
    keyboard1.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['На завтра']])
    keyboard2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard2.row('Что задали?', 'Помочь(в разработке)')
    keyboard2.row('ГДЗ(в разработке)','Назад')
    if message.text == '🔔Звонки':
         bot.send_message(message.chat.id, '<b>Расписание звонков первой смены</b>\n\n' + ur + 'До конца урока осталось ' + str(scolco_do_konca_v1()) + ' минут.', parse_mode='HTML', reply_markup=keyboard)

    if message.text == 'Назад':
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row('🔔Звонки', '📚Уроки')
            keyboard.row('📝Записать ДЗ')
            # keyboard.add(*[telebot.types.KeyboardButton(name) for name in ['Олимпиады', 'Мероприятия']])
            bot.send_message(message.chat.id, 'Что хочешь узнать?', parse_mode='HTML', reply_markup=keyboard)

    if message.text == '📚Уроки':
        data_and_vremy()
        bot.send_message(message.chat.id,
                             '<b>' + day + ' ' + month + ' ,' + tm + '</b>\n\n' +
                             raspisanie, parse_mode='HTML', reply_markup= keyboard1)
        bot.send_message(message.chat.id, '...', reply_markup= keyboard2)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    urok_nomer()
    data_and_vremy()
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Первая смена']])
    keyboard1 = types.InlineKeyboardMarkup()
    keyboard1.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['Вторая смена']])
    keyboard2 = types.InlineKeyboardMarkup()
    keyboard2.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['На сегодня']])
    keyboard3 = types.InlineKeyboardMarkup()
    keyboard3.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['На завтра']])
    if c.data == 'Первая смена':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                  text='<b>Расписание звонков первой смены</b>\n\n' + ur + 'До конца урока осталось ' + str(scolco_do_konca_v1()) + ' минут.', parse_mode='HTML', reply_markup=keyboard1)

    if c.data == 'Вторая смена':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                  text='<b>Расписание звонков второй смены</b>\n\n'
                                       '1. 14:00 - 14:40\n'
                                       '2. 14:50 - 15:30\n'
                                       '3. 15:45 - 16:25\n'
                                       '4. 16:35 - 17:15\n'
                                       '5. 17:25 - 18:05\n'
                                       '6. 18:10 - 18:50\n',
                                  parse_mode='HTML', reply_markup=keyboard)

    if c.data == 'На завтра':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                  text='<b>' + day + ' ' + month + ' ,' + tm + '</b>\n\n' +
                                  raspisanie2, parse_mode='HTML', reply_markup= keyboard2)

    if c.data == 'На сегодня':
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                  text='<b>' + day + ' ' + month + ' ,' + tm + '</b>\n\n' +
                                  raspisanie, parse_mode='HTML', reply_markup= keyboard3)



bot.polling()
