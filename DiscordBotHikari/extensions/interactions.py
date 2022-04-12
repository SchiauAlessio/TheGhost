import asyncio
from lightbulb.ext import neon
import hikari
import lightbulb

plugin=lightbulb.Plugin("Interactions")

LINK_MAPPING={
    "Youtube channel":"https://www.youtube.com/channel/UCN4sb1fxYajMo8u2sCCyHig",
    "Twitch Channel": "https://www.twitch.tv/sattlexp",
    "Discord Invite": "https://discord.gg/587dkAkYc7",
    "Steam": "https://steamcommunity.com/id/alexie974/",

}
@plugin.command()
@lightbulb.command("links","Links")
@lightbulb.implements(lightbulb.SlashCommand)
async def links_cmd(ctx:lightbulb.SlashContext) ->None:
    select_menu=(ctx.bot.rest.build_action_row()
                 .add_select_menu("links_select")
                 .set_placeholder("Choose a link"))

    for name,link in LINK_MAPPING.items():
        select_menu.add_option(name,link).add_to_menu()

    await ctx.respond("Select a link!",component=select_menu.add_to_container())
    while True:
        try:
            event = await ctx.bot.wait_for(hikari.InteractionCreateEvent,timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit_last_response("Timed out",component=None)
        else:
            await event.interaction.create_initial_response(hikari.ResponseType.MESSAGE_UPDATE,f"<{event.interaction.values[0]}>"
            )

@plugin.command()
@lightbulb.command("count","Button counts")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_count(ctx:lightbulb.SlashContext) ->None:
    button_menu = (
        ctx.bot.rest.build_action_row()
        .add_button(hikari.ButtonStyle.PRIMARY,"count_button")
        .set_label("+1")
        .add_to_container()
    )
    count=0
    await ctx.respond("Count: 0",component=button_menu)

    while True:
        try:
            event = await ctx.bot.wait_for(hikari.InteractionCreateEvent,timeout=60)
        except asyncio.TimeoutError:
            await ctx.edit_last_response("Timed out",component=None)
        else:
            count+=1
            await event.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_UPDATE,
                f"Count: {count}"
            )




def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)