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
                name="__________\nHow to Vote", value="Simply React to this message to cast your vote\n 👍 for Yes   |   👎 for No"
            )
        await ctx.send(embed=embed)
