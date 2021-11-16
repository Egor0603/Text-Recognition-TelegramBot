import telebot
from config import TOKEN
import easyocr


bot = telebot.TeleBot(TOKEN)


class TextException(Exception):
    pass


class Recognition(Exception):

    @staticmethod
    def get_text(fileid, lang):

        file_info = bot.get_file(fileid)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(file_info.file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        if lang is None:
            raise TextException('Сначала выберите язык.')

        reader = easyocr.Reader(lang)
        result = reader.readtext(file_info.file_path)

        if result is None:
            raise TextException('Текст не найден :(')

        return result
