import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio
from .emoji import *
from datetime import datetime, timedelta


class RaidTrain(commands.Cog):
    """
    Rotom Raid Train
    """

    rdclist = {
        "331635573271822338": {
            "fm": ["Flower Mound & Highland Village", "fm-hv"],
            "lew": ["Lewisville Vista Ridge", "vista-ridge"],
            "free": ["LL Woods - Free Passes", "llwoods-free"],
            "group4": ["Group 4", "group4"],
            "group5": ["Group 5", "group5"],
        },
        "429381405840244767": {"group1": ["Testing", "test"]},
    }

    rhclist = {
        "331635573271822338": {
            "group1": ["LL Woods", "llwoods"],
            "group2": ["Lewisville Vista Ridge", "vistaridge"],
            "group3": ["Old Town Lewisville", "oldtown"],
            "group4": ["Highland Village Shops", "hvshops"],
            "group5": ["Heritage Park", "heritage"],
            "group6": ["Old Orchard", "oldorchard"],
        },
        "429381405840244767": {"group1": ["Testing", "test"]},
    }

    def __init__(self, bot):
        self.bot = bot

    @checks.mod()
    @commands.command()
    async def raidday(self, ctx, name: str, month: int, day: int, time: int):
        """
            Creates Raid Train rooms for a Raid Day
        """
        if name != "event":
            pkmn = await self.bot.get_cog("Pokemon").get_pkmn(name)
            embed_pkmn = await self.bot.get_cog("Pokemon")._display(ctx, pkmn, ret=True)
        else:
            pkmn = ["", "Event"]

        dt = datetime.strptime(f"{month} {day} {time}", "%m %d %H")
        dt2 = dt + timedelta(hours=3)
        desc = dt.strftime("%b %-d @ %-I%p - ") + dt2.strftime("%-I%p")
        cat = await self.bot.config.guild(ctx.guild).train.category()
        copy = await self.bot.config.guild(ctx.guild).train.mimic()
        chans = await self.bot.config.guild(ctx.guild).train.day()

        for key, value in self.rdclist.items():
            newchan = await ctx.guild.create_text_channel(
                f"{pkmn[1]}-day_{value[1]}",
                category=ctx.guild.get_channel(cat),
                overwrites=ctx.guild.get_channel(copy).overwrites,
            )
            embed_start = discord.Embed(
                title=dt.strftime("%b %-d") + " Raid Day - " + value[0],
                colour=discord.Colour(0xB1D053),
                description=desc + "\n\n" + self._rhroute(ctx.guild.id, key),
            )

            if name != "event":
                embed_start.add_field(
                    name="Info",
                    value=f"{embed_pkmn['name']}\n{embed_pkmn['type']}\n\n{embed_pkmn['weak']}\n{embed_pkmn['resist']}\n",
                    inline=False,
                )
                embed_start.add_field(
                    name="Perfect CP",
                    value=f"Lv20 - {embed_pkmn['cp'][1]}\nLv25 - {embed_pkmn['cp'][2]}",
                    inline=False,
                )
            else:
                embed_start.add_field(
                    name="Info",
                    value=f"Special Event spawns, see in-game news for full list of spawns",
                    inline=False,
                )

            await newchan.send(embed=embed_start)

            async with self.bot.config.guild(ctx.guild).train.day() as days:
                days.append(newchan.id)

        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @checks.mod()
    @commands.command()
    async def raidhour(self, ctx, name: str, month: int, day: int, time: int, form: str = None):
        """
            Creates Raid Hour rooms
        """
        if name != "event":
            pkmn = await self.bot.get_cog("Pokemon").get_pkmn(name)
            embed_pkmn = await self.bot.get_cog("Pokemon")._display(ctx, pkmn, ret=True)
        else:
            pkmn = ["", "Event"]

        dt = datetime.strptime(f"{month} {day} {time}", "%m %d %H")
        dt2 = dt + timedelta(hours=1)
        desc = dt.strftime("%b %-d @ %-I%p - ") + dt2.strftime("%-I%p")
        cat = await self.bot.config.guild(ctx.guild).train.category()
        copy = await self.bot.config.guild(ctx.guild).train.mimic()
        chans = await self.bot.config.guild(ctx.guild).train.hour()

        for key, value in self.rhclist[str(ctx.guild.id)].items():
            newchan = await ctx.guild.create_text_channel(
                f"{pkmn[1]}-hour_{value[1]}",
                category=ctx.guild.get_channel(cat),
                overwrites=ctx.guild.get_channel(copy).overwrites,
            )
            embed_start = discord.Embed(
                title=dt.strftime("%b %-d") + " Raid Hour - " + value[0],
                colour=discord.Colour(0xB1D053),
                description=desc + "\n\n" + self._rhroute(ctx.guild.id, key),
            )

            if name != "event":
                embed_start.add_field(
                    name="Info",
                    value=f"{embed_pkmn['name']}\n{embed_pkmn['type']}\n\n{embed_pkmn['weak']}\n{embed_pkmn['resist']}\n",
                    inline=False,
                )
                embed_start.add_field(
                    name="Perfect CP",
                    value=f"Lv20 - {embed_pkmn['cp'][1]}\nLv25 - {embed_pkmn['cp'][2]}",
                    inline=False,
                )
            else:
                embed_start.add_field(
                    name="Info",
                    value=f"Special Event spawns, see in-game news for full list of spawns",
                    inline=False,
                )

            await newchan.send(embed=embed_start)

            async with self.bot.config.guild(ctx.guild).train.hour() as days:
                days.append(newchan.id)

        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @checks.mod()
    @commands.command()
    async def rhdel(self, ctx):
        async with self.bot.config.guild(ctx.guild).train.hour() as channels:
            for channel in channels:
                try:
                    await ctx.guild.get_channel(channel).delete()
                except:
                    pass
        await self.bot.config.guild(ctx.guild).train.hour.clear()

    @checks.mod()
    @commands.command()
    async def rddel(self, ctx):
        async with self.bot.config.guild(ctx.guild).train.day() as channels:
            for channel in channels:
                try:
                    await ctx.guild.get_channel(channel).delete()
                except:
                    pass
        await self.bot.config.guild(ctx.guild).train.day.clear()

    @checks.mod()
    @commands.group()
    async def test(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="Raid Day - Entei - LL Woods Park Free Passes",
                colour=discord.Colour(0xB1D053),
                description="July 14 @ 4pm - 7pm",
            )
            embed.set_image(
                url="https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/pokemon_icons/pokemon_icon_244_00_shiny.png"
            )
            embed.add_field(
                name="#244 - Entei",
                value=f"Type: {FIRE}\n"
                f"Weakness: {GROUND} {ROCK} {WATER}\n"
                f"Resists: {BUG} {FAIRY} {FIRE} {GRASS} {ICE} {STEEL}\n"
                f"Perfect CP: 1984 / 2480",
                inline=False,
            )
            embed.add_field(
                name="Meetup Location",
                value="LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)",
            )
            embed.add_field(
                name="Route",
                value="__All Gyms are within LL Woods Park__\n"
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12the Tee Par\n"
                "Disc Gold #11\n"
                "Lenard L. Woods Park",
            )
            await ctx.send(embed=embed)

        pass

    def route(self, which: str):
        if which == "free":
            return str(
                "__All Gyms are within LL Woods Park__\n"
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12the Tee Par\n"
                "Disc Gold #11\n"
                "Lenard L. Woods Park\n"
            )
        elif which == "lew":
            return str(
                "Railroad Park Football Fields\n"
                "Railroad Park Soccer Fields\n"
                "Skate Park\n"
                "Railroad Park Box Car\n"
                "Lakeport Gazebo\n"
                "Hebron Station 121 Sign\n"
                "Edgewater Fountain\n"
                "Hilton Fountain\n"
                "Cleaner Fountain and Reflecting Pool\n"
                "Vista Ridge Lone Star\n"
                "Vista Ridge V Obelisk\n"
                "Sprint Store\n"
                "Boomerang Comics\n"
                "Going Bonkers Big Eyes\n"
                "Sequoia Bluff Fountain\n"
                "Redneck Heaven\n"
                "Twin Peaks Lewisville\n"
            )
        elif which == "fm" or which == "hv":
            return str(
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12th Tee Par\n"
                "Disc Golf #11\n"
                "Lenard L. Woods Park\n"
                "Parkers Square Park Fountain\n"
                "NCTC\n"
                "Spring Meadow Park\n"
                "First Baptist Church of Flower Mound\n"
                "Tiger Field\n"
                "Jakes Hilltop Park\n"
                "Grand Park\n"
                "The Village Church - Flower Mound\n"
                "Trietsch Memorial United Methodist Church\n"
                "Dixon Park\n"
                "Valley Creek Church\n"
                "Windmill of Highland Ranch\n"
                "Tower of Highlands Ranch\n"
                "Let's Swing at Shops at Highland Village\n"
                "Highland Village Teeter-Totter\n"
                "Dental Depot Clock Tower\n"
                "Kids' Kastle\n"
                "Fishing Pier\n"
            )

    def meetup(self, which: str):
        if which == "free":
            return str(
                "LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)"
            )
        elif which == "lew":
            return str(
                "Railroad Park - Football Fields Gym\n"
                "1301 S Railroad St, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.035462,-96.9708680)"
            )
        elif which == "fm" or which == "hv":
            return str(
                "LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)"
            )

    def _rhroute(self, guild, which: str):
        if guild == 331635573271822338:
            if which == "group1":
                return str("Group for raiding LL Woods Park and nearby Gyms")
            elif which == "group2":
                return str("Group for raiding Vista Ridge (Music City Mall) area Gyms")
            elif which == "group3":
                return str("Group for raiding Old Town Lewisville area Gyms")
            elif which == "group4":
                return str("Group for raiding Highland Village Shops area Gyms")
            elif which == "group5":
                return str("Group for raiding Heritage Park and nearby Gyms")
            elif which == "group6":
                return str("Group for raiding Old Orchard Church and nearby Gyms")
        elif guild == 429381405840244767:
            if which == "group1":
                return str("Testing Group")

    @test.command(name="route")
    async def route2(self, ctx, which: str):
        if which == "free":
            await ctx.send(
                "__All Gyms are within LL Woods Park__\n"
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12the Tee Par\n"
                "Disc Gold #11\n"
                "Lenard L. Woods Park\n"
            )
        elif which == "lew":
            await ctx.send(
                "Railroad Park Football Fields\n"
                "Railroad Park Soccer Fields\n"
                "Skate Park\n"
                "Railroad Park Box Car\n"
                "Lakeport Gazebo\n"
                "Hebron Station 121 Sign\n"
                "Edgewater Fountain\n"
                "Hilton Fountain\n"
                "Cleaner Fountain and Reflecting Pool\n"
                "Vista Ridge Lone Star\n"
                "Vista Ridge V Obelisk\n"
                "Sprint Store\n"
                "Boomerang Comics\n"
                "Going Bonkers Big Eyes\n"
                "Sequoia Bluff Fountain\n"
                "Redneck Heaven\n"
                "Twin Peaks Lewisville\n"
            )
        elif which == "fm" or which == "hv":
            await ctx.send(
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12th Tee Par\n"
                "Disc Golf #11\n"
                "Lenard L. Woods Park\n"
                "Parkers Square Park Fountain\n"
                "NCTC\n"
                "Spring Meadow Park\n"
                "First Baptist Church of Flower Mound\n"
                "Tiger Field\n"
                "Jakes Hilltop Park\n"
                "Grand Park\n"
                "The Village Church - Flower Mound\n"
                "Trietsch Memorial United Methodist Church\n"
                "Dixon Park\n"
                "Valley Creek Church\n"
                "Windmill of Highland Ranch\n"
                "Tower of Highlands Ranch\n"
                "Let's Swing at Shops at Highland Village\n"
                "Highland Village Teeter-Totter\n"
                "Dental Depot Clock Tower\n"
                "Kids' Kastle\n"
                "Fishing Pier\n"
            )

    @test.command(name="meetup")
    async def meetup2(self, ctx, which: str):
        if which == "free":
            await ctx.send(
                "LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)"
            )
        elif which == "lew":
            await ctx.send(
                "Railroad Park - Football Fields Gym\n"
                "1301 S Railroad St, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.035462,-96.9708680)"
            )
        elif which == "fm" or which == "hv":
            await ctx.send(
                "LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)"
            )
