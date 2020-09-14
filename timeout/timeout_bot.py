from argparse import ArgumentParser
from asyncio import sleep

from timeout.timeout_bot_utils import silence_and_deafen,\
    unsilence_and_undeafen,\
    get_member_by_discriminator_and_name,\
    get_member_by_name


async def run(command_message):
    await process_timeout_command(command_message)


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


async def timeout(member, timeout_length):
    """
    Silences and Deafens a user and then unsilences and undeafens once the specified time is up
    :param member: The server_member to be timed out
    :param timeout_length: The amount of time in seconds to time out the user for
    """
    await silence_and_deafen(member)
    await sleep(timeout_length)
    await unsilence_and_undeafen(member)


async def get_member(given_message, message_args):
    if message_args.discriminator:
        member = await get_member_by_discriminator_and_name(given_message.guild, given_message.channel,
                                                            message_args.username)
    else:
        member = await get_member_by_name(given_message.guild, given_message.channel, message_args.username)

    return member


async def give_user_response(message, member, nick_name, timeout_length):
    if member:
        await message.channel.send('User {0} has been muted for {1} seconds.'.format(nick_name, timeout_length))
        await timeout(member, timeout_length)
    else:
        await message.channel.send('Could not find an individual user with that nickname/unique id. '
                                   'Please try again using the unique member ID.')


def parse_arguments(given_message):
    message_parser = ArgumentParser()

    message_parser.add_argument("command")
    message_parser.add_argument("username")
    message_parser.add_argument("timeout_length", type=int)
    message_parser.add_argument('-d', '--discriminator', action="store_true")

    return message_parser.parse_args(given_message.split(' '))
