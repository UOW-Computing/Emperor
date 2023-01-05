import time

from datetime import datetime

class Lj:
	"""
	Loggerj
	v0.1
	
	Holds the Loggerj functions, from where INFO, WARN and ERROR can be
	made to file and console.
	"""
	
	log_file = None
	
	def __init__(self):
		self.log_file = 'logs/log-'+datetime.now().strftime("%Y %m %d-%H %M")
		
	
	def info(self, pathway: str = 'emperor', content: str = 'no content was given') -> bool:
		"""	
		Makes an INFO entry to log file and prints the log to console

		Args:
			pathway (str, optional): the place where the log was called. Defaults to 'emperor'.
			content (str, optional): the content to log. Defaults to 'no content was given'.

		Returns:
			bool: debug to find if the content was written to log file
		"""
		# format: Year-month-day hour:minute:seconds	INFO	path way	content
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		log_format = f'{time} \x1b[1;49;94mINFO\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m:\t {content}'

		# escape characters cant be in file, therefore cleaned here
		clean_info_format = f'{time} INFO \t {pathway}:\t {content}'
		print(log_format)

		# Simple try and except where it saves to file
		try:
			# save to file
			with open(self.log_file, "a", encoding="utf-8") as file:
				file.write(clean_info_format + "\n")
			file.close()
			return True
		except FileNotFoundError:
			print(f'{time} \x1b[1;49;33mWARN\x1b[0m \x1b[1;49;95memperor.lj[0m: File could not be found')
			return False
   
	def warn(self, pathway: str = 'emperor', content: str = 'no content was given') -> bool:
		"""
		Makes an WARN entry to log file and prints the warn to console

		Args:
			pathway (str, optional): the place where the log was called. Defaults to 'emperor'.
			content (str, optional): the content to log. Defaults to 'no content was given'.

		Returns:
			bool: debug to find if the content was written to log file
		"""
  
		# format: Year-month-day hour:minute:seconds	WARN	path way	content
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		warn_format =	f'{time} \x1b[1;49;33mWARN\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m:\t {content}'
  
  		# escape characters cant be in file, therefore cleaned here
		clean_warn_format = f'{time} WARN \t {pathway}:\t {content}'
  
		print(warn_format)

		# Simple try and except where it saves to file
		try:
			# save to file
			with open(self.log_file, "a", encoding="utf-8") as file:
				file.write(clean_warn_format + "\n")
			file.close()
			return True
		except FileNotFoundError:
				print(f'{time} \x1b[1;49;33mWARN\x1b[0m \x1b[1;49;95memperor.lj[0m: File could not be found')
				return True
	
	
	def error(self, pathway: str = 'emperor', content: str = 'no content was given') -> bool:
		"""
  		Makes an ERROR entry to log file and prints the error to console

		Args:
			pathway (str, optional): the place where the log was called. Defaults to 'emperor'.
			content (str, optional): the content to log. Defaults to 'no content was given'.

		Returns:
			bool: debug to find if the content was written to log file
		"""
		
		# format: Year-month-day hour:minute:seconds	ERROR	path way	content
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		error_format = f"""
{time} \x1b[1;49;31mERROR\x1b[0m
{time} \x1b[1;49;31mERROR\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m:\t {content}
{time} \x1b[1;49;31mERROR\x1b[0m\n
"""

		# escape characters cant be in file, therefore cleaned here
		clean_error_format = f'{time} ERROR \n{time} ERROR \t {pathway}:\t {content}\n{time} ERROR '
  
		print(error_format)

		# Simple try and except where it saves to file
		try:
			# save to file
			with open(self.log_file, "a", encoding="utf-8") as file:
				file.write(clean_error_format + "\n")
			file.close()
			return True
		except FileNotFoundError:
				print(f'{time} \x1b[1;49;33mWARN\x1b[0m \t \x1b[1;49;95memperor.lj[0m: File could not be found')
				return False