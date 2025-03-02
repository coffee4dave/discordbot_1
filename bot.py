# bot.py
import os
import discord
from discord.ext import tasks, commands
from dotenv import load_dotenv
from datetime import datetime

from flask import Flask
from threading import Thread

############################
# 1) LOAD DISCORD TOKEN
############################
# This loads from .env if present (for local dev),
# or from environment variables (like Replit Secrets).
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

############################
# 2) KEEP-ALIVE SERVER (REPLIT)
############################
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

def run_server():
    app.run(host='0.0.0.0', port=8080)

############################
# 3) DISCORD BOT SETUP
############################
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

############################
# 4) READ USER IDS FROM FILE
############################
with open("user_ids.txt", "r") as f:
    lines = f.read().splitlines()
USER_IDS = [int(line.strip()) for line in lines if line.strip().isdigit()]

############################
# 5) BOT EVENTS & TASKS
############################
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    # Start the daily message loop
    daily_message.start()

@tasks.loop(hours=24)
async def daily_message():
    today = datetime.now().strftime("%Y-%m-%d")
    message = f"Good morning, it's {today}!"
    for user_id in USER_IDS:
        try:
            user = await bot.fetch_user(user_id)
            await user.send(message)
            print(f"Sent daily message to {user_id}")
        except Exception as e:
            print(f"Error sending to {user_id}: {e}")

@daily_message.before_loop
async def before_daily_message():
    await bot.wait_until_ready()

############################
# 6) RUN APP & BOT
############################
if __name__ == "__main__":
    # Start the mini webserver for Replit keep-alive
    t = Thread(target=run_server)
    t.start()

    # Run the Discord bot
    bot.run(TOKEN)
