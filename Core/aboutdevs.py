import datetime
import platform
import time
import discord
from discord import app_commands
import utils as  utilities
from discord.ext import commands
from discord.app_commands import Choice

class aboutdevs(commands.Cog):
    """Find information about developers"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="aboutdevs", description="Get information about developers")
    @utilities.check_blacklist()
    @app_commands.describe(dev = "The developer you want to view information on.")
    @app_commands.choices(dev = [
        Choice(name="--Kitsune", value="521028748829786134")
    ])
    async def _aboutdevs_(self, interaction :discord.Interaction , dev:str):
        embed  = discord.Embed(title="About Developers")
        member = await interaction.client.fetch_user(dev)
        if dev == "521028748829786134":
            embed.add_field(name="Age", value="20", inline=False)
            embed.add_field(name="Nationality", value="Netherlands / Dutch", inline=False)
            embed.add_field(name="About", value="20 year old programmer who loves to create a bunch of projects.", inline=False)
            embed.add_field(name="Hobbies", value="- Programming\n- Playing video games\n- Photography", inline=False)
            embed.add_field(name="Links", value="[Website](https://yokaigroup.gg/members/little_fox/)", inline=False)
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.description = "No developer provided"
        return await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="contributors", description="See all the people who helped out")
    @utilities.check_blacklist()
    async def contribs(self, interaction : discord.Interaction):
        embed = discord.Embed(title="Contributors", color = discord.Color.red())
        embed.add_field(name="foxigoose", value="audio files for sfx command. [Their twitter](https://twitter.com/LoxiGoose)", inline=False)
        embed.add_field(name="catsonmarss", value = "New command ideas [Their twitter](https://twitter.com/catsonmarss)")
        return await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(aboutdevs(bot))