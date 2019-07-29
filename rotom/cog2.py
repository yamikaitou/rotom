import discord
from redbot.core import commands, __version__, checks, Config


class Cog2(commands.Cog):
    """ Cog 2 """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cog2(self, ctx):
        """ I am Cog 2 """
        await ctx.send("Cog 2 Success")
