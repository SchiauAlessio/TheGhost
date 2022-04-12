import hikari
import lightbulb
from lightbulb import commands
import asyncio
from time import time
plugin=lightbulb.Plugin("Advanced")

@plugin.command()
@lightbulb.command("aliased","Aliased command",aliases=["a"])
@lightbulb.implements(commands.PrefixCommand)
async def cmd_aliased(ctx) -> None:
    await ctx.respond(f"Command invoked with **{ctx.invoked_with}**")


@plugin.command()
@lightbulb.command("ephemeral","Sends ephemeral messages.",ephemeral=True)
@lightbulb.implements(commands.SlashCommand)
async def cmd_ephemeral(ctx) -> None:
    await ctx.respond("this can only be seen by you")


@plugin.command()
@lightbulb.command("defer","This command auto-defers!",auto_defer=True)
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_defer(ctx)-> None:
    await asyncio.sleep(5)
    await ctx.respond("Bot was asleep for 5 seconds",flags=hikari.MessageFlag.EPHEMERAL)


# @plugin.command()
# @lightbulb.command("dividebyzero","Division by 0",aliases=["div0","d0"])
# @lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
# async def cmd_zero(ctx)-> None:
#     await ctx.respond(f"1/0={1/0}")
#
# @cmd_zero.set_error_handler
# async def cmd_zero_error(event: lightbulb.CommandErrorEvent) -> bool:
#     exc= getattr(event.exception,"__cause__",event.exception)
#     if isinstance(exc,ZeroDivisionError):
#         await event.context.respond("Can't divide by zero")
#         return True
#     return False


@plugin.command()
@lightbulb.option("colour","Colour of choice",choices=("red","orange","yellow","blue","green","purple"))
@lightbulb.option("channel","Channel of choice",type=hikari.GuildChannel)
@lightbulb.option("member","Member of choice",type=hikari.Member)
@lightbulb.option("user","A user",type=hikari.User)
@lightbulb.command("opt","Options")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_opts(ctx)-> None:
    await ctx.respond(f"Colour: {ctx.options.colour}\n"
                      f"Channel: <#{ctx.options.channel.id}>\n"
                      f"Member: <@{ctx.options.member.id}>\n"
                      f"User: <@{ctx.options.user.id}>"
    )


@plugin.command()
@lightbulb.command("pingbot","See the bots latency",aliases=["ping"])
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_ping(ctx)-> None:
    start = time()
    await ctx.respond("pinging")
    end = time()
    await ctx.respond(
        f"**Gateway**: {ctx.bot.heartbeat_latency * 1000:,.0f} ms\n**REST**: {(end - start) * 1000:,.0f} ms",
    )

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)