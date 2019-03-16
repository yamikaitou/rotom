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


class EXRaid(getattr(commands, "Cog", object)):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1977316625, force_registration=True)

        default_guild = {"active": [], "channel": 0}
        default_global = {
            "keys": {
                "aws": {"region": "", "secret_key": "", "access_key": "", "bucket": ""},
                "sql": {"host": "", "user": "", "pass": "", "data": ""},
            }
        }

        self.config.register_guild(**default_guild)
        self.config.register_global(**default_global)

    @commands.command()
    @commands.check(lambda ctx: ctx.guild is None)
    @checks.is_owner()
    async def setexkeys(self, ctx, key, value1, value2, value3, value4):
        """
        Set settings for Suggestions
        
        key = aws or sql
        value1 = aws_region, sql_host
        value2 = aws_secret_key, sql_user
        value3 = aws_access_key, sql_pass
        value4 = aws_bucket, sql_data
        """

        if key == "aws":
            await self.config.keys.aws.set(
                {"region": value1, "secret_key": value2, "access_key": value3, "bucket": value4}
            )
            await ctx.send("AWS Keys set")
        if key == "sql":
            await self.config.keys.sql.set(
                {"host": value1, "user": value2, "pass": value3, "data": value4}
            )
            await ctx.send("MySQL Keys set")

    @commands.command()
    @checks.is_owner()
    async def setexchannel(self, ctx):
        """
        Set the EX Raid Submission channel to the current channel
        """
        await self.config.guild(ctx.guild).channel.set(ctx.channel.id)
        await ctx.message.delete()

    async def on_message(self, message):

        if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
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

            awskeys = await self.config.keys.aws()

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
                                print(when)
                                continue

                            if top is True and where is None:
                                where = text["DetectedText"]
                                print(where)
                                continue

                            if top is True and when is not None and where is not None:
                                break

                    sqlkeys = await self.config.keys.sql()
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
                    cur = await self.config.guild(guild).active()
                    if channel in cur:
                        await ctx.message.delete()
                        return

                    newchan = await ctx.guild.create_text_channel(
                        channel, category=ctx.channel.category
                    )

                    embed = discord.Embed(
                        title="EX Raid @ {}".format(gym[1]),
                        colour=discord.Colour(0x58BA8B),
                        description="**Scheduled for {} {} @ {}**\n\n"
                        "{}\n"
                        "[Google Map](https://www.google.com/search/dir/?api=1&query={})\n\n".format(
                            when2[0][:3], when2[1], time2, gym[3], gym[4]
                        ),
                    )
                    embed.set_thumbnail(url="https://www.serebii.net/art/th/386-lg.png")
                    embed.add_field(
                        name="#386 Deoxys (Defense Mode)",
                        value=f"Type: {PSYCHIC}\n"
                        f"Weakness: {BUG} {GHOST} {DARK}\n"
                        f"Resists: {FIGHTING} {PSYCHIC}\n"
                        f"Perfect CP: 1299 / 1624",
                        inline=False,
                    )
                    # embed.add_field(name="Participants",
                    #                value=f"1:00 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n1:15 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}\n1:30 - 0 {VALOR} | 0 {MYSTIC} | 0 {INSTINCT}",
                    #                inline=False)

                    async with self.config.guild(guild).active() as act:
                        act.append(channel)

                    await ctx.message.delete()
                    await ctx.send(
                        "{} - {} {} = {}".format(gym[1], when2[0][:3], when2[1], newchan.mention)
                    )
                    await newchan.send(embed=embed)

    @commands.command()
    @checks.admin_or_permissions(manage_channels=True)
    async def forceexraid(self, ctx, when, where):
        """
        Forcibly create an EX Raid channel
        """
        sqlkeys = await self.config.keys.sql()
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
            colour=discord.Colour(0x58BA8B),
            description="**Scheduled for {} {} @ {}**\n\n"
            "{}\n"
            "[Google Map](https://www.google.com/search/dir/?api=1&query={})\n\n".format(
                when2[0][:3], when2[1], time2, gym[3], gym[4]
            ),
        )
        embed.set_thumbnail(url="https://www.serebii.net/art/th/386-fr.png")
        embed.add_field(
            name="#386 Deoxys (Attack Mode)",
            value=f"Type: {PSYCHIC}\n"
            f"Weakness: {BUG} {GHOST} {DARK}\n"
            f"Resists: {FIGHTING} {PSYCHIC}\n"
            f"Perfect CP: 1474 / 1842",
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
            msg = await ctx.channel.get_message(msgid)
            await self.on_message(msg)
            await ctx.message.delete()
