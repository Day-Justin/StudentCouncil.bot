import nextcord
from nextcord.ext import commands


class Help(commands.Cog):
    def __int__(self, bot):
        self.bot = bot

        self.help_msg = """
        '''
        k
        '''
        """

        self.text_channel_text = []

        @commands.Cog.listener()
        async def on_ready():
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    self.text_channel_text.append(channel)

            await self.send_to_all(self.help_msg )

        async def send_to_all(self, msg):
            for text_channel in self.text_channel_text:
                await text_channel.send(msg)

        @commands.command(name='help', aliases=['h', 'Help'])
        async def help(self, ctx):
            await ctx.send(self.help_msg)


def setup(client):
    client.add_cog(Help(client))