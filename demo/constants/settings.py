import requests
from pydantic import BaseSettings, HttpUrl, SecretStr
from pydantic.env_settings import SettingsSourceCallable

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

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            # Ignore secrets settings as
            # we ran into issues in the past with bad token being set.
            return init_settings, env_settings

    huggingfacehub_api_token: SecretStr
    openai_api_key: SecretStr
    custom_hf_endpoint_url: HttpUrl | None = None
    genoss_endpoint_url: str = "http://localhost:4321"

    def ping_genoss_backend(self) -> None:
        """Ping Genoss to check that the endpoint is working."""
        response = requests.get(self.genoss_endpoint_url)
        response.raise_for_status()


SETTINGS = Settings()

print(SETTINGS.genoss_openai_api_key.get_secret_value())
print(os.environ.get("OPENAI_API_KEY"))
