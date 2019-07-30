import discord
from redbot.core import commands, __version__, checks, Config


class Cog1(commands.Cog):
    """ Cog 1 """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cog1(self, ctx):
        """ I am Cog 1 """
        await ctx.send("Cog 1 Success")
