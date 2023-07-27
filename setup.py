"""
Emperor, discord bot for school of computing
Copyright (C) 2022-2023  School of Computing Dev Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
from getpass import getpass
from src.ServerUtils import Utils

EMPEROR_VERSION = "v1.0.0"


def check_input(var_input: str) -> str:
    """
    Checks whether the user input is correct

    Params:
        var_input: the user input

    Returns:
        Correct user input
    """
    if var_input.lower() in ["y", "yes", "ye"]:
        return "yes"

    if var_input.lower() in ["n", "no"]:
        return "no"

    return check_input(
        var_input=input(
            """Incorrect input
Would you like to create an env file?: [yes/no]
"""
        )
    )


def check_loop(field: str, inp: str) -> str:
    """Loops untill the condition the input is not empty

    Args:
        field (str): variable that cannot be left empty
        inp (str): The input given by the user

    Returns:
        str: The non-empty value
    """
    # Check if the input given is empty
    if Utils.is_empty(inp):
        # Its empty, ask again
        print(f"{field} cannot be left empty!")
        return check_loop(field, getpass("Please enter a value: "))

    return inp


def write_to_file_dict(content: dict) -> str:
    """
    Makes a string that holds the correct way to store the dict in .env

    Args:
        content (dict): The content to convert into str

    Returns:
        str: The converted string
    """
    return ", ".join(f'"{key}":"{value}"' for key, value in content.items())


# Prints Logo
Utils.print_branding()
print(
    """As this is your first time setting up this repo, please either
make a .env file manually or follow the wizard below to create one."""
)

create_ENV_file = input("Create a new .env file?: [yes/no] ")

if check_input(create_ENV_file) == "yes":
    # Enter guild name and the log channel

    bot_token = check_loop("Bot Token", getpass("Enter BOT token: "))

    openai_key = check_loop("OpenAI key", getpass("Enter you openai api key: "))
    
    print("This field can be left empty, however any API commands that use this token will not work.")
    
    github_key = input("Enter your GitHub token: ")

    guild_ids = []
    log_channel_ids = {}
    staff_ids = {}

    print(
        "INFO: You must have at least 1 GUILD ID and STAFF ROLE for the bot to work, LOG CHANNEL ID can be set to 0"
    )

    while True:
        try:
            guild_id = input("Enter GUILD ID (-1 to stop): ")
        except:
            print("Please only enter valid integer values")
            guild_id = input("Enter GUILD ID (-1 to stop): ")

        match guild_id:
            case "-1":
                # If they want to stop break out of the
                # while loop
                break
            case _:
                if Utils.validate_is_digit(guild_id):

                    log_channel_id = input("Enter LOG CHANNEL ID (0 for none): ")

                    try:
                        log_channel_ids[guild_id] = str(log_channel_id)
                    except Exception:
                        print(
                            "You already have a log channel setup in this guild, cannot have two log channels."
                        )

                    staff_id = input(
                        "Please enter your staff role id (Cannot be left blank): "
                    )

                    if Utils.validate_is_digit(staff_id):
                        try:
                            staff_ids[guild_id] = str(staff_id)
                        except Exception:
                            staff_ids[guild_id] = [staff_ids[guild_id], str(staff_id)]
                    guild_ids.append(guild_id)

                continue

    print("Leave prefix blank for default value of (e!)")
    PREFIX = input("Enter Desired prefix: ")
    if PREFIX == "":
        PREFIX = "e!"

    content_env = f"""# Dotenv file
# author: nukestye & UOW TEAM
# version: {EMPEROR_VERSION}

# -------------------------------------------------
# Do not change anything here
BOT_ENV_VERSION='{EMPEROR_VERSION}'
COGS = COGS = ["api", "core", "emp", "mod", "event", "dev", "help"]
COLOUR = "4915330"	
# -------------------------------------------------

# Ensure that all fields are given correct values.
# Also, the bot should have access to the guild and log channel
# otherwise an error will occur
TOKEN="{bot_token}"
OPENAI_KEY="{openai_key}"
GITHUB_KEY="{github_key}"
BOT_PREFIX="{PREFIX}"
GUILD_ID="[{", ".join(guild for guild in guild_ids)}]"
LOG_CHANNEL_IDS='{{{write_to_file_dict(log_channel_ids)}}}'
STAFF_IDS='{{{write_to_file_dict(staff_ids)}}}'
"""
    # Creates the .env file with the contents parsed above
    Utils.write_to_file(filename="", content=content_env, mode="w", extension=".env")

# Creates a logs folder, where Lj stores all the logs
print("Creating logs folder for Lj....")
try:
    # Create the folder
    os.makedirs("logs")
except FileExistsError:
    # The folder already exists
    print("Testing purposes : File Already Exists")

# Installing the dependencies
Utils.install_dependencies()

print(
    '\n\n\u001B[32mAll configurations completed!\u001B[0m\nYou can now do "python main.py" to launch the bot\n'
)
