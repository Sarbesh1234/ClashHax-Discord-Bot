import asyncio
import asyncpg
import os
import socket
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


client = commands.Bot(command_prefix=get_prefix, help_command=None)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


@client.command()
async def prefix(ctx, arg):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("UPDATE servers SET prefix = $1 WHERE serverid = $2", arg, ctx.guild.id)
            await ctx.send("ClashHax prefix for this server has been changed to " + arg)

@client.command()
async def invite(ctx):
    await ctx.send(
        "The invite link for this discord bot is https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=8&scope=bot")
'''
@client.command()
async def link_clan(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=headers)
            user = response.json()
            # tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                clan_tag = await connection.fetchval("SELECT * FROM servers WHERE $1 = ANY(tag)", user['clan']['tag'])
                if clan_tag is not None:
                    await ctx.send("Your clan is already linked to this discord server")
                    return
                if user['role'] == 'leader' or user['role'] == 'coLeader':
                    await connection.execute("UPDATE servers SET tag = array_append(tag,$1) WHERE serverid = $2",
                                             user['clan']['tag'], ctx.guild.id)
                    await ctx.send(user['clan']['tag'] + " has been linked to your server")
                else:
                    await ctx.send("You need to be co-leader or leader to use this command")
            else:
                await ctx.send("Please use the link command before using this!")


@client.command()
async def unlink_clan(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=headers)
            user = response.json()
            if tag is not None:
                if user['tag'] == 'leader' or user['tag'] == 'coLeader':
                    first = await connection.fetchval("SELECT tag[1] FROM servers WHERE serverid = $1", ctx.guild.id)
                    if first is not None:
                        # await connection.execute("UPDATE players SET tag = array_remove(tag,tag[1]) WHERE discordid = $1"
                        await connection.execute(
                            "UPDATE servers SET tag = array_remove(tag,tag[1]) WHERE serverid = $1", ctx.guild.id)
                        await ctx.send(user['clan']['tag'] + " has been unlinked from your server")
                    else:
                        await ctx.send("There are no more clans from your server to unlink")
                else:
                    await ctx.send("You need to be co-leader or leader to use this command")
            else:
                await ctx.send("Please use the link command before using this!")

'''

loop = asyncio.get_event_loop()
client.pool = loop.run_until_complete(asyncpg.create_pool(**POSTGRES_INFO))
client.run(BOT_TOKEN)
