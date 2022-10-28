import requests
import datetime
from config import TOKEN, API_KEY
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Приветствую!\n'
                        'Я бот для прогноза погоды.\nНапишите название города, используя "/" и я пришлю вам прогноз.')


@dp.message_handler(content_types='text')
async def get_weather(message: types.Message):
    chel = message.text
    if '/' in chel:
        a = chel.replace('/', '')
    else:
        await message.reply('добавьте символ!')
    smile_codes = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Snow': 'Снег \U0001F328',
        'Thunderstorm': 'Гроза \U000026A1',
        'Mist': 'Туман \U0001F32B'
    }
    try:

        w = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={a}&appid={API_KEY}&units=metric')
        data = w.json()

        city = data['name']
        current_temp = data['main']['temp']

        opisanie_pogody = data['weather'][0]['main']
        if opisanie_pogody in smile_codes:
            op = smile_codes[opisanie_pogody]
        else:
            op = 'Я такой погоды не знаю, лучше прячьтесь!'

        vlajnost = data['main']['humidity']
        davl = data['main']['pressure']
        veter = data['wind']['speed']
        voshod_solnca = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        zakat_solnca = datetime.datetime.fromtimestamp(data['sys']['sunset'])


        await message.reply(f'Текущая дата: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
              f'Погода по вашему запросу в городе: {city}\nТемпература воздуха: {current_temp} C° {op}\n'
              f'Влажность воздуха: {vlajnost}%\nДавление: {davl} мм.рт.ст\nСкорость ветра: {veter} м/сек.\n'
              f'Восход солнца: {voshod_solnca} утра\nЗакат солнца: {zakat_solnca} вечера\n'
              f'Спасибо за обращение. Хорошего дня!👍'
              )

    except:
        pass

if __name__ == '__main__':
    executor.start_polling(dp)




