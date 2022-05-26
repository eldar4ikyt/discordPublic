import discord
from discord.ext import commands
from discord_slash.utils.manage_components import create_actionrow
from discord_slash.utils.manage_components import create_button, ButtonStyle
from sentry_sdk import capture_exception

from avocato.client.error import PlazmixApiError


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, ex):
        help_button = create_actionrow(
            create_button(label="Обратиться в поддержку", style=ButtonStyle.URL, url="https://vk.me/plazmixdev")
        )
        if isinstance(ex, PlazmixApiError):
            await ctx.send(
                embed=discord.Embed(title=":x: Ошибка API", description=ex.comment,
                                    colour=discord.Colour.red()),
                content="",
                components=[help_button])
            return

        capture_exception(ex)
        await ctx.send(
            embed=discord.Embed(title=":x: Внутренняя ошибка бота", description=ex,
                                colour=discord.Colour.red()),
            content="",
            components=[help_button])


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
