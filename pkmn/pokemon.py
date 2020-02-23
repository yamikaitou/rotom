import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
from typing import Union
import math
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

        sqlkeys = await self.bot.get_shared_api_tokens("mysql")

        conn = await aiomysql.connect(
            host=sqlkeys.get("host"),
            port=3306,
            user=sqlkeys.get("user"),
            password=sqlkeys.get("pass"),
            db=sqlkeys.get("data"),
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
            embed = discord.Embed(
                title=f"#001 - Bulbasaur",
                colour=discord.Colour(0xA80387),
                description=f"{GRASS} {POISON} :sparkles:\n\n"
                f"Weak - {FIRE} {FLYING} {ICE} {PSYCHIC}\n"
                f"Super Weak - \n\n"
                f"Resists - {ELECTRIC} {FAIRY} {FIGHTING} {WATER}\n"
                f"Super Resists - {GRASS}\n",
            )
            embed.set_image(url="https://rotom.app/discord/pkmn/pokemon_icon_001_00.png")
            bAtk = 118
            bDef = 111
            bSta = 128
            cp15 = math.floor(
                (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.51739395, 2)) / 10
            )
            cp20 = math.floor(
                (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.5974, 2)) / 10
            )
            cp25 = math.floor(
                (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.667934, 2)) / 10
            )

            embed.add_field(
                name="Perfect CP", value=f"Lv15 - {cp15}\nLv20 - {cp20}\nLv25 - {cp25}"
            )
            embed.add_field(
                name="Evolutions", value="2nd: Ivysaur - 25 Candy\n3rd: Venasaur - 100 Candy"
            )
            await ctx.send(embed=embed)
