import discord
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')
command_symbol = os.getenv('BOT_COMMAND_SYMBOL')

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(command_symbol + 'timeout') and message.author.guild_permissions.administrator:
        await call_timeout(message)


async def call_timeout(message):
    message_string = message.content.split(' ')
    nick_name = message_string[1]
    timeout_length = int(message_string[2])

    user_obj = get_member(message.guild, nick_name)

    if user_obj is not None:
        await message.channel.send('User {0} has been muted for {1} seconds.'.format(nick_name, timeout_length))
        await timeout(user_obj, timeout_length)
    else:
        await message.channel.send('Could not find an individual user with that nickname/unique id. '
                                   'Please try again using the unique member ID.')


async def timeout(user_obj, timeout_length):
    await user_obj.edit(mute=True, deafen=True)
    await asyncio.sleep(timeout_length)
    await user_obj.edit(mute=False, deafen=False)


def get_member(guild, nick_name):
    members_list = guild.members
    matched_members = []

    for member in members_list:
        if nick_name == member.nick and member.nick is not None:
            matched_members.append(member)
        elif nick_name == member.name:
            matched_members.append(member)

    if len(matched_members) != 1:
        unique_id = nick_name
        member_obj = guild.get_member(unique_id)

        if member_obj is not None:
            return matched_members[0]
    else:
        return matched_members[0]


client.run(bot_token)
