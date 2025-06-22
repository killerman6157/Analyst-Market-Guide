import json
import pytz
from datetime import datetime, time
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
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
        exit(1) # [span_0](start_span)[span_0](end_span)[span_1](start_span)[span_1](end_span)[span_2](start_span)[span_2](end_span)
    except json.JSONDecodeError as e:
        logger.error(f"Error: Invalid JSON in '{filename}': {e}")
        # Exit if the JSON is malformed.
        exit(1) # [span_3](start_span)[span_3](end_span)[span_4](start_span)[span_4](end_span)
    except KeyError as e:
        logger.error(f"Error: Missing key in '{filename}': {e}. Ensure 'bot_token' and 'user_id' are present.")
        # Exit if required keys are missing.
        exit(1) # [span_5](start_span)[span_5](end_span)

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
    ) # [span_6](start_span)[span_6](end_span)[span_7](start_span)[span_7](end_span)
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
        logger.error(f"Failed to send daily reminder to chat_id {USER_ID}: {e}") # [span_8](start_span)[span_8](end_span)

# Error handler for the dispatcher
async def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer (optional)."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=True)
    # You might want to send a message to a specific admin chat_id for critical errors.
    # For example: await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Error: {context.error}") # [span_9](start_span)[span_9](end_span)[span_10](start_span)[span_10](end_span)

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # The Updater class continuously fetches new updates from Telegram.
    updater = Updater(BOT_TOKEN) # [span_11](start_span)[span_11](end_span)[span_12](start_span)[span_12](end_span)

    # Get the dispatcher to register handlers.
    # The Dispatcher routes all kinds of updates to its registered handlers.
    dispatcher = updater.dispatcher # [span_13](start_span)[span_13](end_span)[span_14](start_span)[span_14](end_span)

    # Add command handlers for /start and /stop
    dispatcher.add_handler(CommandHandler("start", start_command)) # [span_15](start_span)[span_15](end_span)[span_16](start_span)[span_16](end_span)[span_17](start_span)[span_17](end_span)
    dispatcher.add_handler(CommandHandler("stop", stop_command))

    # Get the JobQueue instance from the Updater.
    # This is python-telegram-bot's built-in scheduler.
    job_queue = updater.job_queue # [span_18](start_span)[span_18](end_span)[span_19](start_span)[span_19](end_span)

    # Schedule the daily reminder job using JobQueue.
    # It will run every day at 9:00 AM in the 'Africa/Lagos' timezone.
    job_queue.run_daily(send_daily_reminder_job, time=time(hour=9, minute=0, tzinfo=pytz.timezone('Africa/Lagos'))) # [span_20](start_span)[span_20](end_span)[span_21](start_span)[span_21](end_span)[span_22](start_span)[span_22](end_span)
    logger.info("Daily reminder job scheduled for 9:00 AM Africa/Lagos.")

    # Add a global error handler to catch unhandled exceptions.
    dispatcher.add_error_handler(error_handler)

    # Start the Bot.
    # This begins the long-polling process to fetch updates from Telegram.
    updater.start_polling() # [span_23](start_span)[span_23](end_span)[span_24](start_span)[span_24](end_span)[span_25](start_span)[span_25](end_span)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot if not called.
    updater.idle() # [span_26](start_span)[span_26](end_span)[span_27](start_span)[span_27](end_span)[span_28](start_span)[span_28](end_span)

if __name__ == '__main__':
    main()

