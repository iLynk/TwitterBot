import os
import re
import discord
from discord.ext import commands
from dotenv import load_dotenv

# ============================
# Chargement du token
# ============================

load_dotenv()
TOKEN = os.getenv("TOKEN")

# ============================
# Configuration du bot
# ============================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ============================
# Plateformes supportées
# ============================

PLATFORMS = {
    "x.com": {
        "replace": "fxtwitter.com",
        "emoji": "🐦",
        "texte": "a partagé un tweet"
    },
    "twitter.com": {
        "replace": "fxtwitter.com",
        "emoji": "🐦",
        "texte": "a partagé un tweet"
    },
    "instagram.com": {
        "replace": "ddinstagram.com",
        "emoji": "📸",
        "texte": "a partagé une publication Instagram"
    },
    "reddit.com": {
        "replace": "vxreddit.com",
        "emoji": "👽",
        "texte": "a partagé un post Reddit"
    },
    "tiktok.com": {
        "replace": "tnktok.com",
        "emoji": "💩",
        "texte": "a partagé un tiktok"
    },
}

# ============================
# Détection des liens
# ============================

regex = re.compile(
    r"https?://(?:www|vm|vt\.)?(x\.com|twitter\.com|instagram\.com|reddit\.com|tiktok\.com)(/[^\s]*)",
    re.IGNORECASE
)

# ============================
# Fonction de remplacement
# ============================

def remplacer_liens(texte: str):

    emoji = "🔗"
    description = "a partagé un lien"

    def remplacement(match):
        nonlocal emoji
        nonlocal description

        domaine = match.group(1).lower()
        chemin = match.group(2)

        info = PLATFORMS[domaine]

        emoji = info["emoji"]
        description = info["texte"]

        return f"https://{info['replace']}{chemin}"

    nouveau_texte = regex.sub(remplacement, texte)

    return nouveau_texte, emoji, description

# ============================
# Bot prêt
# ============================

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

# ============================
# Nouveau message
# ============================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    nouveau_message, emoji, description = remplacer_liens(message.content)

    if nouveau_message != message.content:

        try:
            await message.delete()
        except discord.Forbidden:
            print("❌ Impossible de supprimer le message.")

        try:
            await message.channel.send(
                f"{emoji} **{message.author.display_name}** {description}\n"
                f"────────────────────\n"
                f"{nouveau_message}"
            )
        except discord.Forbidden:
            print("❌ Impossible d'envoyer un message.")

    await bot.process_commands(message)

# ============================
# Lancement
# ============================

bot.run(TOKEN)
