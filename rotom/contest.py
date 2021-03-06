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
        default_global = {
            "first": {"apple": [], "google": []},
            "second": {"apple": [], "google": []},
        }

        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)
    
    @commands.Cog.listener()
    @checks.is_owner()
    @commands.guild_only()
    async def on_raw_reaction_add(self, payload):
        pass
    
    @commands.command()
    @checks.is_admin_or_superior()
    async def contest(self, ctx, day: str, kind: int = None):
        """
        Trigger a contest for Community Day

        day = sat or sun
        kind = Contest type value, blank will pick randomly
        """
        if day not in ("sat", "sun"):
            raise discord.ext.commands.BadArgument(message="day must be either sat or sun")

        if kind is None or kind < 1 or kind > 6:
            kind = __import__('secrets').choice(range(1,7))
        
        


        


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
        prints = []
        for k, v in votes.items():
            master[k] = list(dict.fromkeys(v))
        for k, v in master.items():
            prints.append(f"{self.bot.get_guild(331635573271822338).get_member(users[k]).display_name}: {len(v)}")
        
        await ctx.send(prints)

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
