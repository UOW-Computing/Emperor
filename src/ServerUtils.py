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
import sys
import json
import platform
import subprocess


class Utils:
    """
    Holds utility functions

    """

    @staticmethod
    def writeToFile(
        filename, content, mode="a", extension=".txt", directory=""
    ) -> None:
        # Writes the data into a text file
        # NOTE: when giving the filename, do not use .txt since the function already does that for you.

        """Writes the data to a given file name.
        Only needs filename and content to work.
        Optinal args provided, see Docs.

        Example:
            Utils.writeToFile(nameofmyfile, 'helloworld', mode='w')


        Args:
            filename (str): name of the file to be written to
            content (str): data to be written
            mode (str) : modes for opening a file, by default set to append.
            extention(str) : extension to save the file as, by default set to .txt

        Known Errors:
            When setting mode to r or x errors will occour. - Under Revision
        """
        with open(
            f"{directory}{filename}{extension}", mode, encoding="utf-8"
        ) as file:  # NOTE: reference ".txt".
            file.write(content + "\n")
            file.close()

    @staticmethod
    def read_from_json(path_to_file: str) -> dict:
        """Read json file and return it

        Args:
            path_to_file (str): The path to where the file is located

        Returns:
            dict: The json as dictionary
        """

        with open(os.path.realpath(path_to_file), "r") as json_file:
            data = json.loads(json_file.read())
        json_file.close()

        return data

    @staticmethod
    def print_branding():
        """
        Prints the Emperor console logo with version & copyright information
        """
        print("\n" * 100)
        print(
            """
         _____
        |   __|_____ ___ ___ ___ ___ ___
        |   __|     | . | -_|  _| . |  _|
        |_____|_|_|_|  _|___|_| |___|_|
            v0.1.45 |_| GPL-3.0-only 

        © 2022-2023 School of Computing Dev Team

        Welcome to Emperor!
        Discord bot made by students of University of Westminster.
        """
        )

    @staticmethod
    def validate_is_digit(value: str) -> bool:
        """Checks if the string parameter is a digit

        Args:
            value (str): The variable to look through

        Returns:
            bool: if digit, returns True else False
        """

        if value.isdigit():
            return True
        else:
            return False

    @staticmethod
    def is_empty(value: str) -> bool:
        """Determines if the value is empty or not

        Args:
            value (str): The value to check if its empty or not

        Returns:
            bool: True for empty, False for not empty
        """

        return value == ""

    @staticmethod
    def install_dependencies() -> bool:
        """Installs modules into the local system that are dependent by Emperor

        Args:
            module_name (str): The module to install

        Returns:
            bool: True: modules have been installed, False: modules weren't installed
        """

        # Open file to save
        with open("logs/setup.log", "w") as f:

            # Making sure this works on any os
            system = platform.system()
            if system == "Windows":
                command = ["where", "pip3"]
            else:
                command = ["which", "pip3"]

            print("Checking if pip is installed...")

            # Check if pip is installed
            if subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            ).returncode:
                raise "pip is not installed"

            print(
                "pip is installed\nRunning python -m pip install -r requirements.txt\n"
            )

            # Install packages from requirements.txt
            p = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                stdout=f,
                stderr=subprocess.STDOUT,
            )

            f.write("\n")

        f.close()

        # Check if the module was installed
        if p.returncode == 0:
            print("All dependencies of Emperor have been installed!")
            return True
        elif p.returncode == 1:
            print("error occurred, Check if the module name is correct!")
            return False

    # IGNORE #
    # Possible usage later, not implemented. Under revision.

    @staticmethod
    def get_user_input():  # Under revision
        pass
