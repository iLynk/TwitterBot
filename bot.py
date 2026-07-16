import discord
from discord.ext import commands
import re

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

regex = re.compile(r"https?://(?:www\.)?(?:x\.com|twitter\.com)/([^\s]+)")

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if regex.search(message.content):
        nouveau = regex.sub(
            r"https://fxtwitter.com/\1",
            message.content
        )

        await message.delete()
        await message.channel.send(nouveau)

    await bot.process_commands(message)

bot.run(TOKEN)
