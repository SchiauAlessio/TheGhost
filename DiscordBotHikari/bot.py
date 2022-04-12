import logging
import datetime as dt
import hikari
import lightbulb
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
import sake
import logging
from lightbulb import commands
from aiohttp import ClientSession
import aiosqlite
from apscheduler.triggers.cron import CronTrigger
import os
from dotenv import load_dotenv
load_dotenv()
log = logging.getLogger(__name__)
token = os.getenv('BOT_TOKEN') #TheGhost
# token=os.getenv('THE_SUPREME_GHOST_BOT_TOKEN') #TheSupremeGhost #TheSupremeGhost
bot = lightbulb.BotApp(token,
                       prefix="$$",
                       default_enabled_guilds=int(os.getenv('THE_GHOSTS_SERVER_ID')),
                       help_slash_command=True,
                       case_insensitive_prefix_commands=True,

                       # intents=hikari.Intents.ALL,
                       )  # remove this when releasing full version of bot

bot.d.scheduler = AsyncIOScheduler()
bot.d.scheduler.configure(timezone=utc)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

bot.load_extensions_from("extensions")


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    # creating the database
    bot.d.db = await aiosqlite.connect("Data/database.sqlite3")
    await bot.d.db.execute("pragma journal_mode=wal")
    with open("Data/build.sql") as f:
        await bot.d.db.executescript(f.read())
    bot.d.scheduler.add_job(bot.d.db.commit, CronTrigger(second=0))
    log.info("Database connection established")

    # creating the cache
    cache = sake.redis.RedisCache("redis://127.0.0.1", bot)
    await cache.open()
    log.info("Connected to redis server!")

    # create session
    bot.d.scheduler.start()
    bot.d.session = ClientSession(trust_env=True)
    log.info("AIOHTTP session started")


@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    bot.d.scheduler.add_job(lambda: log.info(f"Ping {bot.heartbeat_latency * 1000:.0f} ms"),
                            CronTrigger(second="*/59"),
                            name="ping")
    await bot.rest.create_message(int(os.getenv('MODERATORS_CHAT_CHANNEL_ID')), "Bot online") #the id of the channel where you want the bot to send the message


@bot.listen(hikari.StoppingEvent)
async def on_stopping(event: hikari.StoppingEvent) -> None:
    bot.d.scheduler.shutdown()
    await bot.d.session.close()
    log.info("AIOHTTP session closed")
    await bot.d.db.close()
    log.info("Database connection closed")
    await bot.rest.create_message(
        int(os.getenv('MODERATORS_CHAT_CHANNEL_ID')),
        "Bot now offline"
    )


@bot.listen(hikari.GuildMessageCreateEvent)
async def on_message_create(event: hikari.GuildMessageCreateEvent) -> None:
    if event.message.content.lower() == "tell me a secret":
        await event.message.respond("You are extremely stupid", reply=True, mentions_reply=True)

    if event.message.content.lower() == "embed" or event.message.content.lower() == "server invite" and not event.author.is_bot:
        embed = (
            hikari.Embed(
                title="The Ghosts server invite link",
                description="https://discord.gg/BJky9WrE56",
                colour=event.message.member.get_top_role().colour,
                timestamp=dt.datetime.now().astimezone(),
            )
                .set_author(name="The Ghost")
                .set_footer(
                f"Requested by {event.message.member.display_name}",
                icon=event.message.member.avatar_url,
            )
                .set_thumbnail(event.get_guild().icon_url)
                # .add_field(name="Name", value="Value", inline=True)
        )
        await event.message.respond(embed)

    if event.message.content == "attachment":
        try:
            await event.message.respond(hikari.File("Images/EldenRing.jpg"))
        except hikari.ClientHTTPResponseError:
            await event.message.respond("File is too large!")

    if "sus" in event.message.content.lower() and not event.author.is_bot:
        await event.message.respond("Did I hear SUS?")
        await event.message.respond(os.getenv("SUS_URL"))

@bot.listen(hikari.ExceptionEvent)
async def on_error(event: hikari.ExceptionEvent) -> None:
    raise event.exception


@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.CommandNotFound):
        await event.context.respond("No such command")
        return
    if isinstance(event.exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            "There are some missing arguments: " + ", ".join(
                missing_option.name for missing_option in event.exception.missing_options)
        )
        return

    if isinstance(event.exception, lightbulb.ConverterFailure):
        await event.context.respond(
            f"The '{event.exception.option}' option is invalid"
        )
        return

    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"Command is on cooldown. Try later in {event.exception.retry_after:.0f} seconds"
        )
        return

    if isinstance(event.exception,
                  (lightbulb.NotOwner,lightbulb.ExtensionNotFound, lightbulb.ExtensionNotLoaded, lightbulb.ExtensionAlreadyLoaded)):
        await event.context.respond(
            f"'{event.exception}'"
        )
        return

    await event.context.respond("I have errors")

    raise event.exception


def run():
    if os.name != "nt":
        import uvloop

        uvloop.install()
    bot.run()
