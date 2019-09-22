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
from datetime import datetime, timedelta


class Raids(commands.Cog):
    """
    Raid Channel
    """

    def __init__(self, bot):
        self.bot = bot
        self.raid_channel.start()

    def cog_unload(self):
        self.raid_channel.cancel()

    @commands.command()
    async def create(self, ctx, channel: str, time: int):
        """
        Create Raid Channels following the format of RoomBot

        channel = The name of the channel to create
        time = Time remaining in the Raid (this is the Egg time + Raid time)

        Examples:
        >create lv5-starbucks 20
           This will create a room named `lv5-starbucks` and will expire in 20 minutes (the Raid should already have hatched)
        
        >create lv3-sprint 67
           This will create a room named `lv3-sprint` and will expire in 67 minutes (22 minutes left until hatch and a 45 minute Raid timer)
        """

        chan = await self.bot.config.guild(ctx.guild).raids.channel()
        timer = await self.bot.config.raids.timer()
        if ctx.channel.id == chan:
            newchan = await ctx.guild.create_text_channel(channel, category=ctx.channel.category)

        async with self.bot.config.raids.active() as channels:
            now = datetime.now()
            expire = now + timedelta(minutes=time)
            hatch = now + timedelta(minutes=(time - timer))
            channels[newchan.id] = [ctx.guild.id, now + timedelta(minutes=time)]
            expires = (
                "Expires around "
                + expire.strftime("%m/%d/%Y %I:%M:%S %p")
                + " (~"
                + str(time)
                + " minutes)."
            )
            if hatch < now:
                hatches = "- The egg already has hatched!"
            else:
                hatches = (
                    "- The egg should hatch around "
                    + hatch.strftime("%m/%d/%Y %I:%M:%S %p")
                    + " (~"
                    + str(int(((hatch - now).seconds) / 60))
                    + " minutes)."
                )

            await newchan.send(expires + "\n" + hatches)

    @commands.command()
    async def rename(self, ctx, name: str):
        """
        Renames Raid Channels following the format of RoomBot

        name = The new name of the channel or raid boss
        
        Examples:
        >rename rotom
           If the room name is like `lv3-starbucks`, then this will rename it to `rotom-starbucks`. If the room didn't have a dash in it, then it will behave the same as the below example
        
        >rename rotom-sprint
           This will rename the room to `rotom-sprint` regardless what the previous name was
        """
        await ctx.send("Sorry, but I don't actually do anything yet")

    @tasks.loop(minutes=1.0)
    async def raid_channel(self):
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
