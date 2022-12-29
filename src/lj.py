import time
from datetime import datetime



log_file = r"logs/log-"+ datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")


class Lj:
    def __init__(self):
        pass

    @staticmethod
    def warn(context: str = "main", msg: str = "Unknown error occured!") -> None:

        # get the current time
        ctime = time.ctime(time.time())
        # Print ot console
        warn_format = f"[{ctime}] [{context}] \x1b[2;30;41m[WARN] {msg}\x1b[0m"
        print(warn_format)

        try:
            # save to file
            with open(log_file, "a", encoding="utf-8") as logFile:
                logFile.write(warn_format + "\n")
            logFile.close()
        except FileNotFoundError:
            print("File not found")
            

    @staticmethod
    def log(context: str = "main", message: str = "No context provided") -> None:
        # print to console
        log_format = f"[{time.ctime(time.time())}] [{context}]: {message}"
        print(log_format)

        try:
            # save to file
            with open(log_file, "a", encoding="utf-8") as logFile:
                logFile.write(log_format + "\n")
            logFile.close()
        except FileNotFoundError:
            print("File not found")

    @staticmethod
    def error(
        context: str = "main", message: str = "Unknown exception was not handled"
    ):
        # get the current time
        ctime = time.ctime(time.time())
        # Print ot console
        error_format = f"[{ctime}] [{context}] \x1b[2;30;41m[ERROR] {message}\x1b[0m"
        print("\n", error_format, "\n")

        try:
            # save to file
            with open(log_file, "a", encoding="utf-8") as logFile:
                logFile.write(error_format + "\n")
            logFile.close()
        except FileNotFoundError:
            print("File not found")
