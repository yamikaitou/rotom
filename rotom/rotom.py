import discord
import random
from redbot.core import (
    commands,
    Config,
    checks,
    data_manager,
    __version__,
    VersionInfo,
    version_info as red_version_info,
)
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
import aiobotocore
from typing import Union
import math
import json
from .emoji import *
import datetime
import aiohttp
import sys


class Rotom(commands.Cog):
    """
    Core Rotom commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.bot.config = Config.get_conf(
            self, identifier=192153481165930496, force_registration=True
        )
        default_guild = {
            "ex": {"active": [], "channel": 0, "bucket": ""},
            "raids": {"channel": 0},
            "train": {
                "category": 0,
                "mimic": 0,
                "day": [],
                "hour": [],
                "clean": {"day": 0, "hour": 0},
            },
            "auto": {
                "rare": [],
                "tgr": [],
                "research": [],
                "state": {"rare": 0, "tgr": 0, "research": 0, "nest": 0},
            },
        }
        default_global = {"raids": {"active": {}, "timer": 60}}
        self.bot.config.register_guild(**default_guild)
        self.bot.config.register_global(**default_global)

    @commands.command(name="help2")
    async def rotomhelp(self, ctx):
        """
        Rotom's Custom Help command
        """
        pass

    @commands.command(name="info")
    async def rotominfo(self, ctx):
        """
        Red's info command modified for Rotom
        """
        author_repo = "https://github.com/Twentysix26"
        org_repo = "https://github.com/Cog-Creators"
        red_repo = org_repo + "/Red-DiscordBot"
        red_pypi = "https://pypi.python.org/pypi/Red-DiscordBot"
        support_server_url = "https://discord.gg/red"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        rotom_repo = "https://github.com/yamikaitou/rotom"
        since = datetime.datetime(2016, 1, 2, 0, 0)
        days_since = (datetime.datetime.utcnow() - since).days
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        python_version = "[{}.{}.{}]({})".format(*sys.version_info[:3], python_url)
        red_version = "[{}]({})".format(__version__, red_pypi)
        app_info = await self.bot.application_info()
        owner = app_info.owner
        custom_info = await self.bot.db.custom_info()

        async with aiohttp.ClientSession() as session:
            async with session.get("{}/json".format(red_pypi)) as r:
                data = await r.json()
        outdated = VersionInfo.from_str(data["info"]["version"]) > red_version_info
        about = (
            "This is an instance of [Red, an open source Discord bot]({}) "
            "(which was created by [Twentysix]({}) and [improved by many]({})).\n"
            "Red is backed by a passionate community who contributes and "
            "creates content for everyone to enjoy. [Join us today]({}) "
            "and help us improve!\n"
            "Red has been bringing joy since 02 Jan 2016 (over {} days ago!)\n\n"
            "Rotom is built using Cogs with Red as the underlying framework.\n"
            "While a lot of what makes up Rotom is custom designed for specific Pokemon Go servers, it is open-sourced.\n"
            "You can view it and contribute back on [GitHub]({})"
        ).format(red_repo, author_repo, org_repo, support_server_url, days_since, rotom_repo)

        embed = discord.Embed(color=(await ctx.embed_colour()))
        embed.add_field(name=("Instance owned by"), value=str(owner))
        embed.add_field(name="Python", value=python_version)
        embed.add_field(name="discord.py", value=dpy_version)
        embed.add_field(name=("Red version"), value=red_version)
        if outdated:
            embed.add_field(
                name=("Outdated"), value=("Yes, {} is available").format(data["info"]["version"])
            )
        if custom_info:
            embed.add_field(name=_("About this instance"), value=custom_info, inline=False)
        embed.add_field(name=("About Red & Rotom"), value=about, inline=False)

        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(("I need the `Embed links` permission to send this"))

    @checks.admin()
    @commands.group()
    async def rotom(self, ctx):
        """
        Rotom's Core Command
        """
        pass

    @rotom.group()
    async def set(self, ctx):
        """
        Set stuff
        """
        pass

    @set.group()
    async def raids(self, ctx):
        """
        Set settings for Raid creation/management
        """
        pass

    @raids.command(name="channel")
    async def raidchannel(self, ctx, chan: discord.TextChannel = None):
        """
        Set the channel for Raid Creation commands
        """
        if chan is None:
            chan = ctx.channel

        await self.bot.config.guild(ctx.guild).raids.channel.set(chan.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @raids.command(name="timer")
    async def raidtimer(self, ctx, timer: int):
        """
        Set the Raid timer
        """

        await self.bot.config.raids.timer.set(timer)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @set.group()
    async def ex(self, ctx):
        """
        Set settings for EXRaid creation/management
        """
        pass

    @ex.command(name="channel")
    async def exchannel(self, ctx, chan: discord.TextChannel = None):
        """
        Set the channel for EXRaid Creation commands
        """
        if chan is None:
            chan = ctx.channel

        await self.bot.config.guild(ctx.guild).ex.channel.set(chan.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @ex.command()
    async def bucket(self, ctx, bucket: str):
        """
        Set the channel for EXRaid Creation AWS Bucket
        """

        await self.bot.config.guild(ctx.guild).ex.bucket.set(bucket)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @set.group()
    async def train(self, ctx):
        """
        Set settings for Raid Train creation/management
        """
        pass

    @train.command(name="category")
    async def traincategory(self, ctx, cat: discord.CategoryChannel = None):
        """
        Set the Category the RaidTrain channels are created in
        """
        await self.bot.config.guild(ctx.guild).train.category.set(cat.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @train.command(name="mimic")
    async def trainmimic(self, ctx, mimic: discord.TextChannel = None):
        """
        Set the channel to copy permissions from for RaidTrains
        """

        if mimic is None:
            mimic = ctx.channel

        await self.bot.config.guild(ctx.guild).train.mimic.set(mimic.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
