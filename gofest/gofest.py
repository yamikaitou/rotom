from redbot.core import commands, Config, checks
import discord
from discord.ext import tasks
import random


class GoFest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.poll.start()
    
    def cog_unload(self):
        self.poll.cancel()
    
    @poll.before_loop
    async def before_poll(self):
        await self.bot.wait_until_ready()
    
    @tasks.loop(minutes=1.0)
    async def poll(self):
        pass

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
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of the Go-Fest Day (honor system, I won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 9pm on Saturday")
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
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of Go-Fest Day (honor system, I won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 9pm on Sunday")
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
        embed.add_field(name="Rules", value="* Catch Shinies\n* Tell us your final Shiny count at the end of Go-Fest Weekend (honor system, I won't ask for screenshots)")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Sunday")
        embed.add_field(name="Prize", value="$10 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out.")
        msg = await chan.send(embed=embed)
        await msg.pin()

        chan = await guild.create_text_channel(
                "highest-iv-research-saturday",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Highest IV of the Final Pokemon from Day 1 Special Research", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 25 10am - July 27 10pm")
        embed.add_field(name="Rules", value="* Complete the Special Research given on Day 1\n* Post your IV Appraisal for the Special Pokemon that is awarded from the Research")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Monday\n* These rules may be modified based on the contents of the Special Research, Rotom will announce the Special Pokemon for this contest before the start of the Entry Period")
        embed.add_field(name="Prize", value="$15 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out (most likely by weight, so make sure you screenshot it unevolved and include the weight).")
        msg = await chan.send(embed=embed)
        await msg.pin()

        chan = await guild.create_text_channel(
                "highest-iv-research-sunday",
                category=self.bot.get_channel(735618943988793374)
            )
        await chan.set_permissions(guild.get_role(335996722775851009), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997012619296770), overwrite=overwrite)
        await chan.set_permissions(guild.get_role(335997104088416256), overwrite=overwrite)

        embed = discord.Embed(title="Highest IV of the Final Pokemon from Day 2 Special Research", colour=discord.Colour(0x3b4cca))
        embed.set_thumbnail(url="https://lh3.googleusercontent.com/I7GAF9icMRe9lJSiHu-ymM_cR2bTGtU3Hmldc4Qf_yKEmD5JfZ6C6MIkzQBhEmfLu_GPlTAZwRR5SC6NXsIqSw")
        embed.add_field(name="Entry Period", value="July 26 10am - July 28 10pm")
        embed.add_field(name="Rules", value="* Complete the Special Research given on Day 2\n* Post your IV Appraisal for the Special Pokemon that is awarded from the Research")
        embed.add_field(name="Notes", value="* All entries must be submitted by 10pm on Tuesday\n* These rules may be modified based on the contents of the Special Research, Rotom will announce the Special Pokemon for this contest before the start of the Entry Period")
        embed.add_field(name="Prize", value="$15 Gift Card for Apple App Store or Google Play\n* Winner will be contacted via DM. Code will be delivered as a screenshot of the physical card (sorry, I'm not mailing it to you)\n* Ties will be handled accordingly, I'll figure something out (most likely by weight, so make sure you screenshot it unevolved and include the weight).")
        msg = await chan.send(embed=embed)
        await msg.pin()
        
