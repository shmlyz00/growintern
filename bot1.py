import telebot
import requests
from datetime import datetime
import pytz

TOKEN = '6473175383:AAHGQji3XFO9HDsTwS7NKW3uY4-KP7Ng0J0'
WEATHER_API_KEY = 'c3d72c6f3db342c4ab52b825f9e8df22'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello! I am your bot.')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, 'Send /start to receive a greeting.')


@bot.message_handler(commands=['weather'])
def weather(message):
    city = ' '.join(message.text.split()[1:])  # City name from command arguments
    if not city:
        bot.reply_to(message, 'Please provide a city name.')
        return
    
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric')
    data = response.json()
    
    if data.get('cod') == 200:
        weather_info = (
            f"Weather in {data['name']}:\n"
            f"Temperature: {data['main']['temp']}°C\n"
            f"Weather: {data['weather'][0]['description']}"
        )
    else:
        weather_info = "City not found or invalid API key."
    
    bot.reply_to(message, weather_info)


@bot.message_handler(commands=['news'])
def news(message):
    api_key = '46b1f1535fe543f49d1956eccb58e61d'
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}')
    data = response.json()
    
    if data.get('status') == 'ok':
        articles = data['articles'][:9]  # Get top 5 articles
        news_message = '\n\n'.join(f"{article['title']}\n{article['description']}" for article in articles)
    else:
        news_message = "Could not fetch news at the moment."

    bot.reply_to(message, news_message)

@bot.message_handler(commands=['convert'])
def convert(message):
    parts = message.text.split(maxsplit=3)
    if len(parts) < 4:
        bot.reply_to(message, 'Usage: /convert <amount> <from_currency> <to_currency>')
        return

    amount = parts[1]
    from_currency = parts[2]
    to_currency = parts[3]
    api_key = '44ebaa0a4a96db7660c8879e'
    
    response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}')
    data = response.json()
    
    if 'error' in data:
        bot.reply_to(message, f"Error: {data['error-type']}")
        return
    
    rate = data['rates'].get(to_currency)
    
    if rate:
        converted_amount = float(amount) * rate
        bot.reply_to(message, f"{amount} {from_currency} is {converted_amount:.2f} {to_currency}.")
    else:
        bot.reply_to(message, "Invalid currency code.")

@bot.message_handler(commands=['advice'])
def advice(message):
    response = requests.get('https://api.adviceslip.com/advice')
    data = response.json()
    advice_message = data['slip']['advice']
    bot.reply_to(message, f"Here's some advice: {advice_message}")

@bot.message_handler(commands=['time'])
def time(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.reply_to(message, 'Usage: /time <timezone>')
        return

    timezone = parts[1]
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        time_message = f"Current date and time in {timezone}:\n{now.strftime('%Y-%m-%d %H:%M:%S')}"
    except pytz.UnknownTimeZoneError:
        time_message = "Unknown time zone. Please provide a valid time zone."

    bot.reply_to(message, time_message)

@bot.message_handler(commands=['info'])
def info(message):
    info_message = (
        'I am a bot created to help you. Here are some commands you can use:\n'
        '/start - Greet you\n'
        '/help - Show this help message\n'
        '/weather <city> - Get the current weather for a city\n'
        '/news - Get top 8 articles\n'
        '/advice - Get a random advice \n'
        '/time - Show information about the current weather for a timezone\n'
        '/convert - Converts an amount from one currency to another \n.'
        '/info - Show information about the bot'
    )
    bot.reply_to(message, info_message)

bot.polling()

