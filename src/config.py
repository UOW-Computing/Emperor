from pydantic import BaseSettings


class Settings(BaseSettings):

    TOKEN: str
    BOT_PREFIX: str
    GUILD_ID: str | list
    LOG_CHANNEL_ID: str | dict

    class Config:

        env_file = ".env"
        env_file_encoding = "utf-8"
