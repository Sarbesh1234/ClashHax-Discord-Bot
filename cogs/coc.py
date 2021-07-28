from datetime import datetime
import time
import discord
import requests
from discord.ext import commands

import main


class Coc(commands.Cog):
    """All clash of clan commands"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def link(self, ctx, tag, token):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                test = await connection.fetchval("SELECT * FROM players WHERE $1 = ANY(tag)", tag)
                response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=main.headers)
                user = response.json()
                if test is not None:
                    await ctx.send(user['name'] + " is already linked to this account")
                    return
                x = main.link2(tag, token)
                if x is True:
                    value = await connection.fetchval("SElECT 1 FROM players WHERE discordid = $1", ctx.author.id)
                    if value is None:
                        await connection.execute("INSERT INTO players VALUES ($1,ARRAY[$2])", ctx.author.id, tag)

                    else:
                        await connection.execute("UPDATE players SET tag = array_append(tag,$1) WHERE discordid = $2",
                                                 tag, ctx.author.id)

                    await ctx.send(user['name'] + " has been linked to your discord account!")
                else:
                    await ctx.send(
                        "Please type in the correct format with the right info. If you need help linking your account, use this command `!link_help`")

                await ctx.message.delete()

    @commands.command()
    async def unlink(self, ctx):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                tag = await connection.fetchval("SELECT tag FROM players WHERE discordid = $1", ctx.author.id)
                if tag is not None:
                    tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                    response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:],
                                            headers=main.headers)
                    user = response.json()
                    await connection.execute("UPDATE players SET tag = array_remove(tag,tag[1]) WHERE discordid = $1",
                                             ctx.author.id)
                    await ctx.send(user['name'] + ' has been unlinked from your discord account')
                else:
                    await ctx.send("Please use the link command first")
                size = await connection.execute("SELECT array_length(tag,1) FROM players WHERE discordid = $1",
                                                ctx.author.id)
                if size == 0:
                    await connection.execute("DELETE FROM players WHERE discordid = $1", ctx.author.id)
                    await ctx.send("You have no more clash account linked to your discord account!")

    @commands.command()
    async def profile(self, ctx):
        start_time = time.time()
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                size = await connection.fetchval("SELECT array_length(tag,1) FROM players WHERE discordid = $1",
                                                 ctx.author.id)
                if size == 0:
                    await ctx.send("Please use the link command first before using this command")
                    return
                embed = discord.Embed(title="ClashHax Profile", color=0x4287f5)
                for i in range(1, size + 1):
                    tag = await connection.fetchval("SElECT tag[$1] FROM players WHERE discordid = $2", i,
                                                    ctx.author.id)
                    response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:],
                                            headers=main.headers)
                    user = response.json()
                    if user['role'] == 'admin':
                        string = 'elder'
                    else:
                        string = user['role']
                    des = "[" + user[
                        'name'] + '\t' + tag + "](https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23" + tag[
                                                                                                                       1:] + " \"In-Game Profile\")" + "\n<:exp:819094248498266122>" + str(
                        user['expLevel']) + "   " + main.get_thall_emoji(
                        user) + "\t<:trophyy:841927127468605450>" + str(
                        user['trophies']) + "\t:star:" + str(user['warStars']) + "\n" + main.get_heroes(
                        user) + "\n" + string.capitalize() + " of " + user['clan']['name'] + '\n'
                    if i == 1:
                        embed.add_field(name='\u200b', value="*ACTIVE*\n" + des, inline=False)
                    else:
                        embed.add_field(name='\u200b', value=des, inline=False)
                    embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
                await ctx.send(embed=embed)

    @commands.command()
    async def change_active(self, ctx, tag):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                test = await connection.fetchval("SELECT * FROM players WHERE $1 = ANY(tag)", tag)
                if test is None:
                    await ctx.send("Please link the account first before using this command!")
                else:
                    val = await connection.fetchval("SELECT array_position(tag,$1) FROM players WHERE discordid = $2",
                                                    tag,
                                                    ctx.author.id)
                    print(val)
                    await connection.execute("UPDATE players SET tag = array_remove(tag,tag[$1]) WHERE discordid = $2",
                                             val,
                                             ctx.author.id)
                    await connection.execute("UPDATE players SET tag = array_prepend($1,tag) WHERE discordid = $2", tag,
                                             ctx.author.id)
                    response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:],
                                            headers=main.headers)
                    user = response.json()
                    await ctx.send("Your active account is now " + user['name'])

    @commands.command()
    async def dono_board(self, ctx):
        start_time = time.time()
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=main.headers)
                user = response.json()
                clan_url = (user['clan']['tag'])[1:]
                response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_url + '/members',
                                        headers=main.headers)
                clan = response.json()
                if tag is not None:
                    embed = discord.Embed(title='Donation Leaderboard', color=0x4287f5)
                    embed.add_field(name='Username', value=main.get_eachmember(clan, len(clan['items'])), inline=True)
                    embed.add_field(name='Donated', value=main.get_dono(clan, len(clan['items'])), inline=True)
                    embed.add_field(name='Received', value=main.get_rec(clan, len(clan['items'])), inline=True)
                    embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Please use the link command first before using this command")

    @commands.command()
    async def dono(self, ctx, *args):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                tag = await connection.fetchval("SElECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=main.headers)
                user = response.json()
                clan_url = (user['clan']['tag'])[1:]
                response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_url + '/members',
                                        headers=main.headers)
                clan = response.json()
                if tag is not None:
                    embed = discord.Embed(title='Donation Leaderboard', color=0x4287f5)
                    if len(args) == 0:
                        embed.add_field(name='Rank #', value=main.get_rank(10), inline=True)
                        embed.add_field(name='Username', value=main.get_eachmember(clan, 10), inline=True)
                        embed.add_field(name='Donated', value=main.get_dono(clan, 10), inline=True)
                    elif len(args) == 1:
                        if int(args[0]) > len(clan['items']):
                            embed.add_field(name='Rank #', value=main.get_rank(len(clan['items'])), inline=True)
                            embed.add_field(name='Username', value=main.get_eachmember(clan, len(clan['items'])),
                                            inline=True)
                            embed.add_field(name='Donated', value=main.get_dono(clan, len(clan['items'])))
                        elif int(args[0]) <= 0:
                            await ctx.send("Please pick a valid number")
                            return
                        else:
                            embed.add_field(name='Rank #', value=main.get_rank(int(args[0])), inline=True)
                            embed.add_field(name='Username', value=main.get_eachmember(clan, int(args[0])), inline=True)
                            embed.add_field(name='Donated', value=main.get_dono(clan, int(args[0])), inline=True)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Please link your account first before using this command")

    @commands.command()
    async def clan(self, ctx):
        start_time = time.time()
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=main.headers)
                user = response.json()
                clan_url = (user['clan']['tag'])[1:]
                response = requests.get('https://api.clashofclans.com/v1/clans/%23' + clan_url,
                                        headers=main.headers)
                clan = response.json()
                if tag is not None:
                    if clan['isWarLogPublic'] is True:
                        warl = ':unlock: Warlog Public'
                    else:
                        warl = ':lock: Warlog Private'
                    embed = discord.Embed(title=user['clan']['name'] + '   (' + user['clan']['tag'] + ')',
                                          colour=0x4287f5)
                    embed.description = clan['description']
                    embed.add_field(name='Clan Info', value='<:person:841562165928525854>' + str(
                        clan['members']) + '/50\n<:trophyy:841927127468605450>' + str(
                        clan['clanPoints']) + '\n<:btrophy:841926856760360970>' + str(clan['clanVersusPoints']),
                                    inline=False)
                    embed.add_field(name='War Info', value='<:wars:842075407436218368>' + str(
                        clan['warWins']) + ' wars won' + '\n:white_check_mark:' + str(
                        clan['warWinStreak']) + ' war win streak\n<:medal:842077219890135111>' + str(
                        clan['warLeague']['name']),
                                    inline=False)
                    embed.add_field(name='Location', value=':earth_africa:' + clan['location']['name'], inline=False)
                    embed.add_field(name='Clan Settings',
                                    value=warl + '\n<:trophyy:841927127468605450>' + str(
                                        clan['requiredTrophies']) + ' Required')
                    embed.set_thumbnail(url=clan['badgeUrls']['large'])
                    embed.timestamp = datetime.utcnow()
                    embed.set_footer(text=str(round(time.time() - start_time, 3)) + ' seconds')
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Please use the link command first before using this command")

    @commands.command()
    async def player(self, ctx):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                tag = await connection.fetchval("SELECT tag[1] FROM players WHERE discordid = $1", ctx.author.id)
                response = requests.get('https://api.clashofclans.com/v1/players/%23' + tag[1:], headers=main.headers)
                user = response.json()
                if tag is not None:
                    embed = discord.Embed(title=user['name'] + " (" + tag + ")",
                                          url="https://link.clashofclans.com/en?action=OpenPlayerProfile&tag=%23" + tag[
                                                                                                                    1:],
                                          color=0x4287f5)
                    if user['role'] == 'admin':
                        string = 'elder'
                    else:
                        string = user['role']
                    des = main.get_thall_emoji(user) + "\t" + str(
                        user['townHallLevel']) + "\t<:trophyy:841927127468605450>" + "\t" + str(
                        user['trophies']) + "\t:crossed_swords:" + "\t" + str(
                        user['attackWins']) + "\t" + ":shield:" + "\t" + str(
                        user['defenseWins']) + "\n" + main.get_heroes(
                        user) + "\nHighest Trophies: <:trophyy:841927127468605450>" + "\t" + str(user['bestTrophies'])
                    embed.add_field(name='Home Base Info', value=des, inline=False)
                    des = main.get_bhall_emoji(user) + "\t" + str(
                        user['builderHallLevel']) + "\t<:btrophy:841926856760360970>" + "\t" + str(
                        user['versusTrophies']) + "\t" + ":crossed_swords:" + "\t" + str(
                        user['versusBattleWins']) + "\t" + main.check_bm(
                        user) + "\nHighest Versus Trophies: <:btrophy:841926856760360970>" + "\t" + str(
                        user['bestVersusTrophies'])
                    embed.add_field(name='Builder Base Info', value=des, inline=False)
                    des = "\n<:exp:819094248498266122>" + str(
                        user['expLevel']) + "\t:star:" + str(user['warStars']) + "\n" + "Donations: " + str(
                        user['donations']) + "\nReceived: " + str(
                        user['donationsReceived']) + "\n" + string.capitalize() + " of " + user['clan']['name']
                    embed.add_field(name='General', value=des, inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Please use the link command first.")


def setup(client):
    client.add_cog(Coc(client))
