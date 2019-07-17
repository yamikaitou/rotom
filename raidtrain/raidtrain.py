import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio
from .emoji import *


class RaidTrain(commands.Cog):
    """
    Rotom Raid Train
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)

        default_guild = {"category": 0, "copy": 0, "channels": []}
        self.config.register_guild(**default_guild)

    @checks.mod()
    @commands.command()
    async def raidday(self, ctx, number: int):
        """
            Creates Raid Train rooms
        """

        if isinstance(number, int) and number > 0:
            cat = await self.config.guild(ctx.guild).category()
            copy = await self.config.guild(ctx.guild).copy()
            chans = await self.config.guild(ctx.guild).channels()
            existing = len(chans) + 1
            for k in range(existing, existing + number):
                newchan = await ctx.guild.create_text_channel(
                    f"mewtwo-hour_group{k}",
                    category=ctx.guild.get_channel(cat),
                    overwrites=ctx.guild.get_channel(copy).overwrites,
                )
                
                embed = discord.Embed(
                    title="Legendary Hour - Mewtwo (Armored)",
                    colour=discord.Colour(0xB1D053),
                    description="July 17 @ 6pm",
                )
                embed.set_image(
                    url="https://db.pokemongohub.net/images/ingame/normal/pokemon_icon_150_01.png"
                )
                embed.add_field(
                    name="#150 - Mewtwo (Armored)",
                    value=f"Type: {PSYCHIC}\n"
                    f"Weakness: {BUG} {DARK} {GHOST}\n"
                    f"Resists: {FIGHTING} {PSYCHIC}\n"
                    f"Perfect CP: 1821 / 2276",
                    inline=False,
                )
                await newchan.send(embed=embed)

                async with self.config.guild(ctx.guild).channels() as channels:
                    channels.append(newchan.id)

            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        else:
            await ctx.send("You must specify a number greater than 0")

    @checks.mod()
    @commands.command()
    async def rtdel(self, ctx):
        async with self.config.guild(ctx.guild).channels() as channels:
            for channel in channels:
                await ctx.guild.get_channel(channel).delete()
        await self.config.guild(ctx.guild).channels.clear()

    @checks.admin()
    @commands.group()
    async def rtset(self, ctx):
        """
            Various settings for RaidTrain
        """
        pass

    @rtset.command()
    async def category(self, ctx, category_id: discord.CategoryChannel):
        """
            Set the Category the RaidTrain channels are created in
        """
        await self.config.guild(ctx.guild).category.set(category_id.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @rtset.command()
    async def permission(self, ctx, channel_id: discord.TextChannel):
        """
            Set the channel to copy permissions from
        """
        await self.config.guild(ctx.guild).copy.set(channel_id.id)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

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

    @test.command()
    async def route(self, ctx, which: str):
        if which == "free":
            await ctx.send(
                "__All Gyms are within LL Woods Park__\n"
                "East Lenard L Woods Park\n"
                "17th Tee LLWFGC\n"
                "12the Tee Par\n"
                "Disc Gold #11\n"
                "Lenard L. Woods Park"
            )
        elif which == "lew":
            await ctx.send("Placeholder")
        elif which == "fm" or which == "hv":
            await ctx.send("Placeholder")

    @test.command()
    async def meetup(self, ctx, which: str):
        if which == "free":
            await ctx.send(
                "LL Woods Park Pavilion\n"
                "1000 Arbour Way, Lewisville, TX\n"
                "[Google Map](https://www.google.com/search/dir/?api=1&query=33.055065,-97.038674)"
            )
        elif which == "lew":
            await ctx.send("Placeholder")
        elif which == "fm" or which == "hv":
            await ctx.send("Placeholder")
