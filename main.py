import telebot
from config import TOKEN, values
from extensions import APIException, Exchanger
import traceback


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message):
    text = "Здравствуйте, бот поддерживает следующие команды: \n" \
           "start/help - получить справочную информацию \n" \
           "values - список доступных для конвертирования валют \n" \
           "Пример запроса для конвертирования - евро доллар 1 что означает: \n" \
           "цена 'евро' в 'долларах' в количестве '1'"
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=["values"])
def show_values(message):
    text = "Доступные валюты:"
    for i in values.keys():
        text = "\n".join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def exchanges(message):
    give_values = message.text.split(" ")
    try:
        if len(give_values) != 3:
            raise APIException("Количество элементов в запросе не равно 3")

        ans = Exchanger.get_price(*give_values)
    except APIException as e:
        bot.reply_to(message, f"ошибка:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, ans)


bot.polling()
