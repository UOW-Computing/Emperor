from pathlib import Path
from src.Utils import Utils
emperor_version = "v0.0.72"


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


print("\n" * 100)
print(
	"""
	 _____
	|   __|_____ ___ ___ ___ ___ ___
	|   __|     | . | -_|  _| . |  _|
	|_____|_|_|_|  _|___|_| |___|_|
		v0.0.72 |_|  © 2022 nukestye

Welcome to Emperor!
As this is your first time setting up the discord bot, please either
make a .env file or follow the wizard below to create one.
"""
)


create_ENV_file = input("Create a new .env file?: [yes/no] ")
# NOTE: currently guild id and log channel id are being held as constant values
# Nuke I removed the multiple guild ID's and the json feature, we'll speak about this later.

if check_input(create_ENV_file) == "yes":
	# Enter guild name and the log channel

	bot_token = input("Enter BOT token: ")
	print("Enter GUILD ID: ")
	while True:
		guild_id = input("GUILD ID (-1 to stop): ")
		match guild_id:
			case "-1":
				# If they want to stop break out of the
				# while loop
				break
			case _:
				if not guild_id.isdigit():
					print("Invalid GUILD ID, try again!")
					continue
				print("Enter LOG CHANNEL ID: ")
				log_channel_id = input("LOG CHANNEL ID (0 for none): ")

	prefix = input("Enter Desired prefix: ")
	print("Leave it blank for default value of (/) ")
	if prefix == "":
		prefix = "/"

	content_env = f"""# Dotenv file
# author: nukestye
# version: {emperor_version}

# Ensure that all fields are given correct values.
# Also, the bot should have access to the guild and log channel
# otherwise an error will occur
BOT_ENV_VERSION='{emperor_version}'
COGS = ["maincog", "admin", "mod", "api", "help"]	# this was from nuke
COLOUR = "4915330"									# this was from nuke

TOKEN='{bot_token}'
BOT_PREFIX='{prefix}'
GUILD_ID={guild_id}
LOG_CHANNEL_ID='{log_channel_id}'

"""
	Utils.writeToFile(filename='', content=content_env, mode='w', extension='.env')
	# with open(".envtest", "w", encoding="utf-8") as envfile:
	# 	envfile.write(env)
	# envfile.close()
	# print(".env has been created!\n")
	
	# Creates a logs folder, where Lj stores all the logs
	print("Creating logs folder for Lj....")
	Path('logs').mkdir(parents=True, exist_ok=True)
 
	print("\u001B[32m All configurations completed!\u001B[0m\nYou can now run main.py to launch the bot\n")
