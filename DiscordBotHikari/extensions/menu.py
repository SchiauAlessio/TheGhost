import hikari
import lightbulb
from lightbulb.ext import neon

plugin = lightbulb.Plugin("Menu")


class Menu(neon.ComponentMenu):
    @neon.button("Red", "red_button", hikari.ButtonStyle.DANGER)
    @neon.button("Green", "green_button", hikari.ButtonStyle.SUCCESS)
    @neon.button("Blue", "blue_button", hikari.ButtonStyle.PRIMARY)
    @neon.button("Grey", "grey_button", hikari.ButtonStyle.SECONDARY)
    @neon.button_group()
    async def select_color(self,button:neon.Button)->None:
        await self.edit_msg(f"Favorite color: {button.label}")


@plugin.command()
@lightbulb.command("colours", "Select favourite colour")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_colours(ctx: lightbulb.SlashContext) -> None:
    menu=Menu(ctx,timeout=60)
    message=await ctx.respond("Select your favorite color!", component=menu.build())
    await menu.run(message)

def load(bot) -> None:
    bot.add_plugin(plugin)

def unload(bot) -> None:
    bot.remove_plugin(plugin)