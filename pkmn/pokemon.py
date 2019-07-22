import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
from .emoji import *


class Pokemon(commands.Cog):
    """
    Rotom's Pokemon Database Access
    """

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pkmn(self, ctx, name: [str, int], form: str = None)
        """
        Pull Pokemon details from the database
        """

        conn = await aiomysql.connect(
            host=sqlkeys["host"],
            port=3306,
            user=sqlkeys["user"],
            password=sqlkeys["pass"],
            db=sqlkeys["data"],
            loop=self.bot.loop,
        )
        curs = await conn.cursor()
        await curs.execute("SELECT * FROM gyms WHERE Name LIKE %(name)s OR Dex = %(name)s", {'name': name})
        r = await curs.fetchall()
        await curs.close()
        conn.close()

        await ctx.send(r)