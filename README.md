# my-discord-bot
# Command Structure (with $ as command symbol)
  - $timeout {user} {time(seconds)}
  - example:
    - $timeout example 5
 - The user arg can be the discord nickname or username
 - Ideally the user arg will be able to accept unique user ID however it does not at the moment
 
# Changing the bot command symbol and token
 - To set the bot command symbol and token you must create a file named ".env" in the same directory as the python file
 - There is a template for that file in this repository
 - Open the template file and copy in your bots token and change the command symbol as required

# Required bot permissions
 - Manage Roles
 - View Channels
 - Send Messages
 - Manage Messages
 - Mute Members
 - Deafen Members
