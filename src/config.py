from pydantic import BaseSettings


class Settings(BaseSettings):

    # Hardcoded values in env
    COGS: list
    COLOUR: int

    # Changeable fields
    TOKEN: str
    BOT_PREFIX: str
    OPENAI_KEY: str
    GUILD_ID: int | list
    LOG_CHANNEL_IDs: str | dict
    STAFF_IDS: dict

    class Config:

        env_file = ".env"
        env_file_encoding = "utf-8"
