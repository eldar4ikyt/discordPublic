from dotenv import load_dotenv

load_dotenv()

from bot.lib.plazmixclient.obj import PlazmixUser


user = PlazmixUser.get(nickname="Krashe85")
for user in user.friends:
    print(user)