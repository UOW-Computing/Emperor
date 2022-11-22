import time
from util import TerminalColours
import discord
# -------------------------------------------------
logChannelID = '1043986118258987008'
# -------------------------------------------------


class LJ:


	def __init__(self) -> None:
		if logChannelID is None:
			self.WARN("logger/init", "Channel ID is undefined!")

	@staticmethod
	def WARN(context: str = "main", message: str = "Unknown error occured! Ensure all procedures are working correctly") -> None:
		# Print ot console
		format = f'[{time.ctime(time.time())}] [{context}] \x1b[2;30;41m[WARNING] {message}\x1b[0m'
		print(format)
		
		# Save to file
		with open("logs", 'a') as logFile:
			logFile.write(format+ "\n")
		logFile.close()	

	
	@staticmethod
	def LOG(context: str = "main", message: str = "No context provided") -> None:
		# print to console
		format = f'[{time.ctime(time.time())}] [{context}]: {message}'
		print(format)
		
		# save to file
		with open("logs", 'a') as logFile:
			logFile.write(format+ "\n")
		logFile.close()

	
	# def LOGinChannel(guild: discord.guild, message: str) -> None:
	# 	# send a log in log channel
	# 	if logChannelID is not None:
	# 		e = discord.Embed(title="LJ", description=f"{message}")
	# 		print(logChannelID)
	# 		channel = guild.get_channel(logChannelID)
	# 		print(channel)
	# 		#channel.send(embed=e)


	def ljERROR():
		pass