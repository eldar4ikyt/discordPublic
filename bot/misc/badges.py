# -*- coding: utf-8 -*-

class Basic:
    def __init__(self):
        self.badge_emojis = {
            "legend": {
                "emoji": "<:badge_legend:894341056496300122>",
                "id": 894341056496300122,
                "name": "legend",
                "comment": "**{nickname}** является легендарным и почётным игроком проекта."
            },
            "partner": {
                "emoji": "<:badge_partner:894341079611097088>",
                "id": 894341079611097088,
                "name": "legend",
                "comment": "**{nickname}** является легендарным и почётным игроком проекта."
            },
            "partner_developer": {
                "emoji": "<:badge_partner_developer:894341091975901214>",
                "id": 894341091975901214,
                "name": "partner_developer",
                "comment": "**{nickname}** является разработчиком партнёрского приложения."
            },
            "plus_sub": {
                "emoji": "<:badge_plus_sub:894341103040467004>",
                "id": 894341103040467004,
                "name": "plus_sub",
                "comment": "**{nickname}** самый крутой игрок с подпиской плюс."
            },
            "top_worker": {
                "emoji": "<:badge_top_worker:892021127730315394>",
                "id": 892021127730315394,
                "name": "top_worker",
                "comment": "**{nickname}** почетный участник команды Plazmix."
            },
            "verification": {
                "emoji": "<:badge_verification:894341121319260251>",
                "id": 894341121319260251,
                "name": "verification",
                "comment": "Профиль пользователя **{nickname}** подтверждён администрацией проекта."
            },
            "worker": {
                "emoji": "<:badge_worker:892021160030646282>",
                "id": 892021160030646282,
                "name": "worker",
                "comment": "**{nickname}** является частью команды Plazmix."
            }
        }


class Badges:
    def __init__(self, badge_name):
        self._badge_name = badge_name

    def get_path(self):
        return f"bot/misc/badge_icons/{self._badge_name.technical_name}.png"
