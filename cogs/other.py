from discord.ext import commands


class Other(commands.Cog):
    """Other commands that are not related to the coc commands"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def prefix(self, ctx, arg):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("UPDATE servers SET prefix = $1 WHERE serverid = $2", arg, ctx.guild.id)
                await ctx.send("ClashHax prefix for this server has been changed to " + arg)

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(
            "The invite link for this discord bot is https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=8&scope=bot")

def setup(client):
    client.add_cog(Other(client))