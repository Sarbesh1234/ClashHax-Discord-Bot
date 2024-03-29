import discord
from discord.ext import commands


class Help(commands.Cog):
    """All help commands"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, ctx):
        '''A list of all commands'''
        des = """
            `!` is the default prefix. Your server might have changed it, so ping the bot to find out the bot's prefix for your server. If you still need help, join the [support server](https://discord.gg/GSvXNT5rSu).\n
            `!prefix <new prefix>` • Changes the prefix of the server to the new prefix\n
            `!link <player tag> <api token>` • Links a clash of clans account to your discord account\n
            `!link_help` • Gives specific information on how to use the link command\n
            `!profile` • Gives all your clash of clan accounts linked to your discord\n
            `!change_active <player tag>` • Use this command to switch your active clash of clans account\n
            `!player` • Gives your in-game player information\n
            `!player <player tag>` • Gives in-game player information of the provided player tag\n
            `!clan` • Gives your in-game clan information\n
            `!clan <clan tag>` • Gives in-game clan information of the provided clan tag\n 
            `!dono_board` • Gives donations and requests of all members in your clan\n
            `!dono_board <clan tag>` • Gives donations and requests of all members in the provided clan tag\n
            `!dono <number>` • The bot will give a top 'number' list of the best donors in your clan\n
            `!dono <number> <clan tag>` • The bot will give a top 'number'  list of the best donors of the provided clan tag\n
            `!unlink` • Unlinks your active clash of clans account from this discord account\n
            `!invite` • Gets invite link for the bot
            """
        embed = discord.Embed(title="ClashHax Commands", description=des, color=0x4287f5)
        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(error)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def link_help(self, ctx):
        embed = discord.Embed(title="Linking Help", color=0x4287f5)
        embed.add_field(name='\u200b',
                        value="\nPlease use the command `!link <player tag> <api token>`\nExample: `!link #YG2G8PVV 4ed32drw`",
                        inline=False)

        embed.add_field(name='\nWhere to find player tag?',
                        value="In the image below, the # with a series of letters is your player tag. Also, if you click the little arrow with a square, a pop up with a copy and share button will appear. Clicking copy, will copy your in-game tag to your clipboard. So now you can just paste it.")
        embed.set_image(url='https://cdn.discordapp.com/attachments/833745316401381419/862161173658206218/IMG_6506.PNG')
        await ctx.send(embed=embed)
        embed2 = discord.Embed(title="Linking Help Part 2", color=0x4287f5)
        embed2.add_field(name='\nWhere to find api token?',
                         value="Go to account settings and then click more settings. Scroll to the bottom and you'll see the api token Click the show button to the left of it and either use the copy button or type it manually. API token also changes frequently, so if it doesn't work, check the api token again. In the image below, I've circled the api token.")
        embed2.set_image(
            url='https://cdn.discordapp.com/attachments/833745316401381419/862172619552587796/IMG_6512_1.PNG')
        await ctx.send(embed=embed2)

    @link_help.error
    async def link_help_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send(error)


def setup(client):
    client.add_cog(Help(client))
