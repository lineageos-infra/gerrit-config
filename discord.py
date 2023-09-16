import os

import requests

from lib import send_message, Config

if __name__ == "__main__":
    MESSAGE = os.environ.get("MESSAGE", "")
    if not MESSAGE:
        print("No webhook or message provided, set SLACK_WEBHOOK and SLACK_MESSAGE")
    else:
        send_message(Config.DISCORD_WEBHOOK, MESSAGE)
