import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# Set your OpenAI API key and Telegram bot token
openai.api_key = "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"  # Replace with your OpenAI API Key
TELEGRAM_TOKEN = "7638208028:AAHchjtDECdiyEaJNCyVvvoxsyvzaDr4Vek"  # Replace with your Telegram Bot Token

# Enable logging to capture any issues in the console
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the function to get predictions from ChatGPT
async def get_response_from_chatgpt(user_message):
    try:
        response = openai.Completion.create(
            model="gpt-4",  # You can use other models if needed
            prompt=user_message,
            temperature=0.7,  # Adjust for creativity vs. deterministic output
            max_tokens=150,  # Adjust token limit as needed
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Sorry, I couldn't process your request due to an error with the OpenAI API."
    except Exception as e:
        logger.error(f"Error: {e}")
        return "Sorry, I couldn't process your request right now."

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Send me a message, and I will predict the next outcome using ChatGPT!")

# Handle the message and get ChatGPT response
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text.strip()

    if not user_message:
        await update.message.reply_text("Please send a valid message.")
        return

    # Get response from ChatGPT
    prediction = await get_response_from_chatgpt(user_message)
    await update.message.reply_text(f"ChatGPT's response: {prediction}")

# Main function to set up and run the bot
async def main():
    # Initialize the application and dispatcher
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    
    # Message handler for any text input
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

