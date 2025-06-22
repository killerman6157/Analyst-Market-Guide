import json
import logging
from datetime import datetime, time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Saitin logging don ganin abubuwan da ke faruwa
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load config.json
# Wannan sashin yana kokarin bude fayil din 'config.json' don samun 'bot_token' da 'user_id'.
# Idan fayil din babu ko kuma akwai kuskure a JSON, zai bayar da sako kuma ya tsaya.
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    logger.error("Ba a samo fayil din config.json ba. Da fatan za a kirkiri fayil din tare da 'bot_token' da 'user_id'.")
    exit()
except json.JSONDecodeError:
    logger.error("Akwai kuskure a fayil din config.json. Da fatan za a tabbatar cewa JSON din daidai ne.")
    exit()

BOT_TOKEN = config.get('bot_token')
USER_ID = config.get('user_id') # Wannan shine ID na mai amfani da za a aikawa da tunatarwa.

if not BOT_TOKEN:
    logger.error("BOT_TOKEN ba a samo shi ba a config.json. Da fatan za a tabbatar an saita shi.")
    exit()
# Lura: Ba za mu fita ba idan USER_ID bai kasance ba, saboda ana iya samunsa ta hanyar /start command.

# Sakonni na yau da kullum da aka tsara ta ranar mako
daily_messages = {
    'Sunday': "🗓️ Yau Lahadi ne –\n❌ Avoid trading\n✅ Prepare Weekly Zones\n🔍 Review last week's setups",
    'Monday': "🗓️ Yau Litinin ne –\n⚠️ Watch Accumulation / False BOS\n✅ Mark liquidity zones + structure\n❌ No early entry",
    'Tuesday': "🗓️ Yau Talata ne –\n✅ Wait for BOS confirmation\n✅ Enter based on 15min + 5min confluence\n💡 NY Open = sniper entry",
    'Wednesday': "🗓️ Yau Laraba ne –\n🔥 Most reliable day for entries\n✅ Breakout / Retest / SMC trades\n🎯 Continue/reverse Monday-Tuesday zone",
    'Thursday': "🗓️ Yau Alhamis ne –\n✅ Strong continuation from Wed\n⚠️ Be ready for profit-taking\n✅ Trail SL and manage",
    'Friday': "🗓️ Yau Jumma’a ne –\n⚠️ Exit before NY session close\n✅ Avoid late entries\n🧾 Trade review + journal update",
    'Saturday': "🗓️ Yau Asabar ne –\n❌ No trade (Crypto only, manipulated)\n✅ Backtest or Learn strategy"
}

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Wannan aikin yana aiko da sako na maraba lokacin da mai amfani ya fara bot din (/start).
    Kuma yana nuna ID na mai amfani don taimaka masa ya saita 'user_id' a 'config.json'.
    """
    user_id = update.effective_user.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    await update.message.reply_text(
        f"Sannu, {first_name}! Maraba da zuwa bot din kasuwar kasuwanci.\n"
        f"Makin shaidarku (User ID) shine: `{user_id}`.\n"
        f"Da fatan za ku duba 'config.json' domin tabbatar da cewa 'user_id' dinku ya dace da wannan. Sannan ku fara aiki da bot din yadda ya kamata."
    )
    logger.info(f"An karbi /start daga mai amfani: {user_id} (username: {username})")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Wannan aikin yana aiko da sako na taimako lokacin da aka danna /help."""
    await update.message.reply_text("Wannan bot yana aiko muku da tunatarwa ta yau da kullum game da kasuwanci.\n"
                                    "Kuna iya amfani da /start don fara aiki da bot din kuma ku sami ID dinku.\n"
                                    "Bot din zai aiko da tunatarwa da karfe 9:00 na safe (lokacin Lagos) kowace rana.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Yana amsa duk wani sako da aka aiko masa da shi daidai."""
    logger.info(f"An karbi sako daga {update.effective_user.id}: {update.message.text}")
    # Kawai don gwaji, za mu iya amsa duk wani sako.
    # update.message.reply_text(f"Na karbi sakonku: {update.message.text}")

# --- Scheduled Job ---

async def send_daily_reminder_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Wannan aikin yana aiko da sakon tunatarwa na yau da kullum zuwa ga 'user_id' da aka saita a 'config.json'.
    Wannan aikin zai gudana ta hanyar 'job_queue' na bot.
    """
    # Duba ko akwai USER_ID a config.json
    if not USER_ID:
        logger.warning("USER_ID ba a saita shi ba a config.json. Ba za a iya aiko da tunatarwa ta yau da kullum ba.")
        return

    today = datetime.now(pytz.timezone('Africa/Lagos')).strftime('%A')
    message = daily_messages.get(today, "Babu sako na yau.")
    
    try:
        await context.bot.send_message(chat_id=USER_ID, text=message)
        logger.info(f"An aiko da tunatarwa ta yau da kullum zuwa {USER_ID} don {today}.")
    except Exception as e:
        logger.error(f"Kuskure yayin aiko da tunatarwa ta yau da kullum zuwa {USER_ID}: {e}")

def main() -> None:
    """Yana fara bot din kuma yana saita duk wani mai sarrafa umarni da aikin tsari."""
    # Kirkiri Application kuma ba shi token din bot din ka.
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    # Wannan yana hada aikin 'start_command' da umarnin '/start'.
    application.add_handler(CommandHandler("start", start_command))
    # Wannan yana hada aikin 'help_command' da umarnin '/help'.
    application.add_handler(CommandHandler("help", help_command))
    # Wannan yana karbar duk wani sako wanda ba umarni ba.
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Tsarawa aikin tunatarwa na yau da kullum
    # Wannan zai gudana kowace rana da karfe 9:00 na safe (lokacin Africa/Lagos).
    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_reminder_job, 
        time=time(hour=9, minute=0, tzinfo=pytz.timezone('Africa/Lagos')),
        name="Daily Reminder"
    )
    logger.info("An tsara aikin tunatarwa na yau da kullum don 9:00 AM (lokacin Africa/Lagos).")

    # Fara aikin bot din har sai mai amfani ya danna Ctrl-C
    logger.info("Bot ya fara sauraron sakonni...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

