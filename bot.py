import discord
import os
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
eastern = timezone("America/New_York")

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

counter_file = "counter.txt"

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

    # Dynamically find a text channel where the bot can send messages
    channel = None
    for guild in bot.guilds:
        for text_channel in guild.text_channels:
            if text_channel.permissions_for(guild.me).send_messages:
                channel = text_channel
                break
        if channel:
            break

    if channel is None:
        print("❌ No suitable channel found.")
        await bot.close()
        return

    # Load streak + image + fact
    day_count = read_streak() + 1
    write_streak(day_count)

    with open("facts.txt", "r", encoding="utf-8") as f:
        facts = [line.strip() for line in f.readlines() if line.strip()]
    fact = facts[(day_count - 1) % len(facts)]

    image_dir = "images"
    image_files = sorted([file for file in os.listdir(image_dir) if file.lower().endswith(('.jpg', '.png', '.jpeg'))])
    image_path = os.path.join(image_dir, image_files[(day_count - 1) % len(image_files)])

    with open(image_path, 'rb') as img:
        file = discord.File(img)
        await channel.send(f"📅 **Day {day_count} of the Manul Streak!**\n📸 **Manul of the Day #MOTD** 🐾\n*{fact}*", file=file)

    print(f"✅ Posted to {channel.guild.name} > #{channel.name}. Shutting down.")
    await bot.close()

bot.run(TOKEN)
