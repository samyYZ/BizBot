from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import openai
import requests
import os

# API Keys"
TELEGRAM_BOT_TOKEN = "7653650251:AAHSLzOePbnjm2HN4RaPxN6bZ_kcicxaaJc"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

WEATHER_API_KEY = "227d6af54be24e9f1ccd8eb1f6dc4c13"


openai.api_key = OPENAI_API_KEY

# OpenAI Chat Function
async def handle_message(update: Update, context):
    user_message = update.message.text.lower()  # Convert to lowercase for better matching
    print(f"Received message: {user_message}")  # Debugging line

    # Custom responses
    responses = {
        "hi": "Hello! How are you?",
        "hello": "Hey there! How can I assist you?",
        "how are you": "I'm just a bot, but I'm doing great! How about you?",
        "help": "You can ask me about business ideas, market trends, and more!",
    }
     # Check if the user message matches a custom response
    response = responses.get(user_message, "I'm not sure how to respond to that.")
    
    await update.message.reply_text(response)
# Command Handlers
async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm BizBot. How can I assist you?")
async def help_command(update: Update, context):
    await update.message.reply_text("I can assist with:\n✅ AI responses\n✅ Weather updates\nUse /info to learn more.")

async def info_command(update: Update, context):
    await update.message.reply_text("I'm a chatbot powered by OpenAI and Telegram API.")

async def weather_command(update: Update, context):
    if not context.args:
        await update.message.reply_text("Usage: /weather <city>")
        return

    city = " ".join(context.args)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        await update.message.reply_text("City not found. Try again.")
    else:
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        await update.message.reply_text(f"Weather in {city}: {temp}°C, {desc}")

# Main function
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("info", info_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
