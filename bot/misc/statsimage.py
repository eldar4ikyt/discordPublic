import datetime
import io
import os

import discord
import requests
from PIL import Image, ImageDraw, ImageFont

from bot.misc.badges import Badges

font = ImageFont.truetype("bot/misc/f.ttf", 30)
font_mini = ImageFont.truetype("bot/misc/f.ttf", 25)


async def statsimage(guild, log_channel_id, color, player):
    background = Image.open('bot/misc/player.png', 'r')

    skin_identifier = player.image.identifier
    if skin_identifier in ['alex', 'steve']:
        skin_identifier = "c06f89064c8a49119c29ea1dbd1aab82"

    try:
        im = Image.open(io.BytesIO(requests.get(f"https://crafatar.com/renders/body/{skin_identifier}?scale=10&overlay",
                                                timeout=5.0).content))
    except requests.exceptions.ReadTimeout:
        im = Image.open('bot/misc/default_player.png', 'r')
    background.paste(im, (25, 60), im)
    draw = ImageDraw.Draw(background)
    playerNickname = f"{player.permission_group.name} {player.nickname}"
    w, h = draw.textsize(playerNickname, font=font)
    draw.text(((559 - w) / 2, 34), playerNickname, font=font, fill=color)
    draw.text((260, 85), f"Статистика:", font=font, fill=f"#fff")
    draw.text((264, 123), f"Уровень: {player.level}", font=font, fill=f"#fff")

    if not len(player.badges) == 0:
        draw.text((260, 258), f"Значки: ", font=font, fill=f"#fff")
        now = 264
        for badge in player.badges:
            badges = Badges(badge)
            img = Image.open(badges.get_path())

            background.paste(img, (now, 291), img)
            now += 38

    # draw.text((279, 325), f"Кейсы: {self.LenCases()}", font=self.font, fill=f"#fff")
    dateComment = f"{player.online.comment}"
    w, h = draw.textsize(dateComment, font=font_mini)
    draw.text((5, 512), dateComment, font=font_mini, fill=f"#fff")

    # TODO: ПИЗДЕЦ БЛЯТЬ ПЕРЕПИСАТЬ, А ТО ГИГА ХУИТУ НАПИСАЛ, ВОТ ПАПОЧКУ ПРОВЕРЯТЬ НАДО, А ОН ЛОХ, КАКБЫ ДА
    # пиздец, да?

    name = f'{datetime.datetime.utcnow()}'
    name = name.replace(" ", "")
    name = name.replace(":", "-")
    directory = f'bot/misc/store/{name}.png'
    background.save(directory)
    ch = guild.get_channel(log_channel_id)
    msg = await ch.send(file=discord.File(f"{directory}", filename="image.png"))
    os.remove(directory)
    return msg.attachments[0].url
