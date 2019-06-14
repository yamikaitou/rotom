import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio


class RaidTrain(commands.Cog):
    """
    Rotom Raid Train
    """

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def raidtrain(self, ctx, number: int, *, name: str):
        """
            Creates Raid Train rooms
        """

        if isinstance(number, int) and number > 0:
            await ctx.send(
                "Creating {} channels named {}_group#".format(number, name.replace(" ", "-"))
            )
        else:
            await ctx.send("You must specify a number greater than 0")
