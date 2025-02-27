# bot.py
import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # We'll set these in Replit or .env

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

USER_IDS = [
    843965418724130826,  # Example user IDs
    696438148267245609
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    daily_message.start()

@tasks.loop(hours=24)
async def daily_message():
    today = datetime.now().strftime("%Y-%m-%d")
    text = f"Good morning, it's {today}!"
    for user_id in USER_IDS:
        try:
            user = await bot.fetch_user(user_id)
            await user.send(text)
            print(f"Sent daily message to {user_id}")
        except Exception as e:
            print(f"Error sending to {user_id}: {e}")

@daily_message.before_loop
async def before_daily_message():
    await bot.wait_until_ready()
    


if __name__ == "__main__":
    bot.run(TOKEN)



