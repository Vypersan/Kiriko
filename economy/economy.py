import aiosqlite
import utils
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from economy.econgen import random_balance
import economy.econgen as eg
import datetime
import humanize


class economy(commands.Cog):
    """Economy commands for users to use. Includes db"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name="beg", description="Beg the kitsune spirit for some donuts to eat!")
    @utils.check_blacklist()
    async def beg(self, interaction :discord.Interaction):
        db = await utils.connect_database()
        new_donuts = random_balance()
        embed = discord.Embed(color=discord.Color.green())
        check_for_balance = await db.execute("SELECT balance FROM economy WHERE userid = ?", (interaction.user.id,))
        current_balance = await check_for_balance.fetchone()
        if not current_balance:
            await db.execute("INSERT INTO economy VALUES (?, ?)", (interaction.user.id, new_donuts,))
            await db.commit()
            embed.description = f"You did not have any donuts so the kitsune spirit blessed you with  {new_donuts} 🍩 donut(s)"
        else:
            updated_balace = int(current_balance[0]) + new_donuts
            await db.execute(f"UPDATE economy SET balance = {updated_balace} WHERE userid = ?", (interaction.user.id,))
            await db.commit()
            embed.description = f"The kitsune spirit has blessed you with {new_donuts} 🍩 donut(s), yum!"
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(embed=embed)
        

    @app_commands.command(name="balance", description="Check the amount of donuts you have")
    @utils.check_blacklist()
    async def balance(self, interaction :discord.Interaction):
        db = await utils.connect_database()
        current_balance = await db.execute("SELECT balance FROM  economy WHERE userid = ?", (interaction.user.id,))
        current_balance_check = await current_balance.fetchone()
        if not current_balance_check:
            embed = discord.Embed(color=interaction.user.top_role.color, description="Aww it seems you do not have anything. Here.. Have one of mine 🍩")
            await db.execute("INSERT INTO economy VALUES (?, ?)", (interaction.user.id, 1,))
            await db.commit()
        else:
            embed = discord.Embed(color = interaction.user.top_role.color, description=f"You have {current_balance_check[0]} 🍩 donut(s)")
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Get some donuts for free!")
    @utils.check_blacklist()
    @app_commands.checks.cooldown(1, 86400)
    async def daily(self, interaction : discord.Interaction):
        embed = discord.Embed(title="You went to the fox festival and bought yourself 50 🍩 donuts.")
        db = await utils.connect_database()
        user_id = str(interaction.user.id)
        current_balance = await db.execute("SELECT balance FROM  economy WHERE userid = ?", (user_id,))
        current_balance_check = await current_balance.fetchone()
        if not current_balance_check:
            await db.execute("INSERT INTO economy VALUES (? ,? ) ", (user_id, "50",))
            await db.commit()
            embed.description = "Your new balance is 50 🍩Donut(s)"
        else:
            utils.print_info_line(current_balance_check[0])
            new_balance = int(current_balance_check[0]) + 50
            await db.execute(f"UPDATE ECONOMY SET BALANCE = {new_balance} WHERE userid = ?", (user_id,))
            await db.commit()
            embed.description = f"Your new balance is `{new_balance} 🍩 Donut(s)`"
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(embed=embed)
    

    @app_commands.command(name="search", description="Search for some donuts")
    @utils.check_blacklist()
    @app_commands.checks.cooldown(1, 60)
    async def search(self, interaction : discord.Interaction):
        db = await utils.connect_database()
        random_msg = eg.random_messages_gen()
        found_donuts = random_balance()
        message_select = f"m{random_msg}"
        msg_to_send = str(eg.BegMsg[message_select].value).format(found_donuts)
        embed = discord.Embed(title=msg_to_send, color=interaction.user.top_role.color)
        current_balance = await db.execute("SELECT balance FROM economy WHERE userid = ?", (interaction.user.id,))
        current_balance_check = await current_balance.fetchone()
        if not current_balance_check:
            await db.execute("INSERT INTO economy VALUES (?, ?)",(interaction.user.id, found_donuts))
            await db.commit()
            embed.description = f"Your new balance is `{found_donuts}` Donut(s)"
            try:
                await db.close()
            except ValueError:
                pass
        else:
            new_balance = int(current_balance_check[0]) + found_donuts
            await db.execute(f"UPDATE ECONOMY SET balance = {new_balance} WHERE userid = ?", (interaction.user.id,))
            await db.commit()
            embed.description = f"Your new balance is `{new_balance}` Donut(s)"
            try:
                await db.close()
            except ValueError:
                pass
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(embed=embed)
    ## Error handling

    @daily.error
    async def on_daily_error(self, interaction : discord.Interaction, error: app_commands.AppCommandError):
        err_msg = str(error)
        new_msg = err_msg.replace("You are on cooldown. Try again in ", "")
        new_msg_final = new_msg.replace("s", "")
        seconds = float(new_msg_final)
        cooldown_time = datetime.timedelta(seconds=seconds)
        cooldown_time_clean = humanize.naturaldelta(cooldown_time)
        await interaction.channel.send(f"Hey {interaction.user.mention} listen up,  You can use /{interaction.command.name} again in {cooldown_time_clean}. Got it?")

    @search.error
    async def on_search_error(self, interaction : discord.Interaction, error: app_commands.AppCommandError):
        err_msg = str(error)
        new_msg = err_msg.replace("You are on cooldown. Try again in ", "")
        new_msg_final = new_msg.replace("s", "")
        seconds = float(new_msg_final)
        cooldown_time = datetime.timedelta(seconds=seconds)
        cooldown_time_clean = humanize.naturaldelta(cooldown_time)
        await interaction.channel.send(f"Hey {interaction.user.mention} listen up,  You can use /{interaction.command.name} again in {cooldown_time_clean}. Got it?")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(economy(bot))
