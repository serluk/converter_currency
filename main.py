import requests
import telebot
import json

from extensions import Converter, ApiException
from config import TOKEN, exchanges


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Приветствие!"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = "Доступные валюты:"
    for val in exchanges.keys():
        text = '\n'.join((text, val))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, "Неверное количество параметров!")
    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except ApiException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")


bot.polling()



