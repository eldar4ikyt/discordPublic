import discord
from discord.ext import commands
from discord.ext import tasks

from avocato.client.enum.online import OnlineCollection, OnlineModeSummary
from avocato.client.methods.online import ProjectOnline
import asyncio


class ActivityLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities = ['mc.plazmix.net', 'Игроков онлайн: {online}', 'Серверов с ботом: {servers}']
        self._current_element = -1

        self.activity_loop.start()

    @tasks.loop(seconds=19)
    async def activity_loop(self):
        await asyncio.sleep(1)
        self._current_element += 1
        if self._current_element > len(self.activities) - 1:
            self._current_element = 0

        current_status = self.activities[self._current_element].format(
            online=ProjectOnline().get(OnlineCollection.SUMMARY, OnlineModeSummary.TOTAL),
            servers=len(self.bot.guilds)
        )

        activity = discord.Streaming(name=current_status, url="https://twitch.tv/minecraft")

        await self.bot.change_presence(status=discord.Streaming, activity=activity)


def setup(bot):
    bot.add_cog(ActivityLoop(bot))
