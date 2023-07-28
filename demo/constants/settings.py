from pydantic import BaseSettings, HttpUrl, SecretStr
import os

from demo.constants.paths import ROOT_FOLDER


class Settings(BaseSettings):
    class Config:
        env_file = ROOT_FOLDER / "demo" / ".env"

    genoss_huggingfacehub_api_token: SecretStr
    genoss_openai_api_key: SecretStr
    genoss_custom_hf_endpoint_url: HttpUrl


SETTINGS = Settings()

print(SETTINGS.genoss_openai_api_key.get_secret_value())
print(os.environ.get("OPENAI_API_KEY"))
