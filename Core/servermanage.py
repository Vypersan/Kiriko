import discord
from discord import app_commands
from discord.ext import commands
import assets
import utils 
from typing import Optional
from discord.app_commands import choices, Choice
import aiosqlite
from sqlite3 import IntegrityError as duplicate_error
class serverowners(commands.Cog):
    """Specific server mamage commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    


    @app_commands.command(name="editlogs", description="Edit the log channels of your server.")
    @app_commands.describe(messages = "The message log channel", users = "The user log channels.")
    async def editlogs(self, interaction : discord.Interaction, messages: Optional[discord.TextChannel], users: Optional[discord.TextChannel]):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Only people who can ban users can use this command")
        else:
            db = await utils.connect_database()
            check = await db.execute("SELECT messages FROM logchannels WHERE guildid = ?", (interaction.guild.id,))
            check_result = await check.fetchone()
            if not check_result:
                if messages is not None and users is not None:
                    await db.execute("INSERT INTO logchannels VALUES (?, ?, ?)", (interaction.guild.id, messages.id, users.id,))
                    await db.commit()
                    try:
                        await db.close()
                    except ValueError:
                        pass
                    return await interaction.response.send_message(f"🦊 It seems you did not have log channels yet. Added {messages.mention} as the message log and {users.mention} as the user log channel since you provided these.", ephemeral=True)
                else:
                    try:
                        await db.close()
                    except ValueError:
                        pass
                    return await interaction.response.send_message("Sorry you do not have logs set up yet. And you did not provide enough channels to set them up (2 required.) Use /setuplogs instead!")
            else:
                if messages is not None:
                    if users is not None:
                        await db.execute(f"UPDATE logchannels SET messages = {messages.id} WHERE guildid = ?", (interaction.guild.id,))
                        await db.commit()
                        await db.execute(f"UPDATE logchannels SET users = {users.id} WHERE guildid = ?", (interaction.guild.id,))
                        await db.commit()
                        try:
                            await db.close()
                        except ValueError:
                            pass
                        return await interaction.response.send_message(f"🦊 Updated the channels. Messages are now logged in {messages.mention} and users are now logged in {users.mention}", ephemeral=True)
                    else:
                        await db.execute(f"UPDATE logchannels SET messages = {messages.id} WHERE guildid = ?", (interaction.guild.id,))
                        await db.commit()
                        try:
                            await db.close()
                        except ValueError:
                            pass
                        return await interaction.response.send_message(f"🦊 Updated the Message log channel to {messages.mention}", ephemeral=True)
                else:
                    if users is not None:
                        await db.execute(f"UPDATE logchannels SET users = {users.id} WHERE guildid = ?", (interaction.guild.id,))
                        await db.commit()
                        try:
                            await db.close()
                        except ValueError:
                            pass
                        return await interaction.response.send_message(f"🦊 Updated the user log channel to {users.mention}", ephemeral=True)
                if messages == None and users == None:
                    try:
                        await db.close()
                    except ValueError:
                        pass
                    return await interaction.response.send_message("Dummy, you forgot to provide channels to update")

    @app_commands.command(name="clearlogs", description="Remove all log channels stored in our database.")
    async def clearlogs(self, interaction : discord.Interaction):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("Only people who can ban users can use this command")
        else:
            db = await utils.connect_database()
            try:
                await db.execute("DELETE FROM logchannels WHERE guildid = ?", (interaction.guild.id,))
            except aiosqlite.OperationalError:
                try:
                    await db.close()
                except ValueError:
                    pass
                return await interaction.response.send_message(f"🦊 You do not have any logs set up!", ephemeral=True)
            await db.commit()
            try:
                await db.execute("DELETE FROM welcome WHERE guildID = ?", (interaction.guild.id,))
            except aiosqlite.OperationalError:
                pass
            await db.commit()
            try:
                await db.close()
            except ValueError:
                pass
            return await interaction.response.send_message("🦊 Deleted your log channels.", ephemeral=True)



    @app_commands.command(name="serversetup", description="Set up the bot to work with your server")
    @utils.check_blacklist()
    @commands.has_permissions(kick_members=True)
    async def serversetup(self, interaction : discord.Interaction , userlogs:discord.TextChannel, messagelogs:discord.TextChannel, welcomechannel:discord.TextChannel):
        db = await utils.connect_database()
        await db.execute("CREATE TABLE IF NOT EXISTS welcome (guildID INTEGER UNIQUE, welcomechannel TEXT)")
        await db.commit()
        await db.execute("CREATE TABLE IF NOT EXISTS logchannels (guildid INTEGER PRIMARY KEY, messages TEXT, users TEXT)")
        await db.commit()
        try:
            await db.execute("INSERT INTO welcome VALUES (?, ?)", (interaction.guild.id, welcomechannel.id,))
        except aiosqlite.IntegrityError:
            await interaction.response.send_message("🦊 This server already has a welcome channel. use `/editwelcome` instead.")
            await db.commit()
            try:
                await db.close()
            except ValueError:
                pass
            return await interaction.response.send_message(f"🦊Set your user logs to {userlogs.mention} and message log to {messagelogs.mention} but this server already has a welcome message channel. `use /editwelcome` instead!")
        await db.commit()
        embedVar = discord.Embed(title='Server Setup', color=discord.Color.green())
        try:
            await db.execute("INSERT INTO logchannels VALUES (?, ?, ?)", (interaction.guild.id, messagelogs.id, userlogs.id,))
        except aiosqlite.IntegrityError:
            try:
                await db.close()
            except ValueError:
                pass
            return await interaction.response.send_message("🦊 Set your welcome channel. However this server already has log channels set up. Use `/editlogs` instead")
        embedVar.add_field(name="Welcome channel", value=welcomechannel.mention, inline=False)
        embedVar.add_field(name="User log channel", value=userlogs.mention, inline=False)
        embedVar.add_field(name="Message log channel", value=messagelogs.mention, inline=False)
        await db.commit()
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(embed=embedVar)


    @app_commands.command(name="editwelcome", description="Edit the welcome channel")
    @utils.check_blacklist()
    @commands.has_permissions(kick_members=True)
    async def editlogs(self, interaction : discord.Interaction, welcomechannel:discord.TextChannel):
        db = await utils.connect_database()
        await db.execute("DELETE FROM welcome WHERE guildID = ?", (interaction.guild.id,))
        await db.commit()
        await db.execute("INSERT INTO welcome VALUES (?, ?)", (interaction.guild.id, welcomechannel.id,))
        await db.commit()
        try:
            await db.close()
        except ValueError:
            pass
        return await interaction.response.send_message(f"🦊 Set your new welcome channel to {welcomechannel.mention}")
    
    @commands.Cog.listener()
    async def on_serversetup_error(self, interaction : discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CheckFailure):
            return await interaction.response.send_message("🦊 Sorry you do not have enough permissions to use this command.", ephemeral=True)

    @commands.Cog.listener()
    async def on_editlogs_error(self, interaction : discord.Interaction, error: app_commands.CommandInvokeError):
        if isinstance(error, app_commands.CheckFailure):
            return await interaction.response.send_message("🦊 Sorry you do not have enough permissions to use this command.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(serverowners(bot))
