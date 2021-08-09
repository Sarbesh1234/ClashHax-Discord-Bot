import asyncio
import asyncpg
import os
import socket
import discord
from dotenv import load_dotenv
from discord.ext import commands

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
load_dotenv('discord.env')

if ip_address == os.getenv('MY_IP'):
    bearer = os.getenv('CLASH_HAX_TESTING_BEARER')
    BOT_TOKEN = os.getenv('BOT_TOKEN_HOME')
    POSTGRES_INFO = {'database': os.getenv("DATABASE"), 'user': os.getenv("USERR"), 'password': os.getenv("PASSWORD"),
                     'host': os.getenv("HOST")}
else:
    bearer = os.getenv('CLASH_HAX_BEARER')
    BOT_TOKEN = os.getenv('BOT_TOKEN_AWAY')
    POSTGRES_INFO = {'database': os.getenv("DATABASE"), 'user': os.getenv("USERR"), 'password': os.getenv("PASSWORD"),
                     'host': "localhost"}

headers = {
    'Content-Type': 'application/json',
    'Accepted': 'application/json',
    'authorization': 'Bearer ' + bearer
}


async def get_prefix(self, ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            prefix = await connection.fetchval("SELECT prefix FROM servers WHERE serverid = $1", ctx.guild.id)
            return prefix

intents = discord.Intents(messages=True, members=True, guilds=True, guild_messages=True)
client = commands.Bot(intents=intents, command_prefix=get_prefix, help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


loop = asyncio.get_event_loop()
client.pool = loop.run_until_complete(asyncpg.create_pool(**POSTGRES_INFO))
client.run(BOT_TOKEN)
