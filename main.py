import os
from bot.main import botInstance

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


if __name__ == '__main__':
    print('Launch')

    botInstance.run(DISCORD_TOKEN)
    

