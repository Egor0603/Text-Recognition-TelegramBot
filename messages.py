import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN
from classes import TextException, Recognition


bot = telebot.TeleBot(TOKEN)

lang = None


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('Русский', callback_data='cb_ru'),
               InlineKeyboardButton('Английский', callback_data='cb_en'),
               InlineKeyboardButton('Китайский', callback_data='cb_ch_sim'),
               InlineKeyboardButton('Русский+Английский', callback_data='cb_ru_en'))
    return markup


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = 'Это бот для распознования текста на фото. Выберите язык и отправьте фото.\
           Для начала введите команду /set'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['set'])
def message_handler(message):
    bot.send_message(message.chat.id, 'Выберите язык', reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'cb_ru':
        global lang
        bot.send_message(call.message.chat.id, 'Вы выбрали русский язык, теперь отправьте фото')
        lang = ['ru']

    elif call.data == 'cb_en':
        bot.send_message(call.message.chat.id, 'Вы выбрали английский язык, теперь отправьте фото')
        lang = ['en']

    elif call.data == 'cb_ch_sim':
        bot.send_message(call.message.chat.id, 'Вы выбрали китайский язык, теперь отправьте фото')
        lang = ['ch_sim']

    elif call.data == 'cb_ch_sim':
        bot.send_message(call.message.chat.id, 'Вы выбрали русский+английский языки, теперь отправьте фото')
        lang = ['cb_ru_en']


@bot.message_handler(content_types=['photo'])
def translate(message):
    fileid = message.photo[-1].file_id

    try:

        result = Recognition.get_text(fileid, lang)
        print(result)

    except TextException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка бота:\n{e}')

    else:
        text = []
        check = []

        for i in result:
            text.append(i[1])
            check.append(i[2])

        text2 = ' '.join(map(str, text))
        bot.send_message(message.chat.id, text2)

        if any(check) < 5:
            bot.send_message(message.chat.id, '---Обнаружена низкая точность распознания!\
             В тексте могут быть ошибки.---')


bot.polling()
