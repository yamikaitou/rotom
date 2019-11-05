import discord
from redbot.core import commands, __version__, checks, Config
import sys
from typing import Union
import asyncio
import aiobotocore
import os
import aiofiles
import aiomysql
from .emoji import *


class EXRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1977316625, force_registration=True)

        default_guild = {"active": [], "channel": 0, "bucket": ""}

        self.config.register_guild(**default_guild)

    @commands.command()
    @checks.is_owner()
    async def setexchannel(self, ctx):
        """
        Set the EX Raid Submission channel to the current channel
        """
        await self.config.guild(ctx.guild).channel.set(ctx.channel.id)
        await ctx.message.delete()

    @commands.command()
    @checks.is_owner()
    async def setexbucket(self, ctx, *, bucket):
        """
        Set the EX Raid Submission AWS Bucket
        """
        await self.config.guild(ctx.guild).bucket.set(bucket)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot or not message.guild:
            return

        guild = message.guild
        chan = await self.config.guild(guild).channel()
        if message.channel.id != chan:
            return

        ctx = await self.bot.get_context(message)
        for attach in message.attachments:
            name, ext = os.path.splitext(attach.filename)
            file = "{}{}".format(attach.id, ext)
            await attach.save("/tmp/" + file)

            session = aiobotocore.get_session(loop=self.bot.loop)

            awskeys = await self.bot.db.api_tokens.get_raw(
                "aws", default={"secret_key": None, "access_key": None, "region": None}
            )
            awskeys["bucket"] = await self.config.guild(guild).bucket()

            async with session.create_client(
                "s3",
                region_name=awskeys["region"],
                aws_secret_access_key=awskeys["secret_key"],
                aws_access_key_id=awskeys["access_key"],
            ) as s3client:

                async with aiofiles.open("/tmp/" + file, mode="rb") as f:
                    content = await f.read()
                await s3client.put_object(Bucket=awskeys["bucket"], Key=file, Body=content)

                async with session.create_client(
                    "rekognition",
                    region_name=awskeys["region"],
                    aws_secret_access_key=awskeys["secret_key"],
                    aws_access_key_id=awskeys["access_key"],
                ) as client:

                    resp = await client.detect_text(
                        Image={"S3Object": {"Bucket": awskeys["bucket"], "Name": file}}
                    )
                    top, when, where = None, None, None
                    for text in resp["TextDetections"]:
                        if text["Type"] == "LINE":
                            if text["DetectedText"] == "INVITATION":
                                top = True
                                continue

                            if top is True and when is None:
                                when = text["DetectedText"]
                                continue

                            if top is True and where is None:
                                where = text["DetectedText"]
                                continue

                            if top is True and when is not None and where is not None:
                                break

                    try:
                        await self.processex(ctx, when, where)
                    except Exception as e:
                        await ctx.send(
                            "Something went wrong will processing your image. Please wait for YamiKaitou to manually create the channel"
                        )
                        await self.bot.get_guild(429381405840244767).get_channel(
                            641096527775006735
                        ).send(
                            f"EXRaid failure.\nException: {type(e).__name__}\nWhen: {when}\nWhere: {where}\n{attach.url}"
                        )

    @commands.command()
    @checks.admin_or_permissions(manage_channels=True)
    async def forceexraid(self, ctx, when, where):
        """
        Forcibly create an EX Raid channel
        """
        await self.processex(ctx, when, where)

    async def processex(self, ctx, when, where):
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
        await curs.execute("""SELECT * FROM gyms WHERE Name = "{}";""".format(where))

        r = await curs.fetchall()
        await curs.close()
        conn.close()
        gym = r[0]

        when2 = when.split()
        time = when2[2].split(":")
        if time[1] == "00":
            time2 = time[0] + when2[3].lower()
        else:
            time2 = time[0] + time[1] + when2[3].lower()

        if gym[2] == "":
            where = gym[1]
        else:
            where = gym[2]

        channel = "ex_{}-{}_{}_{}".format(
            when2[0][:3], when2[1], where.replace(" ", "-").replace("'", ""), time2
        ).lower()
        cur = await self.config.guild(ctx.guild).active()
        if channel in cur:
            await ctx.message.delete()
            return

        newchan = await ctx.guild.create_text_channel(channel, category=ctx.channel.category)

        embed = discord.Embed(
            title="EX Raid @ {}".format(gym[1]),
            colour=discord.Color(0x58BA8B),
            description="**Scheduled for {} {} @ {}**\n\n"
            "{}\n"
            "[Google Map](https://www.google.com/search/dir/?api=1&query={})\n\n".format(
                when2[0][:3], when2[1], time2, gym[3], gym[4]
            ),
        )
        embed.set_thumbnail(
            url="https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/pokemon_icons/pokemon_icon_150_00_shiny.png"
        )
        embed.add_field(
            name="#150 Mewtwo",
            value=f"Type: {PSYCHIC}\n"
            f"Weakness: {BUG} {GHOST} {DARK}\n"
            f"Resists: {FIGHTING} {PSYCHIC}\n"
            f"Perfect CP: 2387 / 2984",
            inline=False,
        )
        # embed.add_field(name="Participants",
        #                value=f"1:00 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n1:15 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n1:30 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}",
        #                inline=False)

        async with self.config.guild(ctx.guild).active() as act:
            act.append(channel)

        await ctx.message.delete()
        await ctx.send("{} - {} {} = {}".format(gym[1], when2[0][:3], when2[1], newchan.mention))
        await newchan.send(embed=embed)

    @commands.command()
    @checks.admin_or_permissions(manage_channels=True)
    async def retryex(self, ctx, msgid: int):
        """
        Reprocesses an EXRaid image
        """

        chan = await self.config.guild(ctx.guild).channel()
        if ctx.channel.id == chan:
            msg = await ctx.channel.fetch_message(msgid)
            await self.on_message(msg)
            await ctx.message.delete()
