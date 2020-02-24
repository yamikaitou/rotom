import discord
from discord.ext import tasks
import random
from redbot.core import commands, Config, checks
import math


class Contests(commands.Cog):
    """
    Rotom's Contest management
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

        default_guild = {"active": 0, "channel": 0, "day": 0}
        default_global = {"1st": {"apple": [], "google": []}, "2nd": {"apple": [], "google": []}}

        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

    @commands.command()
    @checks.admin()
    async def photowinner(self, ctx):
        channel = self.bot.get_guild(331635573271822338).get_channel(457213943828447235)
        votes = {}
        users = {}

        async for message in channel.history():
            votes[message.id] = []
            users[message.id] = message.author.id
            reactions = message.reactions
            for reaction in reactions:
                async for vote in reaction.users():
                    votes[message.id].append(vote.id)

        master = {}
        for k, v in votes.items():
            master[k] = list(dict.fromkeys(v))
        for k, v in master.items():
            print(
                f"{self.bot.get_guild(331635573271822338).get_member(users[k]).display_name}: {len(v)}"
            )

    @commands.command()
    @checks.admin()
    async def photocontest(self, ctx, day: int):
        """Start a AR Photo Contest on the provided day"""

        if await self.config.guild(ctx.guild).active() == 1:
            await ctx.send("Error, Photo Contest already active")
            return

        await self.config.guild(ctx.guild).day.set(day)
        await self.config.guild(ctx.guild).active.set(1)
        # self.contest.start()

    @tasks.loop(minutes=1.0)
    async def contest(self):
        pass

    @contest.before_loop
    async def before_contest(self):
        await self.bot.wait_until_ready()
