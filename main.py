'''
conn = sqlite3.connect('clash.db')
c = conn.cursor()

c.execute("""CREATE TABLE extra (
          serverid VARCHAR(25) ,
            prefix VARCHAR(15) 
        )""")

conn.commit()

conn.close()


c.execute("""CREATE TABLE players (
          first author,
            last tag
         )""")

c.execute("""CREATE TABLE clans (
          first author,
          last tag
        )""")



c.execute("""CREATE TABLE testing2 (
          first VARCHAR(100) ,
            last varchar(100) 
         )""")



c.execute("""CREATE TABLE players (
          discordid VARCHAR(25) ,
            tag VARCHAR(15) 
        )""")





c.execute("""CREATE TABLE servers (
          serverid VARCHAR(25) ,
            clantag VARCHAR(15) 
         )""")


#c.execute("INSERT INTO servers (serverid,clantag) VALUES (?, ?)", (833143732949483581, '#2PPLYJPG2'))
#c.execute("DELETE FROM servers")

c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (405188930527559680, '#YG2G8PVV'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (811465843091177502, '#PJQUL2JPY'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (365329172815675394, '#CJGY8PGR'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (226310909264396288, '#J8L8CQ28'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (353735428278452227, '#2VCUV8LVL'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (244911148871188480, '#JC9GVJ9V'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (750109340211347556, '#Q9RRYL98'))
c.execute("INSERT INTO players (discordid,tag) VALUES (?, ?)", (751628343845060700, '#98LURJ0LP'))


#c.execute("SELECT * FROM clash WHERE last ='dinka'")

#print(c.fetchall())

conn.commit()

conn.close()
'''
import asyncio
import asyncpg
import requests
import json
import discord
import time
from dotenv import load_dotenv
import os
from discord.ext import commands
from datetime import datetime
import socket

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


def link2(id, token):
    id = id[1:]
    params = {
        "token": token
    }
    response = requests.post('https://api.clashofclans.com/v1/players/%23' + id + '/verifytoken',
                             data=json.dumps(params), headers=headers)
    user_json = response.json()
    if user_json['status'] == 'ok':
        return True
    else:
        return False


def get_heroes(json):
    num = len(json['heroes'])

    heroes = ''
    for x in range(num):
        if json['heroes'][x]['name'] == 'Barbarian King':
            heroes += "<:BK:822687680915308586> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Archer Queen':
            heroes += " <:AQ:822687698413289512> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Grand Warden':
            heroes += " <:GW:822687710509531156> " + str(json['heroes'][x]['level'])
        elif json['heroes'][x]['name'] == 'Royal Champion':
            heroes += " <:RC:822687723848073227> " + str(json['heroes'][x]['level'])

    return heroes


def check_bm(json):
    num = len(json['heroes'])
    bm = ''
    for x in range(num):
        if json['heroes'][x]['name'] == 'Battle Machine':
            bm = "<:bm:862948965129519134>" + '\t' + str(json['heroes'][x]['level'])
            break
    return bm


def get_dono(clan_json, num):
    # hello = get_clan_tag(id)
    # hello = hello[1:]
    # response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    # member = response.json();
    # test = member
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    # dono_2 = list(range(0,num))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        # print("Username: " + data['items'][i]["name"].ljust(17) + "Donations: " + str(data['items'][i]["donations"]))
        # final+="\n"  + data['items'][i]["name"] + "Donations: ".rjust(length) + str(data['items'][i]["donations"])
        final += "\n" + str(data['items'][i]["donations"])

    return final


def get_rank(num):
    string = ""
    for i in range(num):
        string += "\n" + str(i + 1)
    return string


def get_eachmember(clan_json, num):
    # hello = get_clan_tag(clan_json)
    # hello = hello[1:]
    # response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    # member = response.json();
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        final += "\n" + str(data['items'][i]["name"])
    return final


def get_rec(clan_json, num):
    # hello = get_clan_tag(id)
    # hello = hello[1:]
    # response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    # member = response.json();
    # test = member
    data = json.loads(json.dumps(clan_json))
    dono = list(range(0, len(data['items'])))
    # dono_2 = list(range(0, num))
    final = ""
    for i in range(len(dono)):
        max = i
        for j in range(i + 1, len(dono)):
            if data['items'][dono[max]]['donations'] < data['items'][dono[j]]['donations']:
                max = j
        dono[i], dono[max] = dono[max], dono[i]
    for i in dono[:num]:
        final += "\n" + str(data['items'][i]["donationsReceived"])
    return final


def get_bhall_emoji(json):
    if json['builderHallLevel'] == 1:
        bhall = "<:b1:862937487093530645>"
    elif json['builderHallLevel'] == 2:
        bhall = "<:b2:862937487251996673>"
    elif json['builderHallLevel'] == 3:
        bhall = "<:b3:862937487760293889>"
    elif json['builderHallLevel'] == 4:
        bhall = "<:b4:862937487931736074>"
    elif json['builderHallLevel'] == 5:
        bhall = "<:b5:862937487734865931>"
    elif json['builderHallLevel'] == 6:
        bhall = "<:b6:862937488308699157>"
    elif json['builderHallLevel'] == 7:
        bhall = "<:b7:862937488633102386>"
    elif json['builderHallLevel'] == 8:
        bhall = "<:b8:862937488624320563>"
    else:
        bhall = "<:b9:862937488717119488>"
    return bhall


def get_thall_emoji(json):
    if json['townHallLevel'] == 1:
        thall = "<:Town_Hall1:819094243242672159>"
    elif json['townHallLevel'] == 2:
        thall = "<:Town_Hall2:819094243444260874>"
    elif json['townHallLevel'] == 3:
        thall = "<:Town_Hall3:819094245549015060>"
    elif json['townHallLevel'] == 4:
        thall = "<:Town_Hall4:819094245402869781>"
    elif json['townHallLevel'] == 5:
        thall = "<:Town_Hall5:819094245671043112>"
    elif json['townHallLevel'] == 6:
        thall = "<:Town_Hall6:819094246769295370>"
    elif json['townHallLevel'] == 7:
        thall = "<:Town_Hall7:819094247365017600>"
    elif json['townHallLevel'] == 8:
        thall = "<:Town_Hall8:819094247260028948>"
    elif json['townHallLevel'] == 9:
        thall = "<:Town_Hall9:819094247583383552>"
    elif json['townHallLevel'] == 10:
        thall = "<:Town_Hall10:819094228000309248>"
    elif json['townHallLevel'] == 11:
        thall = "<:Town_Hall11:819094231087841310>"
    elif json['townHallLevel'] == 12:
        thall = "<:Town_Hall12:819094241660764200>"
    elif json['townHallLevel'] == 13:
        thall = "<:Town_Hall13:819094243536273461>"
    else:
        thall = "<:Town_Hall14:833756232375468032>"
    return thall


async def get_prefix(self, ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            prefix = await connection.fetchval("SELECT prefix FROM servers WHERE serverid = $1", ctx.guild.id)
            return prefix


########################GUGUGUGUGUGUGUGUGUGUGUGU#####################

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
