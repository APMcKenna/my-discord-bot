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
    return name_with_discriminator_too_short(name_string) and name_contains_hash_before_discriminator(name_string) \
        and discriminator_contains_four_integers(name_string)


def discriminator_contains_four_integers(name_string):
    discriminator = list(name_string)[-4:]
    for character in discriminator:
        if not character.isdigit():
            return False

    return True


def name_contains_hash_before_discriminator(name_string):
    return list(name_string)[-5] == '#'


def name_with_discriminator_too_short(name_string):
    return len(name_string) < 6


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


async def silence_and_deafen(member):
    await member.edit(mute=True, deafen=True)


async def unsilence_and_undeafen(member):
    await member.edit(mute=False, deafen=False)
