# my-discord-bot
# Command Structure (with $ as command symbol)
  - $timeout {user} {time(seconds)}
  - example:
    - $timeout example 5
  - $timeout {user} {time(seconds)} {-d, --discriminator}
  
 - The user arg can be the discord nickname or username
 - The -d/--discriminator will be included if you wish to have the username and unique discriminator included
 - e.g. "User1234#5665"
 
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
