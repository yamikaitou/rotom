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
        """
        
        chan = await self.bot.config.guild(ctx.guild).raids.channel()
        timer = await self.bot.config.raids.timer()
        if ctx.channel.id == chan:
            newchan = await ctx.guild.create_text_channel(channel, category=ctx.channel.category)
            
        async with self.bot.config.raids.active() as channels:
            now = datetime.now()
            expire =now+timedelta(minutes=time)
            hatch = now+timedelta(minutes=(time-timer))
            channels[newchan.id] = [ctx.guild.id, now+timedelta(minutes=time)]
            expires = "Expires around "+expire.strftime("%m/%d/%Y %I:%M:%S %p")+" (~"+str(time)+" minutes)."
            if hatch < now:
                hatches = "- The egg already has hatched!"
            else:
                hatches = "- The egg should hatch around "+hatch.strftime("%m/%d/%Y %I:%M:%S %p")+" (~"+str(int(((hatch-now).seconds)/60))+" minutes)."

            await newchan.send(expires+"\n"+hatches)

    
    @tasks.loop(minutes=1.0)
    async def raid_channel(self):
        await self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send("task run")
        now = datetime.now()
        async with self.bot.config.raids.active() as channels:
            purge = []
            await self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send(channels)
            for channel,value in channels.items():
                await self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send(channel)
                await self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send(value)
                await self.bot.get_guild(429381405840244767).get_channel(463776844051644418).send(value[0])
                chan = await self.bot.fetch_channel(channel)
                await chan.send("still here")
                if value[1] < now:
                    await chan.send("You are now deleted")
                    purge.append(channel)
            
            for delete in purge:
                del channels[delete]

    @raid_channel.before_loop
    async def before_raidchannel(self):
        await self.bot.wait_until_ready()