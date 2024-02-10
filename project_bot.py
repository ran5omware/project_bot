# Импорт всех библиотек
import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

# Загружаем переменную окружения(наш токен)
load_dotenv()

# Создаем бота
bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())


# Тут будут все команды:

# Создаем событие запуска бота, в котором в консоль выведется сообщение о том, что бот готов к работе
@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready to work!")


# Запуск бота
bot.run(os.getenv('TOKEN'))
