import discord
from discord.ext import tasks
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
from datetime import datetime


class Raids(commands.Cog):
    """
    Raid Channel
    """

    def __init__(self, bot):
        self.bot = bot
        self.slow_count.start()
    
    def cog_unload(self):
        self.slow_count.cancel()
    
    @commands.command()
    async def create(self, ctx, channel: str, time: int):
        """
        Create Raid Channels following the format of RoomBot
        """
        
        chan = await self.bot.config.guild(ctx.guild).raids.channel()
        if ctx.channel.id == chan:
            newchan = await ctx.guild.create_text_channel(channel, category=ctx.channel.category)
            async with self.bot.config.guild(ctx.guild).raids.active() as channels:
                channels[newchan.id] = [ctx.guild, datetime.now(), time]

    
    @tasks.loop(minutes=1.0)
    async def raid_channel(self):
        print("task run")
        async with self.bot.config.guild(self.bot.get_guild(429381405840244767)).raids.active() as channels:
            for channel in channels.items():
                self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send(channel)

    
    @tasks.loop(seconds=5.0, count=5)
    async def slow_count():
        print(self.slow_count.current_loop)

    @slow_count.after_loop
    async def after_slow_count():
        print('done!')
