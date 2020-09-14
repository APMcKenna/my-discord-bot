from discord import Client
from os import getenv
from dotenv import load_dotenv

from discord_bot_utils import check_user_is_bot,\
    check_message_is_command,\
    get_valid_command,\
    user_has_required_privileges


# Load .env file variables into local machine environment variables
load_dotenv()
BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')
COMMAND_SYMBOL = getenv('BOT_COMMAND_SYMBOL')


bot = Client()


@bot.event
async def on_message(message):
    if check_message_is_command(message.content, COMMAND_SYMBOL) and check_user_is_bot(message.author):
        pass
    else:
        command = get_valid_command(message.content)

        if user_has_required_privileges(command["admin_required"], message.author):
            await command["method"](message)


bot.run(BOT_TOKEN)
