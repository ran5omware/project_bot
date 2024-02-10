import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

load_dotenv()

bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")


bot.run(os.getenv('TOKEN'))
