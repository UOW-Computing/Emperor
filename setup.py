import os

from src.ServerUtils import Utils

emperor_version = "v0.1.44"


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


def check_loop(type: str, inp: str) -> str:
    if Utils.isEmpty(inp):
        print(f"{type} cannot be left empty!")
        return check_loop(type, input("Please enter a value: "))
    else:
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
Utils.outputBranding()
print(
    """As this is your first time setting up this repo, please either
make a .env file or follow the wizard below to create one."""
)

create_ENV_file = input("Create a new .env file?: [yes/no] ")

if check_input(create_ENV_file) == "yes":
    # Enter guild name and the log channel

    bot_token = check_loop("bot token", input("Enter BOT token: "))

    openai_token = check_loop("openai key", input("Enter you openai api key: "))

    guild_ids = []
    log_channel_ids = {}
    staff_ids = {}

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
                if Utils.validateIsDigit(guild_id):

                    log_channel_id = input("Enter LOG CHANNEL ID (0 for none): ")

                    try:
                        log_channel_ids[guild_id] = str(log_channel_id)
                    except:
                        print(
                            "You already have a log channel setup in this guild, cannot have two log channels."
                        )

                    staff_id = input(
                        "Please enter your staff role id (Cannot be left blank): "
                    )

                    if Utils.validateIsDigit(staff_id):
                        try:
                            staff_ids[guild_id] = str(staff_id)
                        except:
                            staff_ids[guild_id] = [staff_ids[guild_id], str(staff_id)]
                    guild_ids.append(guild_id)

                continue

    print("Leave prefix blank for default value of (e!)")
    prefix = input("Enter Desired prefix: ")
    if prefix == "":
        prefix = "e!"

    content_env = f"""# Dotenv file
# author: nukestye & UOW TEAM
# version: {emperor_version}

# -------------------------------------------------
# Do not change anything here
BOT_ENV_VERSION='{emperor_version}'
COGS = ["maincog", "admin", "mod", "api", "help"]	# this was from nuke
COLOUR = "4915330"									# this was from nuke
# -------------------------------------------------
#
# Ensure that all fields are given correct values.
# Also, the bot should have access to the guild and log channel
# otherwise an error will occur
TOKEN="{bot_token}"
OPENAI_KEY="{openai_token}"
BOT_PREFIX="{prefix}"
GUILD_ID="[{", ".join(guild for guild in guild_ids)}]"
LOG_CHANNEL_IDS='{{{write_to_file_dict(log_channel_ids)}}}'
STAFF_IDS='{{{write_to_file_dict(staff_ids)}}}'
"""
    # Creates the .env file with the contents parsed above
    Utils.writeToFile(filename="", content=content_env, mode="w", extension=".env")

    # Creates a logs folder, where Lj stores all the logs
    print("Creating logs folder for Lj....")
    try:
        # Create the folder
        os.makedirs("logs")
    except FileExistsError:
        # The folder already exists
        print("Testing purposes : File Already Exists")
        pass

    print(
        "\u001B[32m All configurations completed!\u001B[0m\nYou can now run main.py to launch the bot\n"
    )
