import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import os
from dotenv import load_dotenv
from data import get_weather_data_weekly, get_weather_data_daily

API_TOKEN = os.getenv("API_TOKEN")


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

LatLon = []

@dp.message_handler(commands=["start"])
async def find_location(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonLocation = types.KeyboardButton("Share my location 📍", request_location=True)
    keyboard.add(buttonLocation)
    first_name = message.from_user.first_name

    await message.answer(f"🤖: Hello {first_name}, \n🇺🇿 You are using the most universal and official telegram bot of forecast information of Uzbekistan. \n🧨 To start, please, share your location!", reply_markup=keyboard)

@dp.message_handler(commands=["help"])
async def main_info(message: types.Message):
    await message.answer("ℹ️ This is usage of bot guideline:"
    "\n"
    "\n1️⃣ /start - command for restarting the bot if you have any kind of troubles."
    "\n2️⃣ /help - command to use this guideline."
    '\n3️⃣ "Share location 📍" button to give the most important factor for great forecast information.'
    '\n4️⃣ "📌 Today" button to find out what kind of day you are having.'
    '\n5️⃣ "➡️ Next 3 days" button to identify what kind of upcoming 3 days you are going to have.'
    "\n"
    "\n👨‍💻 Creator: Ismoiljon Vahobjonov"
    "\n🆘 If you have some feedback about improving the bot, you can contact me: @CodingProUzb")

@dp.message_handler(content_types=types.ContentType.LOCATION)
async def weather_info(message: types.Message):
    latitude = message.location.latitude
    longitude = message.location.longitude

    LatLon.append(latitude)
    LatLon.append(longitude)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('📌 Today')
    button2 = types.KeyboardButton('➡️ Next 3 days')

    keyboard.add(button1, button2)
    response_text = f"Location known: {latitude}, {longitude}, \nChoose one of them:"

    await message.answer(response_text, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == '📌 Today')
async def handle_option1(message: types.Message):
    forecast_info = get_weather_data_daily(LatLon[0], LatLon[1])
    response_text = f"This is daily forecast! \n{forecast_info}"
    photo_url = './src/img/daily.png'
    await bot.send_photo(message.chat.id, types.InputFile(photo_url),caption=response_text)

@dp.message_handler(lambda message: message.text == '➡️ Next 3 days')
async def handle_option2(message: types.Message):
    forecast_info = get_weather_data_weekly(LatLon[0], LatLon[1])
    response_text = f"This is 3 days forecast! \n{forecast_info}"
    photo_url = './src/img/weekly.png'
    await bot.send_photo(message.chat.id, types.InputFile(photo_url),caption=response_text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
