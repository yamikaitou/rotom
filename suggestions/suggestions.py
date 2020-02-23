import discord
from discord.ext import tasks
import random
from redbot.core import commands, Config, checks
from github import Github, GithubException
from redbot.core.utils.predicates import MessagePredicate
import asyncio
from datetime import datetime, timedelta


class Suggestions(commands.Cog):
    """
    Rotom Suggestion Bot
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=192153481165930496, force_registration=True)
        default_guild = {"tag": "", "channel": 0, "posts": []}
        default_global = {"repo": "", "issue": 0}
        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

        self.labels = {
            "lab": 429381405840244767,
            "lew/fm/hv": 331635573271822338,
            "harvest": 535612750924218368,
        }

        self.post_suggest.start()

    def cog_unload(self):
        self.post_suggest.cancel()

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

    @suggestset.command()
    async def channel(self, ctx, value: str = None):
        """Set/Show the channel for this guild"""

        if value is None:
            chan = await self.config.guild(ctx.guild).channel()
            chans = ctx.guild.get_channel(chan)
            await ctx.send(f"Current channel: {chans.name} ({chan})")
        else:
            await self.config.guild(ctx.guild).channel.set(value)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @checks.admin()
    @commands.command()
    async def suggest(self, ctx, num: int):
        """
        Get specific Suggestion
        """

        git = await self.bot.get_shared_api_tokens("github")
        gitrepo = await self.config.repo()

        g = Github(git.get("token"))
        repo = g.get_repo(gitrepo)
        issue = repo.get_issue(num)

        guilds = await self.config.all_guilds()

        for label in issue.labels:
            for id, data in guilds.items():
                if id == ctx.guild.id and label.name == data["tag"] and data["channel"] != 0:
                    embed = discord.Embed(
                        title=issue.title, colour=discord.Colour(0xA80387), description=issue.body
                    )
                    embed.add_field(
                        name="__________\nHow to Vote",
                        value="Simply React to this message to cast your vote\n 👍 for Yes   |   👎 for No",
                    )
                    chan = self.bot.get_guild(id).get_channel(data["channel"])
                    msg = await chan.send(embed=embed)
                    await msg.add_reaction("👍")
                    await msg.add_reaction("👎")
                else:
                    await ctx.send(
                        f"That suggestion is not for this guild | {label} | {id} | {data}"
                    )

    @tasks.loop(hours=48.0)
    async def post_suggest(self):
        num = await self.config.issue()

        git = await self.bot.get_shared_api_tokens("github")
        gitrepo = await self.config.repo()

        g = Github(git.get("token"))
        repo = g.get_repo(gitrepo)
        try:
            issue = repo.get_issue(num + 1)
        except GithubException:
            pass
        else:
            guilds = await self.config.all_guilds()

            for label in issue.labels:
                for id, data in guilds.items():
                    if label.name == data["tag"] and data["channel"] != 0:
                        embed = discord.Embed(
                            title=issue.title,
                            colour=discord.Colour(0xA80387),
                            description=issue.body,
                        )
                        embed.add_field(
                            name="__________\nHow to Vote",
                            value="Simply React to this message to cast your vote\n 👍 for Yes   |   👎 for No",
                        )

                        chan = self.bot.get_guild(int(id)).get_channel(int(data["channel"]))
                        msg = await chan.send(embed=embed)
                        await msg.add_reaction("👍")
                        await msg.add_reaction("👎")
                        async with self.config.guild(id).posts() as posts:
                            posts.append([issue.number, msg.id, datetime.utcnow()])

            await self.config.issue.set(num + 1)

    @post_suggest.before_loop
    async def before_post_suggest(self):
        await self.bot.wait_until_ready()

    @tasks.loop(hours=24.0)
    async def end_suggest(self):

        git = await self.bot.get_shared_api_tokens("github")
        gitrepo = await self.config.repo()

        g = Github(git.get("token"))
        repo = g.get_repo(gitrepo)

        guilds = await self.config.all_guilds()
        for id, data in guilds.items():
            for msg, post in data["posts"]:
                pass

    @end_suggest.before_loop
    async def before_end_suggest(self):
        await self.bot.wait_until_ready()
