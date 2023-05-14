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
# pylint: disable=invalid-name

from datetime import datetime
from src.ServerUtils import Utils


class Lj:
    """
    Loggerj
    v0.1

    Holds the Loggerj functions, from where INFO, WARN and ERROR can be
    made to file and console.
    """

    log_file = None

    def __init__(self):
        self.log_file = f'logs_log-{datetime.now().strftime("%Y %m %d-%H %M")}'

    def log(
        self, pathway: str = "emperor", content: str = "no content was given"
    ) -> bool:
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
        log_format = f"{time} \x1b[1;49;94mINFO\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m  {content}"

        # escape characters cant be in file, therefore cleaned here
        clean_info_format = f"{time} INFO  {pathway}  {content}"
        print(log_format)

        # Simple try and except where it saves to file
        try:
            # save to file
            Utils.write_to_file(
                self.log_file, clean_info_format, extension=".log", directory="logs/"
            )
            return True
        except FileNotFoundError:
            print(
                f"{time} \x1b[1;49;33mWARN\x1b[0m \x1b[1;49;95memperor.lj\x1b[0m File could not be found"
            )
            return False

    def warn(
        self, pathway: str = "emperor", content: str = "no content was given"
    ) -> bool:
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
        warn_format = f"{time} \x1b[1;49;33mWARN\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m  {content}"

        # escape characters cant be in file, therefore cleaned here
        clean_warn_format = f"{time} WARN  {pathway}  {content}"

        print(warn_format)

        # Simple try and except where it saves to file
        try:
            # save to file
            Utils.write_to_file(
                self.log_file, clean_warn_format, extension=".log", directory="logs/"
            )
            return True
        except FileNotFoundError:
            print(
                f"{time} \x1b[1;49;33mWARN\x1b[0m \x1b[1;49;95memperor.lj\x1b[0m File could not be found"
            )
            return True

    def error(
        self, pathway: str = "emperor", content: str = "no content was given"
    ) -> bool:
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
{time} \x1b[1;49;31mERROR\x1b[0m     \x1b[1;49;95m{pathway}\x1b[0m  {content}
{time} \x1b[1;49;31mERROR\x1b[0m\n
"""

        # escape characters cant be in file, therefore cleaned here
        clean_error_format = (
            f"{time} ERROR \n{time} ERROR  {pathway}:  {content}\n{time} ERROR "
        )

        print(error_format)

        # Simple try and except where it saves to file
        try:
            # save to file
            Utils.write_to_file(
                self.log_file, clean_error_format, extension=".log", directory="logs/"
            )
            return True
        except FileNotFoundError:
            print(
                f"{time} \x1b[1;49;33mWARN\x1b[0m  \x1b[1;49;95memperor.lj\x1b[0m File could not be found"
            )
            return False
