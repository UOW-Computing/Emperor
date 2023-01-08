import os
from pathlib import Path
from src.ServerUtils import Utils
emperor_version = "v0.1.42"


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
# Prints Logo
Utils.outputBranding()

create_ENV_file = input("Create a new .env file?: [yes/no] ")
# NOTE: currently guild id and log channel id are being held as constant values
# Nuke I removed the multiple guild ID's and the json feature, we'll speak about this later.

if check_input(create_ENV_file) == "yes":
	# Enter guild name and the log channel

	bot_token = input("Enter BOT token: ")
	while True:
		guild_id = input("Enter GUILD ID (-1 to stop): ")
		match guild_id:
			case "-1":
				# If they want to stop break out of the
				# while loop
				break
			case _:
				if not guild_id.isdigit():
					print("Invalid GUILD ID, try again!")
					continue
				log_channel_id = input("Enter LOG CHANNEL ID (0 for none): ")
				break
	print("Leave prefix blank for default value of (/)")
	prefix = input("Enter Desired prefix: ")
	if prefix == "":
		prefix = "/"

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
BOT_PREFIX="{prefix}"
GUILD_ID=["{guild_id}"]
LOG_CHANNEL_ID="{log_channel_id}"
"""
	# Creates the .env file with the contents parsed above
	Utils.writeToFile(filename='', content=content_env, mode='w', extension='.env')	
	
	# Creates a logs folder, where Lj stores all the logs
	print("Creating logs folder for Lj....")
	try:
		# Create the folder
		os.makedirs('logs')
	except FileExistsError:
		# The folder already exists
		print("Testing purposes : File Already Exists")
		pass

 
	print("\u001B[32m All configurations completed!\u001B[0m\nYou can now run main.py to launch the bot\n")
