import discord
import random
from redbot.core import commands, Config, checks
from redbot.core.utils.predicates import MessagePredicate
import asyncio


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
            existing = len(chans)
            for k in range(existing, existing + number + 1):
                newchan = await ctx.guild.create_text_channel(
                    f"raid-day_group{k}",
                    category=ctx.guild.get_channel(cat),
                    overwrites=ctx.guild.get_channel(copy).overwrites,
                )
                embed = discord.Embed(
                    title="Global Challenge Raid Day",
                    colour=discord.Colour(0xA14F2E),
                    description=f"June 29 @ 4pm - 7pm\n\n**Boss: Raikou**\nPerfect CP: 1972 / 2466\n\n\nThis is Group {k}, please coordinate your group and route here\n",
                )
                embed.set_image(
                    url="https://github.com/ZeChrales/PogoAssets/raw/master/pokemon_icons/pokemon_icon_243_00_shiny.png"
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
                channels.remove(channel)
                await ctx.get_channel(channel).delete()

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
