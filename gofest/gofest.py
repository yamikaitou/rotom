from redbot.core import commands, Config, checks
import discord
from discord.ext import tasks
import random
import math
from datetime import datetime


class GoFest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.contest.start()

    @commands.is_owner()
    @commands.command()
    async def gofest(self, ctx):
        
        guild = self.bot.get_guild(331635573271822338)
        overwrite = discord.PermissionOverwrite()
        overwrite.send_messages = False
        overwrite.read_messages = True


        chan = await guild.create_text_channel(
                "contest-chat",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.send("Welcome to Go-Fest 2020! It has been a while since we have had a contest so lets have *multiple* for our first ever Play-At-Home Go-Fest. Check out each channel and read the rules for them. They are each different and have very specific entry periods. I will be controlling access to the channels, so they will only be open during the applicable period. Any questions, poke YamiKaitou")

        chan = await guild.create_text_channel(
                "ar-photos",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="AR Photo Contest", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 26 9pm")
        embed.add_field(name="Rules", value="* Take an AR or AR+ Snapshot of any Pokemon\n* Post the screenshot in this channel\n* React to your favorite screenshots. Any reaction will count as a vote but you can only vote once per photo.")
        embed.add_field(name="Notes", value="* All entries must be submitted by 9pm on Sunday\n* Voting will end at 10pm on Tuesday\n* Multiple entries are allowed, but you can only win once. Please post each entries as a separate message to allow for proper voting\n* Screenshots must be taken with the in-game feature (no collages, no device screenshots, no camera photos, etc)")
        embed.add_field(name="Prize", value="1st Place: $15 Gift Card for Apple App Store or Google Play\n2nd Place: $10 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out.")
        msg = await chan.send(embed=embed)
        await msg.pin()
        
        chan = await guild.create_text_channel(
                "most-shinies-saturday",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Most Shinies (Saturday)", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 25 9pm")
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of the Go-Fest Day (honor system, I probably won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 9pm on Saturday\n* You can only win 1 of the Most Shiny contests")
        embed.add_field(name="Prize", value="$10 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out.")
        msg = await chan.send(embed=embed)
        await msg.pin()
        
        chan = await guild.create_text_channel(
                "most-shinies-sunday",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Most Shinies (Sunday)", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 26 10am - July 26 9pm")
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of Go-Fest Day (honor system, I probably won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 9pm on Sunday\n* You can only win 1 of the Most Shiny contests")
        embed.add_field(name="Prize", value="$10 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out.")
        msg = await chan.send(embed=embed)
        await msg.pin()

        chan = await guild.create_text_channel(
                "most-shinies-weekend",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Most Shinies (Weekend)", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 26 10pm")
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of Go-Fest Weekend (honor system, I probably won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Sunday\n* You can only win 1 of the Most Shiny contests")
        embed.add_field(name="Prize", value="$10 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out.")
        msg = await chan.send(embed=embed)
        await msg.pin()

        chan = await guild.create_text_channel(
                "highest-iv-rotom",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Highest IV of Rotom (Wash Form)", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 26 10pm")
        embed.add_field(name="Rules", value="* Take snapshots to get Photobombed by Rotom during GoFest\n* Post your IV Appraisal for Rotom")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Sunday\n* You can get 5 encounters per day")
        embed.add_field(name="Prize", value="$15 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out (most likely by weight, so make sure you screenshot it unevolved and include the weight).")
        msg = await chan.send(embed=embed)
        await msg.pin()

        chan = await guild.create_text_channel(
                "highest-iv-victini",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Highest IV Victini", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 30 10pm")
        embed.add_field(name="Rules", value="* Complete the Special Research given on Day 2\n* Post your IV Appraisal for Victini")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Thursday\n* These rules may be modified based on the contents of the Special Research, Rotom will announce the Special Pokemon for this contest before the start of the Entry Period")
        embed.add_field(name="Prize", value="$15 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out (most likely by weight, so make sure you screenshot it unevolved and include the weight).")
        msg = await chan.send(embed=embed)
        await msg.pin()
        
    @tasks.loop(minutes=1.0)
    async def contest(self):
        dt = datetime.now()
        guild = self.bot.get_guild(331635573271822338)
        permstart = discord.PermissionOverwrite()
        permstart.read_messages = True
        permstart.send_messages = True
        permstart.add_reactions = True
        permend = discord.PermissionOverwrite()
        permend.read_messages = True
        permend.send_messages = False
        permend.add_reactions = True
        permvote = discord.PermissionOverwrite()
        permvote.read_messages = True
        permvote.send_messages = False
        permvote.add_reactions = False
        roles = [335996722775851009, 335997012619296770, 335997104088416256]

        # Start 7/25 10am
        if 1595689800 <= int(math.floor(dt.timestamp())) < 1595689860:
            for role in roles:
                await self.bot.get_channel(735863543634722877).set_permissions(guild.get_role(role), overwrite=permstart)
                await self.bot.get_channel(735863548596584478).set_permissions(guild.get_role(role), overwrite=permstart)
                await self.bot.get_channel(735863556745986068).set_permissions(guild.get_role(role), overwrite=permstart)
                await self.bot.get_channel(735863560726380658).set_permissions(guild.get_role(role), overwrite=permstart)
                await self.bot.get_channel(735863565826916418).set_permissions(guild.get_role(role), overwrite=permstart)
            print("Start 7/25 10am")
        # End 7/25 9pm
        elif 1595728800 <= int(math.floor(dt.timestamp())) < 1595728860:
            for role in roles:
                await self.bot.get_channel(735863548596584478).set_permissions(guild.get_role(role), overwrite=permend)
            print("End 7/25 9pm")
        # Start 7/26 10am
        elif 1595775600 <= int(math.floor(dt.timestamp())) < 1595775660:
            for role in roles:
                await self.bot.get_channel(735863552019136535).set_permissions(guild.get_role(role), overwrite=permstart)
            print("Start 7/26 10am")
        # End 7/26 9pm
        elif 1595815200 <= int(math.floor(dt.timestamp())) < 1595815260:
            for role in roles:
                await self.bot.get_channel(735863543634722877).set_permissions(guild.get_role(role), overwrite=permend)
                await self.bot.get_channel(735863552019136535).set_permissions(guild.get_role(role), overwrite=permend)
            print("End 7/26 9pm")
        # End 7/26 10pm
        elif 1595818800 <= int(math.floor(dt.timestamp())) < 1595818860:
            for role in roles:
                await self.bot.get_channel(735863556745986068).set_permissions(guild.get_role(role), overwrite=permend)
                await self.bot.get_channel(735863560726380658).set_permissions(guild.get_role(role), overwrite=permend)
            print("End 7/26 10pm")
        # Vote 7/28 10pm
        elif 1595991600 <= int(math.floor(dt.timestamp())) < 1595991660:
            for role in roles:
                await self.bot.get_channel(735863556745986068).set_permissions(guild.get_role(role), overwrite=permvote)
            print("Vote 7/28 10pm")
        # End 7/30 10pm
        elif 1596164400 <= int(math.floor(dt.timestamp())) < 1596164460:
            for role in roles:
                await self.bot.get_channel(735863556745986068).set_permissions(guild.get_role(role), overwrite=permend)
            print("End 7/30 10pm")
        else:
            if dt.minute == 0:
                print("I need to know I'm running")

        


    @contest.before_loop
    async def before_contest(self):
        await self.bot.wait_until_ready()
