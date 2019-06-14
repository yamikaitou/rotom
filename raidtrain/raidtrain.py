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
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

        default_guild = {"category": 0, "copy": 0}
        self.config.register_guild(**default_guild)

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

    @checks.admin()
    @commands.group()
    async def rtset(self, ctx):
        """
            Various settings for RaidTrain
        """
        pass

    @rtset.command()
    async def category(self, ctx, category_id: discord.CategoryChannel):
        """
            Set the Category the RaidTrain channels are created in
        """
        await self.config.guild(ctx.guild).category.set(category_id.id)

    @rtset.command()
    async def permission(self, ctx, channel_id: discord.TextChannel):
        """
            Set the channel to copy permissions from
        """
        await self.config.guild(ctx.guild).copy.set(channel_id.id)
