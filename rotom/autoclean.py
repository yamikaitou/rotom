import discord
import random
from redbot.core import commands, Config, checks, data_manager
from redbot.core.utils.predicates import MessagePredicate
import asyncio
from typing import Union
import math
import json
from .emoji import *


class AutoClean(commands.Cog):
    """
    Rotom's auto cleaning channels cog
    """

    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=1.0)
    async def clean_msg(self):
        now = datetime.now()
        async with self.bot.config.raids.active() as channels:
            purge = []
            for channel, value in channels.items():
                chan = await self.bot.fetch_channel(channel)
                if value[1] < now:
                    await chan.delete()
                    purge.append(channel)

            for delete in purge:
                del channels[delete]

    @raid_channel.before_loop
    async def before_raidchannel(self):
        await self.bot.wait_until_ready()