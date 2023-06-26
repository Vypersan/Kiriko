import datetime
import platform
import time
import discord
from discord import app_commands
import utils as  utilities
from discord.ext import commands
up_time = time.time()


class userinfo(commands.Cog):
    """User information"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="av", description="Get an user's avatar")
    async def av(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        await interaction.response.send_message(member.avatar.url, ephemeral=False)

    @app_commands.command(name="whois", description="Get user information")
    async def whois(self, interaction: discord.Interaction, user: discord.Member = None):
        """Check to see who this person is, their roles and other stuff. format: whois @user"""
        if user is None:
            user = interaction.user
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=discord.Color.orange(),
                              description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar.url)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(
            name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(interaction.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position",
                        value=str(members.index(user) + 1))
        embed.add_field(name="Registered",
                        value=user.created_at.strftime(date_format))

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(
                len(user.roles) - 1), value=role_string, inline=False)
            embed.set_footer(text='ID: ' + str(user.id))
            return await interaction.response.send_message(embed=embed)
        else:
            embed.add_field(name="Roles:", value="None")
        return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="uptime", description="Check the bot's uptime", auto_locale_strings=True)
    async def uptime(self, interaction: discord.Interaction):
        current_time = time.time()
        difference = int(round(current_time - up_time))
        text = str(datetime.timedelta(seconds=difference))

        embed = discord.Embed(colour=interaction.user.top_role.colour)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text="I am awake!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="followstatus", description="Make the bot post status messages in a channel you decide.")
    @commands.has_permissions(ban_members=True)
    async def followStatus(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Allows people to follow the status channel so they can know when it is down or not."""
        try:
            follow_channel = await self.bot.fetch_channel(1115936655849836634)
            await follow_channel.follow(destination=channel)
            await interaction.response.send_message(f"✅ You will now get status updates in {channel.mention}")
        except Exception as e:
            return await interaction.response.send_message("❌ Sorry failed to follow the status page.")

    @app_commands.command(name="guildinfo", description="Get this guild's information")
    @utilities.check_blacklist()
    async def guildinfo(self, interaction : discord.Interaction):
        """Get info about the guild"""
        guild = interaction.guild
        embed = discord.Embed(title=f"{guild.name}", description=f"{guild.description}")
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Members", value= guild.member_count, inline=False)
        embed.add_field(name="Created at", value= guild.created_at, inline=False)
        embed.add_field(name="Boost level:", value=guild.premium_tier, inline=False)
        embed.add_field(name="Booster count", value=guild.premium_subscription_count,inline=False)
        embed.add_field(name="Max Bitrate", value=f"{guild.bitrate_limit} Bits", inline=False)
        embed.add_field(name="Server MFA level", value=guild.mfa_level, inline=False)
        embed.add_field(name="Server Verification level", value=str(guild.verification_level).upper(), inline=False)
        embed.add_field(name="Role count", value=len(guild.roles))
        embed.add_field(name="Afk timeout", value=f"{guild.afk_timeout} seconds.", inline=False )
        embed.add_field(name="Channels", value=len(guild.channels))
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(userinfo(bot))
