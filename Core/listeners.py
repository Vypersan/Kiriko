import discord
from discord.ext import commands
import utils
from datetime import datetime
current_date_pretty = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
class eventlist(commands.Cog):
    """Events and listeners"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, command):
        utils.write_log(f"[{current_date_pretty}]    {command.command} by {command.author}")
        utils.print_info_line(f"{command.command} issued by {command.author}")

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        try:
            utils.write_log(f"[{current_date_pretty}]    {interaction.command.name} issued by {interaction.user}")
        except AttributeError:
            pass
        try:
            utils.print_info_line(f"{interaction.command.name} issued by {interaction.user}")
        except AttributeError:
            pass

    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,  error:commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            utils.print_exception_msg(f"Invalid command was issued by {ctx.author}. Traceback: {error}")
            utils.write_log(f"[{current_date_pretty}]    {ctx.author} issued a invalid command. Traceback: {error}")
            return await ctx.reply("Sorry this command does not exist.")
        if isinstance(error, commands.MissingPermissions):
            utils.print_exception_msg(f"User missing permissions for the {ctx.command} that was issued in {ctx.guild.name}.")
            utils.write_log(f"[{current_date_pretty}]    {ctx.author} is  missing permission(s). {error}")
            await ctx.reply(f"Your clearance is not high enough to execute this. {error}")
        else:
            utils.print_exception_msg(f"Invalid command issued. Traceback: {error}")
            utils.write_log(f"[{current_date_pretty}]    {ctx.author} issued {ctx.command} but something went wrong. {error}")
            await ctx.reply(f"Sorry, something went wrong. `{error}`")
    


# <------------------------------------------------------------------------------------------------------------------------------------------->
# Messages
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        db = await utils.connect_database()
        Delete_embed = discord.Embed(title=f"Message deleted by {message.author.name}", color=discord.Color.red())
        Delete_embed.set_thumbnail(url=message.author.avatar.url)
        logchannel = await db.execute("SELECT messages FROM logchannels WHERE guildid = ?", (message.guild.id,))
        logchannel_result = await logchannel.fetchone()
        if message.author.bot:
            return
        if message.guild is None:
            return
        if logchannel_result is not None:
            channel = self.bot.get_channel(int(logchannel_result[0]))
            Delete_embed.add_field(name="Deleted message:", value=message.content, inline=False)
            Delete_embed.add_field(name="Author ID:", value=message.author.id)
            Delete_embed.add_field(name="Channel:", value=message.channel.mention)
            await channel.send(embed = Delete_embed)
            try:
                await db.close()
            except ValueError:
                pass
        else:
            try:
                await db.close()
            except ValueError:
                pass
            return
    
    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        db = await utils.connect_database()
        edit_embed = discord.Embed(title=f"Message edited by {message_after.author.name}", color = discord.Color.orange())
        logchannel = await db.execute("SELECT messages FROM logchannels WHERE guildid = ?", (message_after.guild.id,))
        logchannel_result = await logchannel.fetchone()
        if message_after.author.bot:
            return
        if message_after.guild is None:
            return
        if logchannel_result is not None:
            channel = self.bot.get_channel(int(logchannel_result[0]))
            edit_embed.set_thumbnail(url=message_after.author.avatar.url)
            edit_embed.add_field(name="Before:", value=message_before.content, inline=False)
            edit_embed.add_field(name="After:", value=message_after.content, inline=False)
            edit_embed.add_field(name="Author ID:", value=message_after.author.id, inline=False)
            edit_embed.add_field(name="Channel:", value=message_after.channel.mention, inline=False)
            await channel.send(embed = edit_embed)
            try:
                await db.close()
            except ValueError:
                pass
        else:
            try:
                await db.close()
            except ValueError:
                pass
# <------------------------------------------------------------------------------------------------------------------------------------------->
# Users    
# <------------------------------------------------------------------------------------------------------------------------------------------->
    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        utils.print_info_line("On member join event called")
        join_embed = discord.Embed(title='User Joined', description='', color=discord.Color.green())
        date_format = "%a, %d %b %Y %I:%M %p"
        join_embed.set_thumbnail(url=member.avatar.url)
        join_embed.add_field(name="Name", value=member, inline=False)
        join_embed.add_field(name="ID", value=member.id, inline=False)
        join_embed.add_field(name="Created at:", value=member.created_at.strftime(date_format), inline=False)
        db = await utils.connect_database()
        logchannel = await db.execute("SELECT users FROM logchannels WHERE guildid = ?", (member.guild.id,))
        logchannel_result = await logchannel.fetchone()
        try:
            send_to_channel = await self.bot.fetch_channel(logchannel_result[0])
        except TypeError:
            try:
                await db.close()
            except ValueError:
                pass
            return
        try:
            await db.close()
        except ValueError:
            pass
        return await send_to_channel.send(embed=join_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        utils.print_info_line("On member leave event called")
        leave_embed = discord.Embed(title='User Left', description='', color=discord.Color.red())
        date_format = "%a, %d %b %Y %I:%M %p"
        leave_embed.set_thumbnail(url=member.avatar.url)
        leave_embed.add_field(name="Name", value=member, inline=False)
        leave_embed.add_field(name="ID", value=member.id, inline=False)
        leave_embed.add_field(name="Created at:", value=member.created_at.strftime(date_format), inline=False)
        db = await utils.connect_database()
        logchannel = await db.execute("SELECT users FROM logchannels WHERE guildid = ?", (member.guild.id,))
        logchannel_result = await logchannel.fetchone()
        try:
            send_to_channel = await self.bot.fetch_channel(logchannel_result[0])
        except TypeError:
            try:
                await db.close()
            except ValueError:
                pass
            return
        try:
            await db.close()
        except ValueError:
            pass
        return await send_to_channel.send(embed=leave_embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild : discord.Guild,  member:discord.Member):
        utils.print_info_line("On member ban event called")
        ban_embed = discord.Embed(title='User Banned', description='', color=discord.Color.red())
        fetched_ban = await guild.fetch_ban(member)
        date_format = "%a, %d %b %Y %I:%M %p"
        ban_embed.set_thumbnail(url=member.avatar.url)
        ban_embed.add_field(name="Name", value=member, inline=False)
        ban_embed.add_field(name="ID", value=member.id, inline=False)
        ban_embed.add_field(name="Created at:", value=member.created_at.strftime(date_format), inline=False)
        ban_embed.add_field(name="Reason", value=fetched_ban.reason)
        db = await utils.connect_database()
        logchannel = await db.execute("SELECT users FROM logchannels WHERE guildid = ?", (member.guild.id,))
        logchannel_result = await logchannel.fetchone()
        try:
            send_to_channel = await self.bot.fetch_channel(logchannel_result[0])
        except TypeError:
            try:
                await db.close()
            except ValueError:
                pass
            return
        try:
            await db.close()
        except ValueError:
            pass
        return await send_to_channel.send(embed=ban_embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(eventlist(bot))