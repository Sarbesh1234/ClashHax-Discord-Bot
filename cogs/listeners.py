import discord
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
    #@commands.bot_has_permissions(=True)
    async def on_guild_join(self, guild):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("INSERT INTO servers VALUES ($1,'!')", guild.id)
                print(guild.channels[0])
                channel = guild.text_channels[0]
                embed = discord.Embed(color=0x4287f5)
                embed.description = 'Hello There! Thanks for inviting ClashHax discord bot. The prefix of this bot is `!`. It can be changed with `!prefix <new prefix>`.\n• If you woud like to see a full list of commands, please use `!help`\n• For more help and updates on the bot, join the [support server](https://discord.gg/GSvXNT5rSu)\n• Share the bot with your friends! [Bot Invite](https://discord.com/api/oauth2/authorize?client_id=815078901574795276&permissions=8&scope=bot)'
                try:
                    await channel.send(embed=embed)
                except:
                    print('no perms to send embed')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        async with self.client.pool.acquire() as connection:
            async with connection.transaction():
                await connection.execute("DELETE FROM servers WHERE serverid = $1", guild.id)


def setup(client):
    client.add_cog(Listeners(client))
