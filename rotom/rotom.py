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
        self.bot.config = Config.get_conf(self, identifier=1977316625, force_registration=True)
        default_guild = {
            "ex": {"active": [], "channel": 0, "bucket": ""},
            "raids": {"channel": 0, active: []},
        }
        self.config.register_guild(**default_guild)

    @checks.admin()
    @commands.group()
    async def rotom(self, ctx):
        pass
