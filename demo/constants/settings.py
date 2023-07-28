import requests
from pydantic import BaseSettings, HttpUrl, SecretStr

from demo.constants.paths import ROOT_FOLDER


class Settings(BaseSettings):
    """Settings for the demo app.

    Reads from demo/.env file or environment variables.
    You can create the .env file from the .env_example file.

    !!! SecretStr is a pydantic type that hides the value in logs.
    If you want to use the real value, you should do:
    SETTINGS.<variable>.get_secret_value()
    """

    class Config:
        env_file = ROOT_FOLDER / "demo" / ".env"

    huggingfacehub_api_token: SecretStr
    openai_api_key: SecretStr
    custom_hf_endpoint_url: HttpUrl
    genoss_endpoint_url: str = "http://localhost:4321"

    def ping_genoss_backend(self) -> None:
        """Ping Genoss to check that the endpoint is working."""
        response = requests.get(self.genoss_endpoint_url)
        response.raise_for_status()


SETTINGS = Settings()
