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
from discord.utils import find
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
else:
    bearer = 'CLASH_HAX_BEARER'
    BOT_TOKEN = os.getenv('BOT_TOKEN_AWAY')

POSTGRES_INFO = {'database': os.getenv("DATABASE"), 'user': os.getenv("USERR"), 'password': os.getenv("PASSWORD"),
                 'host': os.getenv("HOST")}

print(os.getenv("DATABASE"))
print(os.getenv("USERR"))
print(os.getenv("PASSWORD"))
print(os.getenv("HOST"))
headers = {
    'Content-Type': 'application/json',
    'Accepted': 'application/json',
    'authorization': 'Bearer ' + bearer
}


def get_role(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['role']


def link2(id, token):
    # response = requests.post('https://api.clashofclans.com/v1/players/%23' + id + '/verifytoken',headers=headers)
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


def get_clan_tag(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['clan']['tag']


def get_attacks_won(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['attackWins']


def get_defenses_won(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['defenseWins']


def get_highest_trophies(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['bestTrophies']


def get_bhall_tro(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['versusTrophies']


def get_bhall_wins(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['versusBattleWins']


def get_donations(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['donations']


def get_received(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['donationsReceived']


def get_clan_des(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['description']


def get_clan_tro(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['clanPoints']


def get_clan_btro(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['clanVersusPoints']


def get_clan_warwins(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['warWins']


def get_clan_warleauge(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['warLeague']['name']


def get_clan_warstreak(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['warWinStreak']


def get_clan_location(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['location']['name']


def get_clan_warlogpublic(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['isWarLogPublic']


def get_clan_warreq(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['requiredTrophies']


def get_clan_mem(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['members']


def get_clan_logo(id):
    string = get_clan_tag(id)
    string = string[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + string, headers=headers)
    json = response.json();
    return json['badgeUrls']['large']


def get_clan_name(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['clan']['name']


def get_user(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['name']


def get_thall(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['townHallLevel']


def get_bhall(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['builderHallLevel']


def get_highest_btro(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['bestVersusTrophies']


def get_explvl(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['expLevel']


def get_trophies(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['trophies']


def get_warstars(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['warStars']


def get_bk(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['heroes'][0]['level']


def get_aq(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['heroes'][1]['level']


def get_gw(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['heroes'][2]['level']


def get_heroes(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    num = len(user_json['heroes'])

    heroes = ''
    for x in range(num):
        if user_json['heroes'][x]['name'] == 'Barbarian King':
            heroes += "<:BK:822687680915308586> " + str(user_json['heroes'][x]['level'])
        elif user_json['heroes'][x]['name'] == 'Archer Queen':
            heroes += " <:AQ:822687698413289512> " + str(user_json['heroes'][x]['level'])
        elif user_json['heroes'][x]['name'] == 'Grand Warden':
            heroes += " <:GW:822687710509531156> " + str(user_json['heroes'][x]['level'])
        elif user_json['heroes'][x]['name'] == 'Royal Champion':
            heroes += " <:RC:822687723848073227> " + str(user_json['heroes'][x]['level'])

    return heroes


def check_bm(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    num = len(user_json['heroes'])
    bm = ''
    for x in range(num):
        if user_json['heroes'][x]['name'] == 'Battle Machine':
            bm = "<:bm:862948965129519134>" + '\t' + str(user_json['heroes'][x]['level'])
            break
    return bm


def get_rc(id):
    id = id[1:]
    response = requests.get('https://api.clashofclans.com/v1/players/%23' + id, headers=headers)
    user_json = response.json();
    return user_json['heroes'][3]['level']


def get_warlog():
    response = requests.get('https://api.clashofclans.com/v1/clans/%232PPLYJPG2/warlog', headers=headers)
    user_json2 = response.json();
    print(user_json2['name']);


def get_dono(id, num):
    hello = get_clan_tag(id)
    hello = hello[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    member = response.json();
    test = member
    data = json.loads(json.dumps(test))
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


def get_eachmember(id, num):
    hello = get_clan_tag(id)
    hello = hello[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    member = response.json();
    test = member
    data = json.loads(json.dumps(test))
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
        final += "\n" + str(data['items'][i]["name"])
    return final


def get_rec(id, num):
    hello = get_clan_tag(id)
    hello = hello[1:]
    response = requests.get('https://api.clashofclans.com/v1/clans/%23' + hello + '/members', headers=headers)
    member = response.json();
    test = member
    data = json.loads(json.dumps(test))
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


def get_bhall_emoji(tag):
    if get_bhall(tag) == 1:
        bhall = "<:b1:862937487093530645>"
    elif get_bhall(tag) == 2:
        bhall = "<:b2:862937487251996673>"
    elif get_bhall(tag) == 3:
        bhall = "<:b3:862937487760293889>"
    elif get_bhall(tag) == 4:
        bhall = "<:b4:862937487931736074>"
    elif get_bhall(tag) == 5:
        bhall = "<:b5:862937487734865931>"
    elif get_bhall(tag) == 6:
        bhall = "<:b6:862937488308699157>"
    elif get_bhall(tag) == 7:
        bhall = "<:b7:862937488633102386>"
    elif get_bhall(tag) == 8:
        bhall = "<:b8:862937488624320563>"
    else:
        bhall = "<:b9:862937488717119488>"
    return bhall


def get_thall_emoji(tag):
    if get_thall(tag) == 1:
        thall = "<:Town_Hall1:819094243242672159>"
    elif get_thall(tag) == 2:
        thall = "<:Town_Hall2:819094243444260874>"
    elif get_thall(tag) == 3:
        thall = "<:Town_Hall3:819094245549015060>"
    elif get_thall(tag) == 4:
        thall = "<:Town_Hall4:819094245402869781>"
    elif get_thall(tag) == 5:
        thall = "<:Town_Hall5:819094245671043112>"
    elif get_thall(tag) == 6:
        thall = "<:Town_Hall6:819094246769295370>"
    elif get_thall(tag) == 7:
        thall = "<:Town_Hall7:819094247365017600>"
    elif get_thall(tag) == 8:
        thall = "<:Town_Hall8:819094247260028948>"
    elif get_thall(tag) == 9:
        thall = "<:Town_Hall9:819094247583383552>"
    elif get_thall(tag) == 10:
        thall = "<:Town_Hall10:819094228000309248>"
    elif get_thall(tag) == 11:
        thall = "<:Town_Hall11:819094231087841310>"
    elif get_thall(tag) == 12:
        thall = "<:Town_Hall12:819094241660764200>"
    elif get_thall(tag) == 13:
        thall = "<:Town_Hall13:819094243536273461>"
    else:
        thall = "<:Town_Hall14:833756232375468032>"
    return thall


async def get_prefix(self, ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            prefix = await connection.fetchval("SELECT prefix FROM servers WHERE serverid = $1", ctx.guild.id)
            return prefix


print('bruh why you not work')
########################GUGUGUGUGUGUGUGUGUGUGUGU#####################

client = commands.Bot(command_prefix=get_prefix, help_command=None)


@client.command()
async def testing(ctx):
    await ctx.send("why you no work?")


@client.event
async def on_message(message):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            if message.content == '<@&863560351281709097>' or message.content == '<@&837221636779278377>':
                prefix = await connection.fetchval("SELECT prefix FROM servers WHERE serverid = $1", message.guild.id)
                await message.channel.send('The prefix for this server is ' + prefix)
    await client.process_commands(message)

@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


@client.event
async def on_guild_join(guild):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("INSERT INTO servers VALUES ($1,'!')", guild.id)
    #general = find(lambda x: x.name == 'general', guild.text_channels)
    #if general and general.permissions_for(guild.me).send_messages:
        #await general.send('Hey! Thanks for inviting ClashHax discord bot to your server.\nUse !help to bring a list of commands')




@client.event
async def on_guild_remove(guild):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("DELETE FROM servers WHERE serverid = $1", guild.id)


@client.command()
async def prefix(ctx, arg):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            await connection.execute("UPDATE servers SET prefix = $1 WHERE serverid = $2", arg, ctx.guild.id)
            await ctx.send("ClashHax prefix for this server has been changed to " + arg)


@client.command()
async def link_clan(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            # tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                clan_tag = await connection.fetchval("SELECT * FROM servers WHERE $1 = ANY(tag)", get_clan_tag(tag))
                if clan_tag is not None:
                    await ctx.send("Your clan is already linked to this discord server")
                    return
                if get_role(tag) == 'leader' or get_role(tag) == 'coLeader' or get_role(tag) == 'admin':
                    await connection.execute("UPDATE servers SET tag = array_append(tag,$1) WHERE serverid = $2",
                                             get_clan_tag(tag), ctx.guild.id)
                    await ctx.send(get_clan_name(tag) + " has been linked to your server")
                else:
                    await ctx.send("You need to be co-leader or leader to use this command")
            else:
                await ctx.send("Please use the link command before using this!")

@client.command()
async def invite(ctx):
    await ctx.send("The invite link for this discord bot is https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=8&scope=bot")

@client.command()
async def unlink_clan(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                if get_role(tag) == 'leader' or get_role(tag) == 'coLeader' or get_role(tag) == 'admin':
                    first = await connection.fetchval("SELECT tag[1] FROM servers WHERE serverid = $1", ctx.guild.id)
                    if first is not None:
                        # await connection.execute("UPDATE players SET tag = array_remove(tag,tag[1]) WHERE discordid = $1"
                        await connection.execute(
                            "UPDATE servers SET tag = array_remove(tag,tag[1]) WHERE serverid = $1", ctx.guild.id)
                        await ctx.send(get_clan_name(tag) + " has been unlinked from your server")
                    else:
                        await ctx.send("There are no more clans from your server to unlink")
                else:
                    await ctx.send("You need to be co-leader or leader to use this command")
            else:
                await ctx.send("Please use the link command before using this!")


@client.command()
async def link_help(ctx):
    embed = discord.Embed(title="Linking Help", color=0x4287f5)
    embed.add_field(name='\u200b',
                    value="\nPlease use the command `!link <in-game tag> <api token>`\nExample: `!link #YG2G8PVV 4ed32drw`",
                    inline=False)

    embed.add_field(name='\nWhere to find in-game tag?',
                    value="In the image below, the # with a series of letters is your player tag. Also, if you click the little arrow with a square, a pop up with a copy and share button will appear. Clicking copy, will copy your in-game tag to your clipboard. So now you can just paste it.")
    embed.set_image(url='https://cdn.discordapp.com/attachments/833745316401381419/862161173658206218/IMG_6506.PNG')
    await ctx.send(embed=embed)
    embed2 = discord.Embed(title="Linking Help Part 2", color=0x4287f5)
    embed2.add_field(name='\nWhere to find api token?',
                     value="Go to account settings and then click more settings. Scroll to the bottom and you'll see the api token Click the show button to the left of it and either use the copy button or type it manually. API token also changes frequently, so if it doesn't work, check the api token again. In the image below, I've circled the api token.")
    embed2.set_image(url='https://cdn.discordapp.com/attachments/833745316401381419/862172619552587796/IMG_6512_1.PNG')
    await ctx.send(embed=embed2)


@client.command(aliases=['linked'])
async def link(ctx, tag, token):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            test = await connection.fetchval("SELECT * FROM players WHERE $1 = ANY(tag)", tag)
            print(test)
            if test is not None:
                await ctx.send(get_user(tag) + " is already linked to this account")
                return
            x = link2(tag, token)
            if x is True:
                value = await connection.fetchval("SElECT 1 FROM players WHERE discordid = $1", ctx.author.id)
                if value is None:
                    await connection.execute("INSERT INTO players VALUES ($1,ARRAY[$2])", ctx.author.id, tag)

                else:
                    await connection.execute("UPDATE players SET tag = array_append(tag,$1) WHERE discordid = $2",
                                             tag, ctx.author.id)

                await ctx.send(get_user(tag) + " has been linked to your discord account!")
            else:
                await ctx.send(
                    "Please type in the correct format with the right info. If you need help linking your account, use this command `!link_help`")

            await ctx.message.delete()


@client.command()
async def help(ctx):
    des = """
    `!` is the default prefix. Your server might have changed it, so ping the bot to find out your prefix\n
    `!prefix <new prefix>` • Changes the prefix of the server to the new prefix\n
    `!link <in-game tag> <api token>` • Links a clash of clans account to your discord account\n
    `!link_help` • Gives specific information on how to use the link command\n
    `!player` • Gives your in-game player information\n
    `!change_active <in-game tag>` • Use this command to switch your active clash of clans account. Only applies to users with multiple clash accounts linked to their discord\n
    `!clan` • Gives your in-game clan information\n
    `!profile` • Gives all your clash of clan accounts linked to your discord\n
    `!dono_board` • Gives donations and requests of all members in your clan\n
    `!dono <number>` • The bot will give a top 'number' list of the best donors in your clan\n
    `!unlink` • Unlinks your active clash of clans account from this discord account
    """
    embed = discord.Embed(title="ClashHax Commands", description=des, color=0x4287f5)
    await ctx.send(embed=embed)


@client.command()
async def player(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                embed = discord.Embed(title=get_user(tag) + " (" + tag + ")",
                                      url="https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23" + tag[
                                                                                                                1:],
                                      color=0x4287f5)
                if get_role(tag) == 'admin':
                    string = 'elder'
                else:
                    string = get_role(tag)
                des = get_thall_emoji(tag) + "\t" + str(
                    get_thall(tag)) + "\t<:trophyy:841927127468605450>" + "\t" + str(
                    get_trophies(tag)) + "\t:crossed_swords:" + "\t" + str(
                    get_attacks_won(tag)) + "\t" + ":shield:" + "\t" + str(get_defenses_won(tag)) + "\n" + get_heroes(
                    tag) + "\nHighest Trophies: <:trophyy:841927127468605450>" + "\t" + str(get_highest_trophies(tag))
                embed.add_field(name='Home Base Info', value=des, inline=False)
                des = get_bhall_emoji(tag) + "\t" + str(
                    get_bhall(tag)) + "\t<:btrophy:841926856760360970>" + "\t" + str(
                    get_bhall_tro(tag)) + "\t" + ":crossed_swords:" + "\t" + str(get_bhall_wins(tag)) + "\t" + check_bm(
                    tag) + "\nHighest Versus Trophies: <:btrophy:841926856760360970>" + "\t" + str(get_bhall_tro(tag))
                embed.add_field(name='Builder Base Info', value=des, inline=False)
                des = "\n<:exp:819094248498266122>" + str(
                    get_explvl(tag)) + "\t:star:" + str(get_warstars(tag)) + "\n" + "Donations: " + str(
                    get_donations(tag)) + "\nReceived: " + str(
                    get_received(tag)) + "\n" + string.capitalize() + " of " + get_clan_name(
                    tag)
                embed.add_field(name='General', value=des, inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Please use the link command first.")


@client.command()
async def unlink(ctx):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                await connection.execute("UPDATE players SET tag = array_remove(tag,tag[1]) WHERE discordid = $1",
                                         ctx.author.id)
                await ctx.send(get_user(tag) + ' has been unlinked from your discord account')
            else:
                await ctx.send("Please use the link command first")
            size = await connection.execute("SELECT array_length(tag,1) FROM players WHERE discordid = $1",
                                            ctx.author.id)
            if size == 0:
                await connection.execute("DELETE FROM players WHERE discordid = $1", ctx.author.id)
                await ctx.send("You have no more clash account linked to your discord account!")


@client.command()
async def change_main(ctx, tag):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            test = await connection.fetchval("SELECT * FROM players WHERE $1 = ANY(tag)", tag)
            if test is None:
                await ctx.send("Please link the account first before using this command!")
            else:
                val = await connection.fetchval("SELECT array_position(tag,$1) FROM players WHERE discordid = $2", tag,
                                                ctx.author.id)
                print(val)
                await connection.execute("UPDATE players SET tag = array_remove(tag,tag[$1]) WHERE discordid = $2", val,
                                         ctx.author.id)
                await connection.execute("UPDATE players SET tag = array_prepend($1,tag) WHERE discordid = $2", tag,
                                         ctx.author.id)
                await ctx.send("Your active account is now " + get_user(tag))


@client.command()
async def profile(ctx):
    start_time = time.time()
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            size = await connection.fetchval("SELECT array_length(tag,1) FROM players WHERE discordid = $1",
                                             ctx.author.id)
            if size == 0:
                await ctx.send("Please use the link command first before using this command")
                return
            embed = discord.Embed(title="ClashHax Profile", color=0x4287f5)
            for i in range(1, size + 1):
                tag = await connection.fetchval("SElECT tag[$1] FROM players WHERE discordid = $2", i, ctx.author.id)
                if get_role(tag) == 'admin':
                    string = 'elder'
                else:
                    string = get_role(tag)
                des = "[" + get_user(
                    tag) + '\t' + tag + "](https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23" + tag[
                                                                                                                1:] + " \"In-Game Profile\")" + "\n<:exp:819094248498266122>" + str(
                    get_explvl(tag)) + "   " + get_thall_emoji(tag) + "\t<:trophyy:841927127468605450>" + str(
                    get_trophies(tag)) + "\t:star:" + str(get_warstars(tag)) + "\n" + get_heroes(
                    tag) + "\n" + string.capitalize() + " of " + get_clan_name(
                    tag) + '\n'
                if i == 1:
                    embed.add_field(name='\u200b', value="*ACTIVE*\n" + des, inline=False)
                else:
                    embed.add_field(name='\u200b', value=des, inline=False)
                embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
            await ctx.send(embed=embed)


@client.command()
async def dono_board(ctx):
    start_time = time.time()
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                embed = discord.Embed(title='Donation Leaderboard', color=0x4287f5)
                embed.add_field(name='Username', value=get_eachmember(tag, get_clan_mem(tag)), inline=True)
                embed.add_field(name='Donated', value=get_dono(tag, get_clan_mem(tag)), inline=True)
                embed.add_field(name='Received', value=get_rec(tag, get_clan_mem(tag)), inline=True)
                embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
                await ctx.send(embed=embed)
            else:
                await ctx.send("Please use the link command first before using this command")


@client.command()
async def dono(ctx, *args):
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                embed = discord.Embed(title='Donation Leaderboard', color=0x4287f5)
                if len(args) == 0:
                    embed.add_field(name='Rank #', value=get_rank(10), inline=True)
                    embed.add_field(name='Username', value=get_eachmember(tag, 10), inline=True)
                    embed.add_field(name='Donated', value=get_dono(tag, 10), inline=True)
                elif len(args) == 1:
                    if int(args[0]) > get_clan_mem(tag):
                        embed.add_field(name='Rank #', value=get_rank(get_clan_mem(tag)), inline=True)
                        embed.add_field(name='Username', value=get_eachmember(tag, get_clan_mem(tag)), inline=True)
                        embed.add_field(name='Donated', value=get_dono(tag, get_clan_mem(tag)))
                    elif int(args[0]) <= 0:
                        await ctx.send("Please pick a valid number")
                        return
                    else:
                        embed.add_field(name='Rank #', value=get_rank(int(args[0])), inline=True)
                        embed.add_field(name='Username', value=get_eachmember(tag, int(args[0])), inline=True)
                        embed.add_field(name='Donated', value=get_dono(tag, int(args[0])), inline=True)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Please link your account first before using this command")


@client.command()
async def clan(ctx):
    start_time = time.time()
    async with client.pool.acquire() as connection:
        async with connection.transaction():
            tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
            if tag is not None:
                if get_clan_warlogpublic(tag) is True:
                    warl = ':unlock: Warlog Public'
                else:
                    warl = ':lock: Warlog Private'
                embed = discord.Embed(title=get_clan_name(tag) + '   (' + get_clan_tag(tag) + ')', colour=0x4287f5)
                embed.description = get_clan_des(tag)
                embed.add_field(name='Clan Info', value='<:person:841562165928525854>' + str(
                    get_clan_mem(tag)) + '/50\n<:trophyy:841927127468605450>' + str(
                    get_clan_tro(tag)) + '\n<:btrophy:841926856760360970>' + str(get_clan_btro(tag)), inline=False)
                embed.add_field(name='War Info', value='<:wars:842075407436218368>' + str(
                    get_clan_warwins(tag)) + ' wars won' + '\n:white_check_mark:' + str(
                    get_clan_warstreak(tag)) + ' war win streak\n<:medal:842077219890135111>' + str(
                    get_clan_warleauge(tag)),
                                inline=False)
                embed.add_field(name='Location', value=':earth_africa:' + get_clan_location(tag), inline=False)
                embed.add_field(name='Clan Settings',
                                value=warl + '\n<:trophyy:841927127468605450>' + str(
                                    get_clan_warreq(tag)) + ' Required')
                embed.set_thumbnail(url=get_clan_logo(tag))
                embed.timestamp = datetime.utcnow()
                embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
                await ctx.send(embed=embed)
            else:
                await ctx.send("Please use the link command first before using this command")


loop = asyncio.get_event_loop()
client.pool = loop.run_until_complete(asyncpg.create_pool(**POSTGRES_INFO))
client.run(BOT_TOKEN)
