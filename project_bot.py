# Импорт всех библиотек
import os
import time
import disnake
import sqlite3
from dotenv import load_dotenv
from random import choice
from disnake.ext import commands
from pyrogram import Client
from disnake import ApplicationCommandInteraction

# Загружаем переменную окружения(наш токен)
load_dotenv()

db = sqlite3.connect('level.db')
sql = db.cursor()
db.commit()

dolgi = sqlite3.connect('dolgi.db')
sql_d = dolgi.cursor()
dolgi.commit()

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
        sql_d.execute("""CREATE TABLE IF NOT EXISTS dolgi (
                name TEXT,
                id INT,
                subjects TEXT
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
                    if sql_d.execute(f"SELECT id FROM dolgi WHERE id = {member.id}").fetchone() is None:
                        sql_d.execute(f"INSERT INTO dolgi VALUES ('{member}', {member.id}, '')")
                    if sql.execute(f"SELECT id FROM users WHERE id = {member.id}").fetchone() is None:
                        sql.execute(f"INSERT INTO users VALUES ('{member}', {member.id}, 0, 1)")
                    else:
                        pass

        db.commit()
        dolgi.commit()
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


@bot.slash_command(description='Расписание')
async def table(inter: ApplicationCommandInteraction, date: str = commands.Param(choices=["Сегодня", "Завтра", "Текущая неделя", "Следующая неделя"])):
    await inter.response.send_message("Please wait...")

    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')

    app = Client('me_client', api_id, api_hash)

    await app.start()
    await app.send_message('mirea_table_bot', date)
    time.sleep(1)
    async for message in app.get_chat_history('mirea_table_bot', 1):
        await inter.edit_original_message(message.text)
    await app.stop()


@bot.slash_command(description='Добавить долг')
async def add_dolg(interaction: disnake.ApplicationCommandInteraction, name: disnake.Member, subject: str):
    sql_d.execute(f"SELECT subjects FROM dolgi WHERE name = ?", (str(name),))
    subject = sql_d.fetchone()[0] + ' ' + subject
    sql_d.execute(f"UPDATE dolgi SET subjects = ? WHERE name = ?", (subject, str(name)))
    await interaction.response.send_message("Добавил!")
    dolgi.commit()


@bot.slash_command(description='Удалить долг')
async def delete_dolg(interaction: disnake.ApplicationCommandInteraction, name: disnake.Member, subject: str):
    for subjects in sql_d.execute(f"SELECT subjects FROM dolgi WHERE name = ?", (str(name),)).fetchone():
        if subject in subjects:
            sql_d.execute(f"SELECT subjects FROM dolgi WHERE name = ?", (str(name),))
            subjects = sql_d.fetchone()[0]
            subjects = subjects.replace(' ' + subject, '')
            sql_d.execute(f"UPDATE dolgi SET subjects = ? WHERE name = ?", (subjects, str(name)))
            await interaction.response.send_message("Удалил!")
            dolgi.commit()
    else:
        await interaction.response.send_message("Долг не найден")


@bot.slash_command(description='Посмотреть долги')
async def check_dolg(interaction: disnake.ApplicationCommandInteraction, name: disnake.Member):
    sql_d.execute(f"SELECT subjects FROM dolgi WHERE name = ?", (str(name),))
    subjects = sql_d.fetchone()[0]
    if subjects:
        await interaction.response.send_message(f"Долги пользователя {name}:\n{subjects}")
    else:
        await interaction.response.send_message("У пользователя отсутствуют долги")


# Запуск бота
bot.run(os.getenv('TOKEN'))
