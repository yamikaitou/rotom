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

    @checks.admin()
    @commands.command()
    async def suggest(self, ctx, num: int):
        """
        Get specific Suggestion
        """

        git = await self.bot.db.api_tokens.get_raw(
            "github", default={"token": None, "repo": None}
        )

        g = Github(git["token"])
        repo = g.get_repo(git["repo"])
        issue = repo.get_issue(num)

        embed = discord.Embed(
                title=issue.title,
                colour=discord.Colour(0xA80387),
                description=issue.body,
            )
        embed.add_field(
                name="How to Vote", value="Simply React to this message to cast your vote\n\N{THUMBS UP} for Yes\n\N{THUMBS DOWN} for No"
            )
        embed.add_field(
                name="How to Vote", value="Simply React to this message to cast your vote\n\N{CHECK MARK} for Yes\n\N{MULTIPLICATION SIGN} for No\n\N{MINUS SIGN} for Don't Care"
            )
        await ctx.send(embed=embed)
