import discord
from discord.ext import commands


class Help(commands.Cog):
    """All help commands"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        '''A list of all commands'''
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


def setup(client):
    client.add_cog(Help(client))
