import tomllib
import tomli_w
from typing import Optional
from pathlib import Path
from pydantic import SecretStr, Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class ExampleSection(BaseModel):
    example_key: str = "example_value"
    maybe_value: Optional[int] = None

class Settings(BaseSettings):
    default_config_dir: Path = Field(default=Path.home() / ".config", # / "python-boilerplate",
        description="Default path to user configuration file.", exclude=True)
    config_file_name: Path = Field(default=Path("python_boilerplate.toml"),
        description="Name of the configuration file.", exclude=True)
    logfile: str = "python-boilerplate.log"
    example_string: str = Field(default="Example Default", description="An example string value.")
    example_int: Optional[int] = None
    example_float: Optional[float] = None
    example_bool: bool = True
    example_list: list[int] = [1, 2, 3]
    example_dict: dict[str, str] = {"key": "value", "foo": "bar"}
    example_section: ExampleSection = ExampleSection()

    model_config = SettingsConfigDict(
        env_prefix="PYTHON_BOILERPLATE_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def load(cls, custom_file: Optional[Path | str] = None) -> "Settings":
        # Use the provided custom file, or look for config file in standard locations
        if custom_file is not None and Path(custom_file).is_file():
            config_file = Path(custom_file)
        elif Path(Path.cwd() / cls().config_file_name).is_file():
            # Check for config in current directory
            config_file = Path.cwd() / cls().config_file_name
        elif Path(cls().default_config_dir / cls().config_file_name).is_file():
            # Wherever the heck we specified
            config_file = cls().default_config_dir / cls().config_file_name
        else:
            # Return default settings if no config file found
            return cls()

        if config_file.is_file():
            with config_file.open("rb") as f:
                config_data = tomllib.load(f)
            return cls.model_validate(config_data)
        
        return cls()
    
    def save(self, custom_file: Optional[Path] = None) -> None:
        # Use the provided custom file, or look for config file in standard locations
        if custom_file is not None:
            config_file = custom_file
        else:
            config_file = self.default_config_dir / self.config_file_name

        config_file.parent.mkdir(parents=True, exist_ok=True)

        with config_file.open("wb") as f:
            tomli_w.dump(self.model_dump(mode="json",exclude_none=True), f)