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


class Raids(commands.Cog):
    """
    Raid Channel
    """

    def __init__(self, bot):
        self.bot = bot
