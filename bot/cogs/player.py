import os

import discord
from PIL import ImageColor
from discord.ext import commands
from discord_slash import SlashContext, cog_ext, ComponentContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_components import create_actionrow
from discord_slash.utils.manage_components import create_select, create_select_option, create_button, ButtonStyle

from avocato.client import methods
from avocato.client.enum import game
from ..misc.badges import Basic
from ..misc.embedutils import EmbedUtils
from ..misc.statsimage import statsimage


class PlayerModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _skywars(self, player_nickname: str, message_author: discord.Member) -> discord.Embed:
        player = methods.PlazmixUser.get_from_nickname(nickname=player_nickname)
        sw = methods.GameUserSkyWars.get(user_nickname=player_nickname)

        swins = sw.get_from_game_type(game.SkyWarsGameType.INSANE)
        swdbl = sw.get_from_game_type(game.SkyWarsGameType.DOUBLES)
        # swrnk = sw.get_from_game_type(game.SkyWarsGameType.RANKED)

        hex_ = player.permission_group.html_color
        rgb_tup = ImageColor.getcolor(hex_, "RGB")
        clr = discord.Colour.from_rgb(r=rgb_tup[0], g=rgb_tup[1], b=rgb_tup[2])

        online_comment = f"{'🟢' if player.online.is_online else '🔴'} {player.online.comment}"

        embed = discord.Embed(
            colour=clr,
            description=online_comment
        )

        embed.add_field(name='⚔️ Solo Kills', value=swins.kills, inline=True)
        embed.add_field(name='🌯 Solo Wins', value=swins.wins, inline=True)
        EmbedUtils(embed).insert_empty_line()
        embed.add_field(name='⚔️ Doubles Kills', value=swdbl.kills, inline=True)
        embed.add_field(name='🌯 Doubles Wins', value=swdbl.wins, inline=True)
        EmbedUtils(embed).insert_empty_line()

        embed.set_author(name=f"{player.nickname}",
                         icon_url=player.image.variants.avatar.size_300,
                         url=f"https://profile.plazmix.net/u/{player.uuid}"
                         )

        embed.set_thumbnail(url="https://i.imgur.com/jN5od6Z.png")

        embed.set_footer(text=f"Запрошено: {message_author.name}#{message_author.discriminator}")

        return embed

    async def _player(self, player_nickname: str, message_author: discord.Member) -> discord.Embed:
        player = methods.PlazmixUser.get_from_nickname(nickname=player_nickname)
        hex_ = player.permission_group.html_color
        rgb_tup = ImageColor.getcolor(hex_, "RGB")
        clr = discord.Colour.from_rgb(r=rgb_tup[0], g=rgb_tup[1], b=rgb_tup[2])
        # other_groups = ""
        # other_groups_list = player.all_permission_group
        # other_groups_list.remove(player.permission_group)
        # for group in other_groups_list:
        #    other_groups += f'\n - {group.name}'

        online_comment = f"{'🟢' if player.online.is_online else '🔴'} {player.online.comment}"

        embed = discord.Embed(
            colour=clr,
            description=online_comment
        )

        dev_guild = self.bot.get_guild(int(os.getenv("DEV_GUILD")))

        embed.add_field(name='🏆 Уровень', value=player.level, inline=True)
        embed.add_field(name='🎭 Группа', value=player.permission_group.name, inline=True)
        EmbedUtils(embed).insert_empty_line()
        embed.add_field(name='👥 Друзья', value=player.friends_count, inline=True)
        EmbedUtils(embed).insert_empty_line()

        embed.set_author(name=f"{player.nickname}",
                         icon_url=player.image.variants.avatar.size_300,
                         url=f"https://profile.plazmix.net/u/{player.uuid}"
                         )

        image = await statsimage(dev_guild, log_channel_id=881221303665823764, color=hex_, player=player)
        embed.set_image(url=image)
        embed.set_thumbnail(url="https://i.imgur.com/jN5od6Z.png")

        embed.set_footer(text=f"Запрошено: {message_author.name}#{message_author.discriminator}")

        return embed

    async def _badge_buttons(self, player_nickname) -> list:
        player = methods.PlazmixUser.get_from_nickname(nickname=player_nickname)
        emojis = Basic().badge_emojis
        buttons = []
        for badge in player.badges:
            buttons.append(create_button(
                custom_id=f"{badge.technical_name}",
                emoji=self.bot.get_emoji(emojis.get(badge.technical_name)['id']),
                style=ButtonStyle.gray
            ))

        return buttons

    @cog_ext.cog_slash(name="player", description="Получить информацию об игроке.", options=[
        create_option(
            name="nickname",
            description="Никнейм игрока.",
            option_type=3,
            required=True
        )])
    async def _command_player(self, ctx: SlashContext, nickname: str = "TheGiga"):
        await ctx.defer()

        default_embed = await self._player(nickname, ctx.author)

        select = create_select(
            placeholder="Выберите метод...",
            custom_id="InfoSelect",
            max_values=1,
            options=[
                create_select_option(
                    label="Базовая статистика", emoji="📈", value="SelectBasic",
                    description="Возвращает статистику пользователя по его нику.",
                    default=True
                ),
                create_select_option(
                    label="SkyWars", emoji="🏹", value="SelectSkywars",
                    description="Возвращает статистику пользователя в SkyWars."
                )
            ]
        )

        comps = [create_actionrow(select)]

        buttons = await self._badge_buttons(player_nickname=nickname)

        if not len(buttons) == 0:
            comps.append(create_actionrow(*buttons))

        await ctx.send(embed=default_embed, components=comps)

    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        possible_badges_ids = ["legend", "partner_developer", "plus_sub", "top_worker", "verification", "worker",
                               "partner"]

        if ctx.custom_id in possible_badges_ids:
            player = methods.PlazmixUser.get_from_nickname(nickname=ctx.origin_message.embeds[0].author.name)
            badges = Basic().badge_emojis
            content = f"{badges.get(ctx.custom_id)['comment'].format(nickname=player.nickname)}"

            if ctx.custom_id == "partner_developer":
                content += "\n\nВы можете получить этот значок, подробности тут - <https://plzm.xyz/dev>"
            elif ctx.custom_id == "worker":
                content += "\n\nВы можете получить этот значок, подробности тут - <https://team.plazmix.net>"

            await ctx.defer(hidden=True)

            await ctx.send(hidden=True,
                           content=content
                           )
            return

        if not ctx.custom_id == "InfoSelect":
            return

        nickname = ctx.origin_message.embeds[0].author.name

        interacted = ctx.selected_options[0]

        useful = {
            "SelectBasic": {
                "function": self._player,
                "pressed": False
            },
            "SelectSkywars": {
                "function": self._skywars,
                "pressed": False
            }
        }

        func = useful.get(interacted)["function"]
        embed = await func(nickname, message_author=ctx.author)

        useful[interacted]["pressed"] = True

        select = create_select(
            placeholder="Выберите метод...",
            custom_id="InfoSelect",
            max_values=1,
            options=[
                create_select_option(
                    label="Базовая статистика", emoji="📈", value="SelectBasic",
                    description="Возвращает статистику пользователя по его нику.",
                    default=useful["SelectBasic"]["pressed"]
                ),
                create_select_option(
                    label="SkyWars", emoji="🏹", value="SelectSkywars",
                    description="Возвращает статистику пользователя в SkyWars.",
                    default=useful["SelectSkywars"]["pressed"]
                )
            ]
        )

        await ctx.defer(edit_origin=True)

        comps = [create_actionrow(select)]

        if useful["SelectBasic"]["pressed"] is True:
            buttons = await self._badge_buttons(player_nickname=nickname)

            if not len(buttons) == 0:
                comps.append(create_actionrow(*buttons))

        await ctx.origin_message.edit(embed=embed, components=comps)
        # await interaction.respond(type=6)


def setup(bot):
    bot.add_cog(PlayerModule(bot))
