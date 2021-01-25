import telebot
from config import TOKEN, keys
from extensions import ConversionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для начала работы бота необходимо ввести команду в формате:\n' \
'<Название переводимой валюты> (с маленькой буквы)\n' \
'<В какую валюту перевести> (с маленькой буквы)\n' \
'<Количество переводимой валюты> (цифра)\n' \
'Через пробел!!!\n'\
'Например - "доллар евро 5"\n' \
'Чтобы увидеть список всех доступных валют введите команду: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise ConversionException('Много параметров.')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote, base, amount)

    except ConversionException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')

    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
