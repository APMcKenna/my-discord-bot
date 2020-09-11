from discord import Client
from asyncio import sleep
from argparse import ArgumentParser
from os import getenv
from dotenv import load_dotenv

# Load .env file variables into local machine environment variables
load_dotenv()
BOT_TOKEN = getenv('DISCORD_BOT_TOKEN')
COMMAND_SYMBOL = getenv('BOT_COMMAND_SYMBOL')


# Creating the bot
bot = Client()


@bot.event
async def on_message(message):
    """
    Function gets called each time a message is sent in any of the servers text channels
    :param message: The message that triggered the event
    :return: Returns if message was sent by the bot
    """
    if check_user_is_bot(message.author):
        return

    if author_is_admin(message.author) and message_is_timeout_command(message.content):
        await process_timeout_command(message)


def author_is_admin(message_author):
    return message_author.guild_permissions.administrator


def message_is_timeout_command(message_content):
    return message_content.startswith(COMMAND_SYMBOL + "timeout")


def check_user_is_bot(message_author):
    return message_author == bot.user


async def process_timeout_command(given_message):
    member, timeout_length = await process_input(given_message)

    if member is None:
        return
    else:
        await timeout(member, timeout_length)


async def process_input(given_message):
    message_args = parse_arguments(given_message.content)

    member = await get_member(given_message, message_args)
    return member, message_args.timeout_length


def parse_arguments(given_message):
    message_parser = ArgumentParser()

    message_parser.add_argument("command")
    message_parser.add_argument("username")
    message_parser.add_argument("timeout_length", type=int)
    message_parser.add_argument('-d', '--discriminator', action="store_true")

    return message_parser.parse_args(given_message.split(' '))


async def get_member(given_message, message_args):
    if message_args.discriminator:
        member = await get_member_by_discriminator_and_name(given_message.guild, given_message.channel,
                                                            message_args.username)
    else:
        member = await get_member_by_name(given_message.guild, given_message.channel, message_args.username)

    return member


async def get_member_by_discriminator_and_name(guild, channel, name_string):
    matched_members = get_member_list_by_discriminator_and_name(guild, name_string)

    if len(matched_members) == 0:
        await channel.send("Could not find an individual user with that name and discriminator. Please double-check "
                           "the name you have given and try again.")
        return None
    elif len(matched_members) == 1:
        return matched_members[0]
    else:
        await channel.send("Found multiple users with that name and discriminator. This should not be possible due to "
                           "name and discriminator being unique. Check that you are using the username and not the "
                           "nickname.")
        return None


def get_member_list_by_discriminator_and_name(guild, name_string):
    given_name, given_discriminator = split_name_and_discriminator(name_string)

    members_list = guild.members
    matched_members_list = []

    for member in members_list:
        if check_discriminator_and_name(given_discriminator, given_name, member):
            matched_members_list.append(member)

    return matched_members_list


def check_discriminator_and_name(given_discriminator, given_name, member):
    return check_member_name(given_name, member) and check_discriminator(given_discriminator, member)


def check_discriminator(given_discriminator, member):
    return given_discriminator == member.discriminator


def split_name_and_discriminator(name_string):
    name = ''.join(list(name_string)[:-5])
    discriminator = ''.join(list(name_string)[-4:])

    return name, discriminator


def check_name_contains_discriminator(name_string):
    """
    Checks that the given "name_string" contains a possible discriminator

    :param name_string: given username that is flagged to contain a discriminator
    :return: True or False
    """
    return name_too_short(name_string) and name_contains_hash_before_discriminator(name_string) \
           and discriminator_contains_four_integers(name_string)


def discriminator_contains_four_integers(name_string):
    discriminator = list(name_string)[-4:]
    for character in discriminator:
        if not character.isdigit():
            return False

    return True


def name_contains_hash_before_discriminator(name_string):
    return list(name_string)[-5] == '#'


def name_too_short(name_string):
    return len(name_string) < 6


async def get_member_by_name(guild, channel, username):
    matched_members = get_member_list_by_name(guild, username)

    if len(matched_members) == 0:
        await channel.send("Could not find an individual user with that name. Please try again using -d and attaching "
                           "the user discriminator, e.g. username#6666")
        return None
    elif len(matched_members) == 1:
        return matched_members[0]
    else:
        await channel.send("Found multiple users with that name. Please try again using -d and attaching the user "
                           "discriminator, e.g username#6666")
        return None


def get_member_list_by_name(guild, username):
    members_list = guild.members
    matched_members_list = []

    for member in members_list:
        if check_matching_member_name(username, member):
            matched_members_list.append(member)

    return matched_members_list


def check_matching_member_name(username, member):
    if check_display_name(username, member):
        return True
    elif check_member_name(username, member):
        return True
    else:
        return False


def check_display_name(username, member):
    return username == member.display_name


def check_member_name(username, member):
    return username == member.name


async def give_user_response(message, member, nick_name, timeout_length):
    if member:
        await message.channel.send('User {0} has been muted for {1} seconds.'.format(nick_name, timeout_length))
        await timeout(member, timeout_length)
    else:
        await message.channel.send('Could not find an individual user with that nickname/unique id. '
                                   'Please try again using the unique member ID.')


async def timeout(member, timeout_length):
    """
    Silences and Deafens a user and then unsilences and undeafens once the specified time is up
    :param member: The server_member to be timed out
    :param timeout_length: The amount of time in seconds to time out the user for
    """
    await silence_and_deafen(member)
    await sleep(timeout_length)
    await unsilence_and_undeafen(member)


async def silence_and_deafen(member):
    await member.edit(mute=True, deafen=True)


async def unsilence_and_undeafen(member):
    await member.edit(mute=False, deafen=False)


# Initializes the bot on the server
bot.run(BOT_TOKEN)
