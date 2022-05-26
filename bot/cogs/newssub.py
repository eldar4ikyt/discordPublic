from discord_slash import SlashCommand, SlashContext, cog_ext
import discord
from discord.ext import commands

from discord_slash.utils.manage_commands import create_choice, create_option
from avocato.client import methods

import sqlite3


class NewsSubModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.newsloop.start()

    def _create_connection(self):
        self.connection = sqlite3.connect("bot/NewsSubscribers.db", timeout=15)
        self.c = self.connection.cursor()

    @cog_ext.cog_slash(name="subscribe", description="Подписаться на новости Plazmix Network.", options=[
        create_option(
            name="channel",
            description="Канал отправления новостей.",
            option_type=7,
            required=True
        )])
    async def subscribe(self, ctx, channel):
        print('test')
        await ctx.defer()
        if not ctx.author.guild_permissions.administrator:
            return
        guild_id = ctx.guild.id
        self._create_connection()
        self.c.execute("SELECT * FROM subscribers WHERE id=?", (guild_id,))
        result = self.c.fetchone()
        if result is not None:
            return await ctx.send(content=f"**Вы уже подписаны на новости PLAZMIX NETWORK!**\nКанал подписки: <#{result[1]}>")

        self.c.execute("INSERT INTO subscribers VALUES (?, ?)", (guild_id, channel.id,))
        self.connection.commit()

        self.connection.close()
        await ctx.send(content="**Вы успешно подписались на новости PLAZMIX NETWORK**!\n"
                               "Что-бы отписаться используйте: `/un-subscribe`\n"
                               "*В данный момент сообщения из новостей не приходят, но скоро все будет!*")

    @cog_ext.cog_slash(name="un-subscribe", description="Отписаться от новостей Plazmix Network.")
    async def un_subscribe(self, ctx):
        await ctx.defer()
        if not ctx.author.guild_permissions.administrator:
            return

        guild_id = ctx.guild.id
        self._create_connection()
        self.c.execute("SELECT * FROM subscribers WHERE id=?", (guild_id,))
        result = self.c.fetchone()
        if result is None:
            return await ctx.send(content=f"**Вы еще не подписаны на новости PLAZMIX NETWORK**.\n"
                                          "Для подписки используйте: `/subscribe <канал>`")

        self.c.execute("DELETE FROM subscribers WHERE id=?", (guild_id,))
        self.connection.commit()
        self.connection.close()
        await ctx.send(content="**Вы успешно отказались от получения новостей PLAZMIX NETWORK**...\n"
                               "Что-бы подписаться снова используйте: `/subscribe <канал>`")

    async def _paginate_and_send(self, information):
        self._create_connection()
        self.c.execute('SELECT COUNT(*) from subscribers')
        num = self.c.fetchone()[0]

        limit = 100
        current_offset = 0

        times = round(num / 100)

        for i in range(0, times + 1):
            print("started")
            print("current offset " + str(current_offset))
            self.c.execute("SELECT * FROM subscribers LIMIT ? OFFSET ?", (limit, current_offset))
            result = self.c.fetchall()

            for guild in result:
                print("found guilds" + str(guild))
                channel = await self.bot.fetch_channel(guild[1])
                await channel.send("test")

            current_offset += 100

        self.connection.close()

    # @tasks.loop(minutes=10)
    # async def newsloop(self):
    #     await self._paginate_and_send(information="none")
    #     information = methods.PlazmixNews.last()
    #     print(information)


def setup(bot):
    bot.add_cog(NewsSubModule(bot))
