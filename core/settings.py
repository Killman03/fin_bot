from dataclasses import dataclass
import config


@dataclass
class Bots:
    BOT_TOKEN: str
    ADMIN_ID: int


@dataclass
class Settings:
    bots: Bots


def get_settings() -> Settings:
    return Settings(
        bots=Bots(
            BOT_TOKEN=config.BOT_TOKEN,
            ADMIN_ID=config.ADMIN_ID,
        )
    )


settings = get_settings()