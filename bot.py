import discord
import os
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from datetime import datetime, timedelta

TOKEN = "MTM1NDEyNzY0MzEyMDg5ODExOQ.G8C1sc.UZS_GS8spIcDhLUcf_YGUW-Xek7FXlhypB7f8s"
CHANNEL_ID = 1354128166561517591  # Replace with your channel ID

eastern = timezone("America/New_York")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Load facts and images
with open("facts.txt", "r", encoding="utf-8") as f:
    facts = [line.strip() for line in f.readlines() if line.strip()]

image_dir = "images"
image_files = sorted([file for file in os.listdir(image_dir) if file.lower().endswith(('.jpg', '.png', '.jpeg'))])

index = 0
scheduler = AsyncIOScheduler()
counter_file = "counter.txt"

# Read or create streak counter
def read_streak():
    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("0")
        return 0
    with open(counter_file, "r") as f:
        return int(f.read().strip())

def write_streak(count):
    with open(counter_file, "w") as f:
        f.write(str(count))

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    scheduler.start()

    # For daily use (use this after testing)
    scheduler.add_job(post_motd, 'cron', hour=12, minute=0, timezone=eastern)
    print("📅 Scheduled daily MOTD at 12:00 PM Eastern Time.")

@bot.command()
async def motd(ctx):
    print("🛠️ Manual MOTD command used.")
    await post_motd()

async def post_motd():
    global index
    print("📤 Attempting to post MOTD...")

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ Channel not found! Check your CHANNEL_ID.")
        return

    try:
        # Read and increment streak
        day_count = read_streak() + 1
        write_streak(day_count)

        fact = facts[index % len(facts)]
        image_path = os.path.join(image_dir, image_files[index % len(image_files)])

        print(f"📸 Using image: {image_path}")
        print(f"📘 Using fact: {fact}")
        print(f"📆 Streak day: {day_count}")

        with open(image_path, 'rb') as img:
            file = discord.File(img)
            await channel.send(f"📅 **Day {day_count} of the Manul Streak!**\n📸 **Manul of the Day #MOTD** 🐾\n*{fact}*", file=file)

        index += 1
        print("✅ MOTD sent successfully!")
    except Exception as e:
        print("⚠️ Error in post_motd:", e)

bot.run(TOKEN)
