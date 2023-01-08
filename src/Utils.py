class Utils:
    @staticmethod
    def writeToFile(filename, content, mode='a',extension='.txt') -> None: # Writes the data into a text file
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
        with open(f"{filename}{extension}", mode, encoding="utf-8") as file: #NOTE: reference ".txt".
            file.write(content + "\n")
            file.close()


    @staticmethod
    def getUserInput():  # Under revision
        pass