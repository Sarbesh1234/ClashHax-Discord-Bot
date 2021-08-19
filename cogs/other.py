import discord
from discord.ext import commands


class Other(commands.Cog):
    """Other commands that are not related to the coc commands"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, arg):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE servers SET prefix = $1 WHERE serverid = $2", arg, ctx.guild.id)
                await ctx.send("ClashHax prefix for this server has been changed to " + arg)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(error)

    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def invite(self, ctx):
        embed = discord.Embed(color=0x4287f5)
        #embed.description = "Click for the bot invite link [here] (https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=8&scope=bot)"
        embed.description = "[Click here for to invite bot](https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=289792&scope=bot)."
        await ctx.send(embed=embed)

    @invite.error
    async def invite_error(self, ctx, error):
        if isinstance(error,commands.BotMissingPermissions):
            await ctx.send(error)
            print(error)


def setup(client):
    client.add_cog(Other(client))