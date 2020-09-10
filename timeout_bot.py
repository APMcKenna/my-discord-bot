import discord
import asyncio
import os
from dotenv import load_dotenv

# Load .env file variables into local machine environment variables
# load_dotenv()
# BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
# COMMAND_SYMBOL = os.getenv('BOT_COMMAND_SYMBOL')

BOT_TOKEN = "Njc4MzA1MTYzMjMyMTQ5NTI2.Xkg26Q.oet0V25HtdPXRGKmEOiBVSUxC7Y"
COMMAND_SYMBOL = "$"


# Creating the bot object
bot = discord.Client()


@bot.event
async def on_message(message):
    """
    Function gets called each time a message is sent in any of the servers text channels
    :param message: The message that triggered the event
    :return: Returns if message was sent by the bot
    """
    if message.author == bot.user:
        return

    # Checks that the timeout command was called by an admin
    if message.author.guild_permissions.administrator and message.content.startswith(COMMAND_SYMBOL + 'timeout'):
        await call_timeout(message)


async def call_timeout(message):
    """
    Splits the message contents into a list of [command][nickname][timeout length]
    :param message: The message that triggered the event
    """
    message_string = message.content.split(' ')
    nick_name = message_string[1]
    timeout_length = int(message_string[2])

    user_obj = get_member(message.guild, nick_name)

    await give_user_response(message, user_obj, nick_name, timeout_length)


async def give_user_response(message, user_obj, nick_name, timeout_length):
    if user_obj:
        await message.channel.send('User {0} has been muted for {1} seconds.'.format(nick_name, timeout_length))
        await timeout(user_obj, timeout_length)
    else:
        await message.channel.send('Could not find an individual user with that nickname/unique id. '
                                   'Please try again using the unique member ID.')


async def timeout(user_obj, timeout_length):
    """
    Silences and Deafens a user and then unsilences and undeafens once the specified time is up
    :param user_obj: The server_member to be timed out
    :param timeout_length: The amount of time in seconds to time out the user for
    """
    await silence_and_deafen(user_obj)
    await asyncio.sleep(timeout_length)
    await unsilence_and_undeafen(user_obj)


async def silence_and_deafen(user):
    await user.edit(mute=True, deafen=True)


async def unsilence_and_undeafen(user):
    await user.edit(mute=False, deafen=False)


def get_member(guild, given_name):
    """
    Searches the server for a member by nick_name or username
    :param guild: the server that the bot is connected to
    :param given_name: The nickname or username of the user to be timed out
    :return: The individual member that matches the specified nick_name or username
    """
    members_list = guild.members
    matched_members = []

    for member in members_list:
        if member.nick is not None and given_name == member.nick:
            matched_members.append(member)
        elif given_name == member.name:
            matched_members.append(member)

    if len(matched_members) != 1:
        given_unique_id = int(given_name)
        member_obj = guild.get_member(given_unique_id)

        if member_obj is not None:
            return matched_members[0]
    else:
        return matched_members[0]


# Initializes the bot on the server
bot.run(BOT_TOKEN)
