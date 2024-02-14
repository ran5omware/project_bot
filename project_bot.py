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

# level_limit = dict[
#     0: 0,
#     1: 50,
#     2: 150
# ]

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

        for guild in bot.guilds:
            for member in guild.members:
                if member.bot:
                    pass
                else:
                    if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                        sql.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 1)")
                    else:
                        pass

        db.commit()
        print('client connected')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    sql.execute("UPDATE users SET exp = exp + 10 WHERE id = {}".format(message.author.id))
    db.commit()
    cur_lvl = sql.execute("SELECT level FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]
    cur_exp = sql.execute("SELECT exp FROM users WHERE id = {}".format(message.author.id)).fetchone()[0]
    if int((cur_exp - 50) / 100) + 1 > cur_lvl:
        sql.execute("UPDATE users SET level = level + 1 WHERE id = {}".format(message.author.id))
        sql.execute("UPDATE users SET exp = 0 WHERE id = {}".format(message.author.id))
        await message.channel.send(f"Поздравляю, {message.author.mention}, ваш уровень повышен до {cur_lvl + 1}")


# Команда для просмотра уровня
@bot.slash_command(description='Посмотреть уровень')
async def level_check(ctx, member: disnake.Member):
    try:
        level = sql.execute("SELECT level FROM users WHERE id = {}".format(member.id)).fetchone()[0]
        # exp = sql.execute("SELECT exp FROM users WHERE id = {}".format(member.id)).fetchone()[0]
        embed = disnake.Embed(
            title=f'{member}',
            description=f'**{level} уровень**',
            color=disnake.Colour.yellow(),
        )
        # embed.add_field(name='', value=f'*{exp} exp*')
        await ctx.send(embed=embed)
    except:
        await ctx.send('Невозможно посмотреть уровень у бота')


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
