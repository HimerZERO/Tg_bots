from dataclasses import dataclass
from environs import Env


@dataclass
class Url:
    path: str

    def to(self, step: str):
        return Url(f"{self.path}/{step}")


@dataclass
class TgBot:
    token: str
    admins: list[str]


@dataclass
class Config:
    bot: TgBot
    urls: dict[str, Url]


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)

    config = Config(
        bot=TgBot(
            env("BOT_TOKEN"),
            env.list("ADMINS"),
        ),
        urls={
            "CAT_API": Url(env("CAT_API")),
            "TG_API": Url(env("TG_API")),
            "HTTP_CAT": Url(env("HTTP_CAT")),
        },
    )
    return config
