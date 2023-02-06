import telebot
from telebot import types  # для указание типов
from config import keys, TOKEN
from utils import CurrencyConverter, ConvertionException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton('/help')
    markup.add(btn1)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я тестовый бот который умеет работать с курсами валют! Введите "
                          "команду в следующем формате:\n "
                          "1)Имя валюты\n\
2)В какую валюту хотите перевести\n\
3)Количество переводимой валюты\n\
Например: Доллар Рубль 100\n\
  Увидеть список доступных валют:\n                          /values".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Доступные валюты:")
    markup.add(button1)
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise ConvertionException("Слишком много параметров!")
        if len(values) < 3:
            raise ConvertionException("Слишком мало параметров!")

        quote, base, amount = values
        amount = float(amount)
        result = CurrencyConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        q1 = ""
        if quote == "Доллар":
            q1 = "$"
        if quote == "Евро":
            q1 = "€"
        if quote == "Рубль":
            q1 = "₽"

        b1 = ""
        if base == "Доллар":
            b1 = "Долларах"
        if base == "Евро":
            b1 = "Евро"
        if base == "Рубль":
            b1 = "Рублях"
        text = f'Цена {amount} {q1} в {b1} = {round(result, 2)}!'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
