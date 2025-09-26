# pip install pyTelegramBotAPI
import telebot
import requests

BOT_TOKEN = "6526495207:AAES3K8wRgaK6216bMtC6PqW44v2FJ0Q9bA"
#ESP_IP = input("Enter your ESP IP: ")
ESP_IP = "192.168.1.14"
URL  = f"http://{ESP_IP}:80"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Use /on or /off to control the LED.")

@bot.message_handler(commands=['on'])
def led_on(message):
    try:
        requests.get(f"{URL}/on", timeout=5)
        bot.reply_to(message, "LED is ON ✅")
    except:
        bot.reply_to(message, "Failed to reach ESP8266 ⚠️")

@bot.message_handler(commands=['off'])
def led_off(message):
    try:
        requests.get(f"{URL}/off", timeout=5)
        bot.reply_to(message, "LED is OFF ❌")
    except:
        bot.reply_to(message, "Failed to reach ESP8266 ⚠️")

bot.polling()

