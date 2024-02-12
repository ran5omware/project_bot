# Импорт всех библиотек
import os
import disnake
import sqlite3
from dotenv import load_dotenv
from random import choice
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

# Загружаем переменную окружения(наш токен)
load_dotenv()

db = sqlite3.connect('level.db')
sql = db.cursor()
db.commit()

# Создаем бота
bot = commands.Bot(command_prefix="/", help_command=None, intents=disnake.Intents.all())


# Тут будут все команды:

# Создаем событие запуска бота и запуск базы данных, в котором
#   в консоль выведется сообщение о том, что бот и база данных готовы к работе
@bot.event
async def on_ready():
    try:
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
                name TEXT,
                id INT,
                exp BIGINT,
                level INT
            )""")
    except:
        print('Возникла ошибка во время запуска базы данных')
    finally:
        print(f"Bot {bot.user} is ready to work!")
        db.commit()
        print('client connected')


# Игровая команда "Орел и решка"
@bot.slash_command(description="Сыграть в монеточку")
async def coin(ctx, side: str = commands.Param(choices=["орел", "решка"])):
    sides = ['орел', 'решка']
    botChoice = choice(sides)
    if botChoice == side and side == 'орел':
        embed = disnake.Embed(
            title="Выпал орёл, вы выиграли",
            description="Congratz!!!",
            colour=0xF0C43F,
        )
        embed.set_image(url="https://i.ibb.co/hVrnL9F/image.png")
        await ctx.send(embed=embed)

    elif botChoice == side and side == 'решка':
        embed = disnake.Embed(
            title="Выпала решка, вы выиграли",
            description="Congratz!!!",
            colour=0xF0C43F,
        )
        embed.set_image(url="https://i.ibb.co/tZq8GQ5/image.png")
        await ctx.send(embed=embed)

    elif botChoice != side and side == 'решка':
        embed = disnake.Embed(
            title="Выпал орёл, вы проиграли",
            description="unlucky",
            colour=0xF0C43F,
        )
        embed.set_image(url="https://i.ibb.co/hVrnL9F/image.png")
        await ctx.send(embed=embed)

    elif botChoice != side and side == 'орел':
        embed = disnake.Embed(
            title="Выпала решка, вы проиграли",
            description="unlucky",
            colour=0xF0C43F,
        )
        embed.set_image(url="https://i.ibb.co/tZq8GQ5/image.png")
        await ctx.send(embed=embed)


# Запуск бота
bot.run(os.getenv('TOKEN'))
