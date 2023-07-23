import assets
import discord
import utils
from utils import load_json as jlload
from argparse import ArgumentParser
from typing import Optional
from discord.ext import commands
from discord.ext.commands import Context, Greedy
from discord import app_commands
import sqlite3
from sqlite3 import IntegrityError as duplicate_error
loader = jlload(assets.jsonfile)
token = loader["token"]
invite = loader["invite_url"]
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.moderation = True
parser = ArgumentParser(description="The console that allows the bot to run in certain modes")
parser.add_argument("--developer", action="store_true", help="Run the bot in developer mode.")
args = parser.parse_args()
# Normal server 981259218122338354  |||||| Dev server 1038431009676460082
MY_GUILD = discord.Object(id=1038431009676460082)

if args.developer:
    appID = loader["devID"]
else:
    appID= loader["appID"]


async def prefix_adder(guild):
    db = await utils.connect_database()
    try:
        await db.execute("INSERT INTO guilds VALUES (?, ?)", (guild.id, "kiriko-",))
        utils.print_info_line(f"Added {guild.name} to the prefix db as it was not added yet.")
    except duplicate_error:
        utils.print_warning_line(f"Did not add {guild.name} to the prefix db as it already is in there.")
        pass
    await db.commit()
    try:
        await db.close()
    except ValueError:
        pass

async def get_prefix(bot, message):
    db =  sqlite3.connect("./database.db")
    prefix = db.execute("SELECT prefix FROM guilds WHERE guildID = ?", (message.guild.id,))
    prefix_result = prefix.fetchone()
    if prefix_result:
        try:
            db.close()
        except ValueError:
            pass
        return prefix_result[0]
    else:
        await prefix_adder(message.guild)


class kiriko(commands.Bot):
    """The main bot class"""
    def __init__(self, intents = intents):
        super().__init__(intents=intents, command_prefix =  get_prefix, application_id = appID, description="Let the kitsune guide you")
    
    async def setup_hook(self) -> None:
        self.tree.copy_global_to(guild=MY_GUILD)
    
    async def on_ready(self):
        """On ready event"""
        utils.print_info_line(f"{self.user} has connected to the gateaway")
        db = await utils.connect_database()
        for extension in assets.modules:
            await kirikobot.load_extension(extension)
            utils.print_info_line(f"Loaded {extension}")
            utils.write_log(f'Loaded {extension}')
        for guild in kirikobot.guilds:
            await prefix_adder(guild)
        await kirikobot.change_presence(activity=discord.Game(name="Cleaning the shrine"))
        if args.developer:
            dev_invite = loader["dev_url"]
            utils.print_info_line(dev_invite)
            utils.print_info_line("Running bot in developer mode.")
        else:
            utils.print_info_line(invite)
        utils.print_info_line("Loaded everything and bot is online.")
        utils.write_log(f"Bot started on {utils.logname_pretty}")



kirikobot = kiriko(intents= intents)
kirikobot.remove_command("help")
tree = kirikobot.tree


@kirikobot.command(name="synccmd")
@utils.is_bot_admin()
async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[str] = None) -> None:
    if not guilds:
        if spec == "guild":
            synced = await ctx.bot.tree.sync()
        elif spec == "copy":
            ctx.bot.tree.copy_global_to(guild=MY_GUILD)
            synced = await ctx.bot.tree.sync()
        elif spec == "delete":
            ctx.bot.tree.clear_commands()
            await ctx.bot.tree.sync()
            synced = []
        else:
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        utils.print_info_line(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return
    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1
    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@kirikobot.command()
async def help(ctx):
    await ctx.reply("You can find all commands at https://little-fox.info/foxguard/documentation ")

@kirikobot.listen()
async def on_guild_join(guild:discord.Guild):
    await prefix_adder(guild)
    botowner = await kirikobot.fetch_user(521028748829786134)

@tree.error
async def on_app_command_error(interaction : discord.Interaction, error: discord.app_commands.errors.AppCommandError):
    if isinstance(error, discord.app_commands.errors.CheckFailure):
        if str(interaction.command.checks.copy()).__contains__("check_blacklist"):
            await interaction.response.send_message("You are blacklisted. Please read our terms of service to appeal. <https://little-fox.info/general-bot-terms-of-service>", ephemeral=True)
        if str(interaction.command.checks.copy().__contains__("has_permissions")):
            await interaction.response.send_message("Sorry you do not have permissions to do this!", ephemeral=True)
    else:
        print(error)


if __name__ == "__main__":
    if args.developer:
        developer_token = loader["devtoken"]
        kirikobot.run(developer_token)
    else:
        kirikobot.run(token)