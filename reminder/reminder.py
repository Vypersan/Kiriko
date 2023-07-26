import datetime
import discord
from discord.app_commands import Choice
from discord import app_commands
from discord.ext import commands
import time
import platform
import asyncio
import pytz
import utils as utilities
from utils import logname
current_uptime = time.time()

# Yo! It's time to get going, the reminder's going off
# Whoa! Something ain't right with that format you put in. Let's try this: `YYYY-MM-DD HH:MM TIMEZONE` got it?
#Hey now, that date's in the past. I don't know how it is where you are, but here on Earth, you gotta live in the present. So come on, get with it.
#I promise to remind you about {remindertopic} on {date} at {time} ({timezone}
#Yo {interaction.user.mention}! It's time to get going, the reminder for {remindertopic} is going off
class reminder(commands.Cog):
    """Reminder commands for users"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    @app_commands.command(name="reminder", description="Set a reminder for yourself")
    @app_commands.describe(date = "The date in the following format: yyyy-mm-dd", time = "The time in the following format: HH:MM",timezone = "The timezone you are in. Example: Europe/Amsterdam", remindertopic = "The thing you want to be reminded for." )
    @utilities.check_blacklist()
    async def remindme(self, interaction : discord.Interaction,date:str, time:str, timezone:str, remindertopic:str ):
        channel = await self.bot.fetch_channel(interaction.channel.id)
        try:
            reminder_datetime_str = f'{date} {time}'
            reminder_datetime = datetime.datetime.strptime(reminder_datetime_str, '%Y-%m-%d %H:%M')
            tz = pytz.timezone(timezone)
            reminder_datetime = tz.localize(reminder_datetime)
        except ValueError:
            return await channel.send(f"Whoa! Something ain't right with that format you put in. Let's try this: `YYYY-MM-DD HH:MM TIMEZONE` got it? {interaction.user.mention}")
        current_datetime = datetime.datetime.now(pytz.utc)
        await interaction.response.send_message("Working on it.....")
        time_difference = reminder_datetime - current_datetime
        if time_difference.total_seconds() <= 0:
            return await channel.send("Hey now, that date's in the past. I don't know how it is where you are, but here on Earth, you gotta live in the present. So come on, get with it.")
        await channel.send(f"I promise to remind you about `{remindertopic}` on {date} at {time} ({timezone})")
        await asyncio.sleep(time_difference.total_seconds())
        reminder_message = f"Yo {interaction.user.mention}! It's time to get going, the reminder for `{remindertopic}` is going off"
        await channel.send(reminder_message)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(reminder(bot))

