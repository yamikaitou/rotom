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
