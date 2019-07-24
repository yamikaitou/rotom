import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
from typing import Union
from .emoji import *


class Pokemon(commands.Cog):
    """
    Rotom's Pokemon Database Access
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pkmn(self, ctx, name: Union[str, int], form: str = None):
        """
        Pull Pokemon details from the database
        """

        sqlkeys = await self.bot.db.api_tokens.get_raw(
            "mysql", default={"host": None, "user": None, "pass": None, "data": None}
        )
        conn = await aiomysql.connect(
            host=sqlkeys["host"],
            port=3306,
            user=sqlkeys["user"],
            password=sqlkeys["pass"],
            db=sqlkeys["data"],
            loop=self.bot.loop,
        )
        curs = await conn.cursor()
        await curs.execute(
            "SELECT * FROM pokemon WHERE Name LIKE %(name)s OR Dex = %(name)s", {"name": name}
        )
        r = await curs.fetchall()
        await curs.close()
        conn.close()

        if len(r) == 1:
            embed = discord.Embed(title="#001 - Bulbasaur", colour=discord.Colour(0xa80387), description=f"{GRASS} {POISON}\n:sparkles:")
            embed.set_image(url="https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/pokemon_icons/pokemon_icon_001_00.png")
            embed.add_field(name="Perfect CP", value="Lv15: 100\nLv20: 200\nLv25: 300")
            embed.add_field(name="Evolutions", value="2nd: Ivysaur - 25 Candy\n3rd: Venasaur - 100 Candy")
            embed.add_field(name="Weakness", value=f"160% - {FIRE} {FLYING} {ICE} {PSYCHIC}")
            embed.add_field(name="Resistance", value=f"62.5% - {ELECTRIC} {FAIRY} {FIGHTING} {WATER}\n39.1% - {GRASS}")
            await ctx.send(embed=embed)
