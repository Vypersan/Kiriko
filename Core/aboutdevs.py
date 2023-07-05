import datetime
import platform
import time
import discord
from discord import app_commands
import utils as  utilities
from discord.ext import commands

class aboutdevs(commands.Cog):
    """Find information about developers"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(aboutdevs(bot))