from discord.ext import commands


class Listeners(commands.Cog):
    """All listener events"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user.mentioned_in(message):
            async with self.client.pool.acquire() as connection:
                async with connection.transaction():
                    prefix = await connection.fetchval("SELECT prefix FROM servers WHERE serverid = $1",
                                                       message.guild.id)
                    await message.channel.send('The prefix for this server is `' + prefix + '`')

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is ready.')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("INSERT INTO servers VALUES ($1,'!')", guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM servers WHERE serverid = $1", guild.id)


def setup(client):
    client.add_cog(Listeners(client))
