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


class Pokemon(commands.Cog):
    """
    Rotom's Pokemon Database Access
    """

    def __init__(self, bot):
        self.bot = bot
        self.chart = json.load(open(data_manager.bundled_data_path(self).joinpath("chart.json")))

    @commands.command()
    async def pkmn(self, ctx, name: Union[str, int], *, form: str = None):
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
            await self._display(ctx, r[0])
        elif len(r) >= 1:
            if form is None:
                form = "NORMAL"
            if form.upper() == "ARMORED" or form.upper() == "ARMOR":
                form = "A"

            yes = False
            forms = ""
            for p in r:
                forms += p[3].capitalize() + ", "
                if p[3] == form.upper():
                    await self._display(ctx, p)
                    yes = True
                    break

            if not yes:
                await ctx.send(f"Form not understood, try one of these instead\n{forms}")
        else:
            await ctx.send("Unknown Pokemon")

    @commands.command()
    @checks.mod()
    async def newshiny(self, ctx, name: str):
        """
        Activate a new shiny
        """

        session = aiobotocore.get_session(loop=self.bot.loop)

        awskeys = await self.bot.db.api_tokens.get_raw(
            "aws", default={"secret_key": None, "access_key": None, "region": None}
        )

        async with session.create_client(
            "sqs",
            region_name=awskeys["region"],
            aws_secret_access_key=awskeys["secret_key"],
            aws_access_key_id=awskeys["access_key"],
        ) as client:
            response = await client.get_queue_url(QueueName="rotom")
            queue_url = response["QueueUrl"]
            resp = await client.send_message(QueueUrl=queue_url, MessageBody=name)
            await ctx.send(resp)

    async def _display(self, ctx, data, *, disp=False, ret=False):
        szTitle = "#" + str(data[2]) + " - " + data[1].capitalize()
        if data[3] is not None and data[3] != "NORMAL":
            szTitle += " (" + data[3].capitalize() + ")"
        szType = emojis[data[6]]
        if data[7] != None:
            szType += " " + emojis[data[7]]
        if data[5]:
            szType += " :sparkles:"

        t1 = self.chart[data[6]]
        t2 = {}
        if data[7] is not None:
            t2 = self.chart[data[7]]
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

        embed = discord.Embed(
            title=szTitle,
            colour=discord.Colour(0xA80387),
            description=f"{szType}\n\n" f"{vulnable}\n" f"{resist}\n",
        )
        if data[5] == 1:
            shiny = "_1"
        else:
            shiny = ""
        embed.set_image(
            url=f"https://rotom.app/discord/pkmn/pokemon_icon_{data[2]:03d}_{data[4]:02d}{shiny}.png"
        )
        bAtk = data[8] + 15
        bDef = data[9] + 15
        bSta = data[10] + 15
        cp15 = math.floor(
            (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.51739395, 2)) / 10
        )
        cp20 = math.floor(
            (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.5974, 2)) / 10
        )
        cp25 = math.floor(
            (bAtk * math.pow(bDef, 0.5) * math.pow(bSta, 0.5) * math.pow(0.667934, 2)) / 10
        )

        embed.add_field(name="Perfect CP", value=f"Lv15 - {cp15}\nLv20 - {cp20}\nLv25 - {cp25}")
        if ret:
            return {
                "name": szTitle,
                "form": data[3].capitalize(),
                "type": szType,
                "resist": resist,
                "weak": vulnable,
                "shiny": data[5],
                "cp": [cp15, cp20, cp25],
            }
        if disp:
            return embed

        await ctx.send(embed=embed)

    async def get_pkmn(self, name: str, form: str = None):
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
            return r[0]
        elif len(r) >= 1:
            if form is None:
                form = "NORMAL"
            if form.upper() == "ARMORED" or form.upper() == "ARMOR":
                form = "A"

            yes = False
            forms = ""
            for p in r:
                forms += p[3].capitalize() + ", "
                if p[3] == form.upper():
                    return p

            if not yes:
                return False
        else:
            return False
