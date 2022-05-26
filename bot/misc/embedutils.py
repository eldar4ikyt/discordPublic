class EmbedUtils:
    def __init__(self, embed):
        self.embed = embed

    def insert_empty_line(self, inline=True):
        return self.embed.add_field(name='⠀', value="⠀", inline=inline)
