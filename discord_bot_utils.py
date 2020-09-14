from timeout import timeout_bot


def author_is_admin(message_author):
    return message_author.guild_permissions.administrator


def user_has_required_privileges(admin_required, message_author):
    return not (admin_required and not message_author)


def check_user_is_bot(message_author):
    return message_author.bot


def get_valid_command(message):
    command = get_command_word_from_message(message)

    valid_commands = get_command_dict()

    return check_command_in_valid_commands(command, valid_commands)


def check_command_in_valid_commands(command, valid_commands):
    if command in valid_commands:
        return valid_commands[command]
    else:
        return None


def get_command_word_from_message(message):
    command_with_symbol = message.split(' ')[0]

    return remove_symbol_from_command(command_with_symbol)


def remove_symbol_from_command(command_with_symbol):
    return command_with_symbol[1:]


def check_message_is_command(message, command_symbol):
    return message.startswith(command_symbol)


def get_command_dict():
    return {
        "timeout":
            {
                "method": timeout_bot.run,
                "admin_required": True
            }
    }
