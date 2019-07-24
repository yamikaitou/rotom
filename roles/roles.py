import discord
from redbot.core import commands, __version__, checks, Config
import sys
from typing import Union
import aiohttp
import random


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1977316625, force_registration=True)

        default_guild = {
            "active": 0,
            "channel": 0,
            "roles": {"raid": [], "pkmn": [], "ex": [], "event": [], "new": [], "ban": []},
        }

        self.config.register_guild(**default_guild)

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, rolename=None):
        """
        Adds a role to the user
        :param rolename: Role Name
        """

        guild = ctx.guild
        chan = await self.config.guild(guild).channel()
        if ctx.message.channel.id != chan:
            return

        msg = None

        if rolename is not None:
            try:
                gen = await self.config.guild(guild).roles.raid()
                pkm = await self.config.guild(guild).roles.pkmn()
                exr = await self.config.guild(guild).roles.ex()
                evt = await self.config.guild(guild).roles.event()

                if (
                    rolename not in gen
                    and rolename not in pkm
                    and rolename not in exr
                    and rolename not in evt
                ):
                    raise AttributeError("Invalid Role")

                role = discord.utils.get(ctx.guild.roles, name=rolename)
                if role not in ctx.author.roles:
                    await ctx.author.add_roles(role)
                    await ctx.send("I have given you the role")
                    return
                else:
                    await ctx.author.remove_roles(role)
                    await ctx.send("I have taken the role from you")
                    return
            except AttributeError:
                msg = "I could not find that role, please try again\n"

        embed = discord.Embed(
            title="Available Roles",
            color=discord.Color(random.randint(0x000000, 0xFFFFFF)),
            description="Select one of the roles below to be added/removed from your profile\n\n"
            "Example: !role raids-all\n\n",
        )

        value = ""
        async with self.config.guild(guild).roles.raid() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Locations", value=value)

        value = ""
        async with self.config.guild(guild).roles.pkmn() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Pokemon", value=value)

        value = ""
        async with self.config.guild(guild).roles.ex() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="EX Locations", value=value)

        await ctx.send(content=msg, embed=embed)

    async def on_guild_role_create(self, role):
        async with self.config.guild(role.guild).roles as setting:
            setting.new.append(role.name)

    async def on_guild_role_update(self, before, after):
        if before.name != after.name:
            async with self.config.guild(after.guild).roles as setting:
                if before.name in setting.raid:
                    for entry in setting.raid:
                        if entry == before.name:
                            entry = after.name
                elif before.name in setting.pkmn:
                    for entry in setting.pkmn:
                        if entry == before.name:
                            entry = after.name
                elif before.name in setting.ex:
                    for entry in setting.ex:
                        if entry == before.name:
                            entry = after.name
                elif before.name in setting.event:
                    for entry in setting.event:
                        if entry == before.name:
                            entry = after.name
                elif before.name in setting.new:
                    for entry in setting.new:
                        if entry == before.name:
                            entry = after.name
                elif before.name in setting.ban:
                    for entry in setting.ban:
                        if entry == before.name:
                            entry = after.name
                else:
                    print("Unknown Role")

    @commands.command(hidden=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def roles_first_run(self, ctx, force = 0):
        ran = await self.config.guild(ctx.guild).active() or not force
        if not ran:
            await self.config.guild(ctx.guild).roles.raid.set([])
            await self.config.guild(ctx.guild).roles.pkmn.set([])
            await self.config.guild(ctx.guild).roles.ex.set([])
            await self.config.guild(ctx.guild).roles.event.set([])
            await self.config.guild(ctx.guild).roles.ban.set([])
            await self.config.guild(ctx.guild).roles.new.set([])
            for role in ctx.guild.roles:
                async with self.config.guild(ctx.guild).roles.new() as roles:
                    roles.append(role.name)

            await self.config.guild(ctx.guild).active.set(1)
