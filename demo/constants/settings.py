from pydantic import BaseSettings, HttpUrl, SecretStr

from demo.constants.paths import ROOT_FOLDER


class Settings(BaseSettings):
    class Config:
        env_file = ROOT_FOLDER / "demo" / ".env"

    huggingfacehub_api_token: SecretStr
    openai_api_key: SecretStr
    custom_hf_endpoint_url: HttpUrl


SETTINGS = Settings()
