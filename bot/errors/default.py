class BotDefaultError(Exception):
    def __init__(self, comment):
        self.comment = comment
