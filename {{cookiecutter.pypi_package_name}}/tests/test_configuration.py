from pathlib import Path

from pydantic import SecretStr
import configuration as config

def test_settings_object():

    setting_obj = config.Settings()
    assert setting_obj.example_string == "Example Default"


def test_settings_load_missing():
    setting_obj = config.Settings().load("non_existent_config_file.toml")
    assert setting_obj.example_string == "Example Default"
    assert setting_obj.example_float is None

def test_settings_save_and_load(tmp_path: Path):
    test_config_file = tmp_path / "test_config.toml"

    # Create a settings object and modify some values
    setting_obj = config.Settings()
    setting_obj.example_string = "Modified String"
    setting_obj.example_int = 42
    setting_obj.example_section.example_key = "Modified Section Key"

    # Save the settings to the test config file
    setting_obj.save(custom_file=test_config_file)

    # Load the settings from the test config file
    loaded_settings = config.Settings.load(custom_file=test_config_file)

    # Verify that the loaded settings match the saved settings
    assert loaded_settings.example_string == "Modified String"
    assert loaded_settings.example_int == 42
    assert loaded_settings.example_section.example_key == "Modified Section Key"