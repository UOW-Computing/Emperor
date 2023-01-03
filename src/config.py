from pydantic import BaseSettings


class Settings(BaseSettings):

    # Hardcoded values in env
    COGS: list
    COLOUR: int

    # Changeable fields
    TOKEN: str
    BOT_PREFIX: str
    GUILD_ID: int | list
    LOG_CHANNEL_ID: str | dict

    class Config:

        env_file = ".env"
        env_file_encoding = "utf-8"
