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
        self.config = Config.get_conf(self, identifier=1705281793, force_registration=True)
        self.config.register_global(**{"token": 0, "repo": "git/hub"})

    @commands.command()
    @commands.check(lambda ctx: ctx.guild is None)
    @checks.is_owner()
    async def setsug(self, ctx, key, value):
        """
        Set settings for Suggestions
        
        key = token or repo
        value = value for the key
        """

        if key == "token":
            await self.config.token.set(value)
            await ctx.send("GitHub Token Set")
        if key == "repo":
            await self.config.repo.set(value)
            await ctx.send("GitHub Repo Set")

    @commands.command()
    @commands.check(lambda ctx: ctx.guild is None)
    async def suggest(self, ctx):
        """
        Log a suggestion for features to add to Rotom
        """

        await ctx.send(
            "Bzzt! Greetings. I am ready to hear your suggestion. Please type it all in 1 message and within the next 5 minutes"
        )
        try:

            msg = await self.bot.wait_for(
                "message",
                check=MessagePredicate.same_context(ctx, ctx.channel, ctx.author),
                timeout=300,
            )

            token = await self.config.token()
            repos = await self.config.repo()

            g = Github(token)

            repo = g.get_repo(repos)
            label = repo.get_label("enhancement")
            issue = repo.create_issue(
                title="Feature Request from {}".format(
                    self.bot.get_guild(331635573271822338).get_member(ctx.author.id).display_name
                ),
                labels=[label],
                body=msg.content,
            )
            await ctx.send(
                "Your suggestion has been logged.\n"
                "You can view the status of it at <https://github.com/{repo}/issues/{id}>\n"
                "You can view other suggestions at <https://github.com/{repo}/issues?q=is%3Aissue+label%3Aenhancement>".format(
                    repo=repos, id=issue.number
                )
            )
        except asyncio.TimeoutError:
            await ctx.send(
                "Sorry, you took too long. If you would like to try again, just say `>suggest` to get started again"
            )
