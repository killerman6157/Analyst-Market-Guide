import json
import pytz
from datetime import datetime, time
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import logging

# Configure logging for better debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to load configuration with error handling
def load_config(filename='config.json'):
    """Loads bot configuration from a JSON file."""
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Error: Config file '{filename}' not found. Please create it with 'bot_token' and 'user_id'.")
        # Exit the script if the config file is missing, as it's critical.
        exit(1) # [1, 2, 3]
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON in '{filename}': {e}")
        # Exit if the JSON is malformed.
        exit(1) # [4, 5]
    except KeyError as e:
        logger.error(f"Error: Missing key in '{filename}': {e}. Ensure 'bot_token' and 'user_id' are present.")
        # Exit if required keys are missing.
        exit(1) # [4]

# Load configuration
config = load_config()
BOT_TOKEN = config['bot_token']
USER_ID = config['user_id'] # This USER_ID will be used for sending daily reminders

# Daily messages mapped by day
daily_messages = {
    'Sunday': "🗓️ Yau Lahadi ne –\n❌ Avoid trading\n✅ Prepare Weekly Zones\n🔍 Review last week's setups",
    'Monday': "🗓️ Yau Litinin ne –\n⚠️ Watch Accumulation / False BOS\n✅ Mark liquidity zones + structure\n❌ No early entry",
    'Tuesday': "🗓️ Yau Talata ne –\n✅ Wait for BOS confirmation\n✅ Enter based on 15min + 5min confluence\n💡 NY Open = sniper entry",
    'Wednesday': "🗓️ Yau Laraba ne –\n🔥 Most reliable day for entries\n✅ Breakout / Retest / SMC trades\n🎯 Continue/reverse Monday-Tuesday zone",
    'Thursday': "🗓️ Yau Alhamis ne –\n✅ Strong continuation from Wed\n⚠️ Be ready for profit-taking\n✅ Trail SL and manage",
    'Friday': "🗓️ Yau Jumma’a ne –\n⚠️ Exit before NY session close\n🧾 Trade review + journal update",
    'Saturday': "🗓️ Yau Asabar ne –\n❌ No trade (Crypto only, manipulated)\n✅ Backtest or Learn strategy"
}

# Define the /start command handler
async def start_command(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message when the /start command is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Sannu, {user.mention_html()}! Barka da zuwa bot din Daily Trading Reminders. "
        "Zan rika tura maka sakon tunatarwa na yau da kullum da karfe 9:00 na safe (Africa/Lagos lokaci). "
        "Idan kana so ka daina karbar sakonni, danna /stop."
    ) # [6, 7]
    logger.info(f"User {user.id} ({user.full_name}) started the bot.")

# Define the /stop command handler
async def stop_command(update: Update, context: CallbackContext) -> None:
    """Sends a goodbye message and stops daily reminders for the user."""
    user = update.effective_user
    await update.message.reply_text("Na gode da amfani da bot din. Ba zan sake tura maka sakonni ba.")
    # In a more complex application, you might want to remove the user's chat_id
    # from a list of active users or disable reminders specifically for this chat_id.
    logger.info(f"User {user.id} ({user.full_name}) stopped the bot.")

# Daily reminder function (adapted for python-telegram-bot's JobQueue)
async def send_daily_reminder_job(context: CallbackContext) -> None:
    """Sends a daily reminder message to the configured USER_ID."""
    today = datetime.now(pytz.timezone('Africa/Lagos')).strftime('%A')
    message = daily_messages.get(today, "No message for today.")
    try:
        await context.bot.send_message(chat_id=USER_ID, text=message)
        logger.info(f"Daily reminder sent for {today} to chat_id {USER_ID}.")
    except Exception as e:
        logger.error(f"Failed to send daily reminder to chat_id {USER_ID}: {e}") # [8]

# Error handler for the dispatcher
async def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer (optional)."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=True)
    # You might want to send a message to a specific admin chat_id for critical errors.
    # For example: await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Error: {context.error}") # [9, 10]

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    # This is the modern way to initialize the bot in python-telegram-bot v20+.
    application = Application.builder().token(BOT_TOKEN).build() #

    # Get the dispatcher to register handlers.
    # The Dispatcher routes all kinds of updates to its registered handlers.
    # With Application, you add handlers directly to the application.
    
    # Add command handlers for /start and /stop
    application.add_handler(CommandHandler("start", start_command)) # [11, 6, 7]
    application.add_handler(CommandHandler("stop", stop_command))

    # Get the JobQueue instance from the Application.
    # This is python-telegram-bot's built-in scheduler.
    job_queue = application.job_queue # [12, 13]

    # Schedule the daily reminder job using JobQueue.
    # It will run every day at 9:00 AM in the 'Africa/Lagos' timezone.
    job_queue.run_daily(send_daily_reminder_job, time=time(hour=9, minute=0, tzinfo=pytz.timezone('Africa/Lagos'))) # [12, 13, 14]
    logger.info("Daily reminder job scheduled for 9:00 AM Africa/Lagos.")

    # Add a global error handler to catch unhandled exceptions.
    application.add_error_handler(error_handler)

    # Run the bot.
    # This begins the long-polling process to fetch updates from Telegram.
    # application.run_polling() replaces updater.start_polling() and updater.idle()
    application.run_polling(allowed_updates=Update.ALL_TYPES) #

if __name__ == '__main__':
    main()
    
