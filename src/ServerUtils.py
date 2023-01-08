class Utils:
    @staticmethod
    def writeToFile(filename, content, mode='a',extension='.txt', directory='') -> None: # Writes the data into a text file
    #NOTE: when giving the filename, do not use .txt since the function already does that for you.

        """ Writes the data to a given file name.
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
        with open(f"{directory}{filename}{extension}", mode, encoding="utf-8") as file: #NOTE: reference ".txt".
            file.write(content + "\n")
            file.close()
        

    @staticmethod
    def outputBranding(): 
        # Moved this into a function in order to declutter setup.py
        """
        Outputs Emperor Branding.
        """
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







    # IGNORE #
    # Possible usage later, not implemented. Under revision.    
    @staticmethod
    def validateIsDigit(value:str):
        if value.isdigit():
            return True
        else:
            return False
    @staticmethod
    def getUserInput():  # Under revision
        pass