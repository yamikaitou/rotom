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

        default_guild = {"category": 0, "copy": 0}
        self.config.register_guild(**default_guild)

    @checks.mod()
    @commands.command()
    async def raidtrain(self, ctx, number: int):
        """
            Creates Raid Train rooms
        """

        if isinstance(number, int) and number > 0:
            cat = await self.config.guild(ctx.guild).category()
            copy = await self.config.guild(ctx.guild).copy()
            for k in range(1, number + 1):
                newchan = await ctx.guild.create_text_channel(
                    f"legendary-hour_group{k}",
                    category=cat,
                    overwrites=ctx.guild.get_channel(copy).overwrites,
                )
                embed = discord.Embed(
                    title="Legendary Raid Hour",
                    colour=discord.Colour(0xA14F2E),
                    description=f"June 19 @ 6pm\n\n**Boss: Kyogre**\nPerfect CP: 2351 / 2939\n\n\nThis is Group {k}, please coordinate your group and route here\n",
                )
                embed.set_image(
                    url="https://github.com/ZeChrales/PogoAssets/raw/master/pokemon_icons/pokemon_icon_382_00_shiny.png"
                )
                await newchan.send(embed=embed)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        else:
            await ctx.send("You must specify a number greater than 0")

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
