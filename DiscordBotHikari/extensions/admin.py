import os

import hikari
import lightbulb
from lightbulb import commands
plugin=lightbulb.Plugin("Admin")


@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown","shut dow the bot")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond("Bot shut down")
    await ctx.bot.close()

#todo allow more complex queries
@plugin.command()
@lightbulb.add_checks(lightbulb.has_roles(int(os.getenv('MODERATOR_ROLE_ID')))) #if any of these roles are missing an error will be raised
@lightbulb.option("statement","The python statement you wish to evaluate",modifier=commands.OptionModifier.CONSUME_REST)
@lightbulb.command("eval","evaluate a statement")
@lightbulb.implements(commands.PrefixCommand,commands.SlashCommand)
async def cmd_exec(ctx: lightbulb.Context) -> None:
    result=eval(ctx.options.statement)
    await ctx.respond(f"```py\n>>> {ctx.options.statement}\n{result}```")


@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("extension","Load,unload and reload extension")
@lightbulb.implements(commands.PrefixCommandGroup,commands.SlashCommandGroup)
async def cmd_extension(ctx) -> None:
    ...

@cmd_extension.child()
@lightbulb.option("name","Name of extension to load")
@lightbulb.command("load","Load extension")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_extension_load(ctx: lightbulb.context.Context) -> None:
    ctx.bot.load_extensions(ctx.options.name.lower())
    await ctx.respond("Done")

@cmd_extension.child()
@lightbulb.option("name","Name of extension to unload")
@lightbulb.command("unload","Unload extension")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_extension_unload(ctx: lightbulb.context.Context) -> None:
    if ctx.options.name.lower() == "admin":
        await ctx.respond("You cannot unload the admin extension")
    current_plugin = ctx.bot.get_plugin(ctx.options.name.lower())
    ctx.bot.remove_plugin(current_plugin)
    await ctx.respond("Done")


@cmd_extension.child()
@lightbulb.option("name","Name of extension to reload")
@lightbulb.command("reload","Reload extension")
@lightbulb.implements(commands.PrefixSubCommand,commands.SlashSubCommand)
async def cmd_extension_reload(ctx) -> None:
    ctx.bot.reload_extensions(ctx.options.name.title())
    await ctx.respond("Done")


def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)