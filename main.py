import json
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pytz

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

BOT_TOKEN = config['bot_token']
USER_ID = config['user_id']

bot = Bot(token=BOT_TOKEN)

# Daily messages mapped by day
daily_messages = {
    'Sunday': "🗓️ Yau Lahadi ne –\n❌ Avoid trading\n✅ Prepare Weekly Zones\n🔍 Review last week's setups",
    'Monday': "🗓️ Yau Litinin ne –\n⚠️ Watch Accumulation / False BOS\n✅ Mark liquidity zones + structure\n❌ No early entry",
    'Tuesday': "🗓️ Yau Talata ne –\n✅ Wait for BOS confirmation\n✅ Enter based on 15min + 5min confluence\n💡 NY Open = sniper entry",
    'Wednesday': "🗓️ Yau Laraba ne –\n🔥 Most reliable day for entries\n✅ Breakout / Retest / SMC trades\n🎯 Continue/reverse Monday-Tuesday zone",
    'Thursday': "🗓️ Yau Alhamis ne –\n✅ Strong continuation from Wed\n⚠️ Be ready for profit-taking\n✅ Trail SL and manage",
    'Friday': "🗓️ Yau Jumma’a ne –\n⚠️ Exit before NY session close\n✅ Avoid late entries\n🧾 Trade review + journal update",
    'Saturday': "🗓️ Yau Asabar ne –\n❌ No trade (Crypto only, manipulated)\n✅ Backtest or Learn strategy"
}

def send_daily_reminder():
    today = datetime.now(pytz.timezone('Africa/Lagos')).strftime('%A')
    message = daily_messages.get(today, "No message for today.")
    bot.send_message(chat_id=USER_ID, text=message)

# Schedule job
scheduler = BlockingScheduler(timezone='Africa/Lagos')
scheduler.add_job(send_daily_reminder, trigger='cron', hour=9, minute=0)
scheduler.start()
