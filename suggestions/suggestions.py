import discord
import random
from redbot.core import commands, Config, checks
from github import Github
from redbot.core.utils.predicates import MessagePredicate
import asyncio


class Suggestions(commands.Cog):
    """
    Rotom Suggestion Bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)
        default_guild = {"tag": ""}
        default_global = {"repo": "", "issue": 0}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

        self.labels = {
            "lab": 429381405840244767,
            "lew/fm/hv": 331635573271822338,
            "harvest": 535612750924218368,
        }

    @checks.is_owner()
    @commands.group()
    async def suggestset(self, ctx):
        """Configure Suggestion settings"""
        pass

    @suggestset.command()
    async def repo(self, ctx, value: str = None):
        """Set/Show the repo to fetch the suggestions from (global setting)"""

        if value is None:
            rep = await self.config.repo()
            await ctx.send(f"Current repo: {rep}")
        else:
            await self.config.repo.set(value)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @suggestset.command()
    async def label(self, ctx, value: str = None):
        """Set/Show the issue label for this guild"""

        if value is None:
            tag = await self.config.guild(ctx.guild).tag()
            await ctx.send(f"Current repo: {tag}")
        else:
            await self.config.guild(ctx.guild).tag.set(value)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @checks.admin()
    @commands.command()
    async def suggest(self, ctx, num: int):
        """
        Get specific Suggestion
        """

        git = await self.bot.db.api_tokens.get_raw("github", default={"token": None})
        git["repo"] = await self.config.repo()

        g = Github(git["token"])
        repo = g.get_repo(git["repo"])
        issue = repo.get_issue(num)

        guilds = await self.config.all_guilds()

        for label in issue.labels:
            if guilds[self.labels[label.name]] == ctx.guild.id:

                embed = discord.Embed(
                    title=issue.title, colour=discord.Colour(0xA80387), description=issue.body
                )
                embed.add_field(
                    name="__________\nHow to Vote",
                    value="Simply React to this message to cast your vote\n 👍 for Yes   |   👎 for No",
                )
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
            else:
                await ctx.send("That suggestion is not for this guild")
