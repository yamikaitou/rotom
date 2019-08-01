import discord
import random
from redbot.core import commands, Config, checks, data_manager
from redbot.core.utils.predicates import MessagePredicate
import asyncio
import aiomysql
from typing import Union
import math
import json
from .emoji import *


class Pokemon(commands.Cog):
    """
    Rotom's Pokemon Database Access
    """

    def __init__(self, bot):
        self.bot = bot
        self.chart = json.load(open(data_manager.bundled_data_path(self).joinpath("chart.json")))

    @commands.command()
    async def pkmn(self, ctx, name: Union[str, int], form: str = None):
        """
        Pull Pokemon details from the database
        """

        sqlkeys = await self.bot.db.api_tokens.get_raw(
            "mysql", default={"host": None, "user": None, "pass": None, "data": None}
        )
        await ctx.send("Searching")
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
            await ctx.send("1 form found")
            szTitle = "#" + str(r[0][2]) + " - " + r[0][1].capitalize()
            szType = emojis[r[0][6]]
            if r[0][7] != None:
                szType += " " + emojis[r[0][7]]
            if r[0][5]:
                szType += " :sparkles:"

            t1 = self.chart[r[0][6]]
            t2 = {}
            if r[0][7] is not None:
                t2 = self.chart[r[0][7]]
            ts = {key: t1.get(key, 0) + t2.get(key, 0) for key in set(t1) | set(t2)}
            t = {"r": [], "dr": [], "tr": [], "v": [], "dv": []}
            for k, v in ts.items():
                if v <= -3:
                    t["tr"].append(k)
                elif v == -2:
                    t["dr"].append(k)
                elif v == -1:
                    t["r"].append(k)
                elif v == 1:
                    t["v"].append(k)
                elif v >= 2:
                    t["dv"].append(k)

            resist = ""
            if t["r"] != []:
                resist += "Resists: "
                for k in t["r"]:
                    resist += emojis[k] + " "
                resist += "\n"
            if t["dr"] != []:
                resist += "Double Resists: "
                for k in t["dr"]:
                    resist += emojis[k] + " "
                resist += "\n"
            if t["tr"] != []:
                resist += "Triple Resists: "
                for k in t["tr"]:
                    resist += emojis[k] + " "
                resist += "\n"

            vulnable = ""
            if t["v"] != []:
                vulnable += "Weak: "
                for k in t["v"]:
                    vulnable += emojis[k] + " "
                vulnable += "\n"
            if t["dv"] != []:
                vulnable += "Super Weak: "
                for k in t["dv"]:
                    vulnable += emojis[k] + " "
                vulnable += "\n"
            await ctx.send(t)
            embed = discord.Embed(
                title=szTitle,
                colour=discord.Colour(0xA80387),
                description=f"{szType}\n\n" f"{vulnable}\n" f"{resist}\n",
            )
            embed.set_image(
                url=f"https://rotom.app/discord/pkmn/pokemon_icon_{r[0][2]}_{r[0][4]}.png"
            )
            bAtk = r[0][8]
            bDef = r[0][9]
            bSta = r[0][10]
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
            await ctx.send(embed=embed)
        else:
            await ctx.send(r)
