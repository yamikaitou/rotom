import discord
import random
from redbot.core import commands, Config, checks, data_manager
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
import aiobotocore
from typing import Union
import math
import json
from .emoji import *


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
            "raids": {"channel": 0, "active": []},
        }
        self.config.register_guild(**default_guild)

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

    @raids.command()
    async def channel(self, ctx, chan: discord.TextChannel = None):
        """
        Set the channel for Raid Creation commands
        """
        if chan is None:
            chan = ctx.channel

        await self.bot.config.raids.channel.set(chan.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @set.group()
    async def ex(self, ctx):
        """
        Set settings for EXRaid creation/management
        """
        pass

    @ex.command()
    async def channel(self, ctx, chan: discord.TextChannel = None):
        """
        Set the channel for EXRaid Creation commands
        """
        if chan is None:
            chan = ctx.channel

        await self.bot.config.ex.channel.set(chan.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @ex.command()
    async def channel(self, ctx, bucket: str):
        """
        Set the channel for EXRaid Creation AWS Bucket
        """

        await self.bot.config.ex.bucket.set(bucket)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
