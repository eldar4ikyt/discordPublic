import os

from dotenv import load_dotenv

load_dotenv()

import sentry_sdk
import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand, SlashContext

if bool(os.getenv("PRODUCTION")):
    sentry_sdk.init("http://3e86d04c5df345db83b5a2f675c03fcd@sentry.plazmix.space/5")

intents = discord.Intents.default()
intents.members = True

activity = discord.Streaming(name="mc.plazmix.net", url="https://twitch.tv/minecraft")

botInstance = Bot(command_prefix="/", intents=intents, activity=activity, help_command=None)

Slash = SlashCommand(botInstance, sync_commands=True, sync_on_cog_reload=True)

botInstance.load_extension("bot.cogs.error_handler")
botInstance.load_extension("bot.cogs.player")
botInstance.load_extension("bot.cogs.newssub")
botInstance.load_extension("bot.cogs.activity")


@Slash.slash(name='help', description="Помощь и информация бота.")
async def basic_help(ctx: SlashContext):
    await ctx.defer(hidden=True)

    await ctx.send(
        hidden=True,
        content="**Команды:**\n- `/player <ник> - информация об игроке.`\n"
                "\n- `/subscribe <канал> - подписка на новости` *`(нужны права админа)`*"
                "\n- `/un-subscribe - отписаться от новостей` *`(нужны права админа)`*"
                "\n"
                "\n**Пригласить бота - https://plzm.xyz/publicbot**"
                "\n**Дискорд сервер - https://plzm.xyz/ds-pub**"
                "\n**Дискорд сервер разработчиков - https://plzm.xyz/dev**"
    )
