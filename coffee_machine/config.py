import json
import os


BASE_DIR = os.path.dirname(__file__)
PARAMS_FILE = os.path.join(BASE_DIR, 'params.json')
CONFIG_FILE = os.path.join(BASE_DIR, 'config.json')


def _get_settings_file(path):
    if not os.path.isfile(path):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        raise FileNotFoundError('Settings file: "{}" not found in directory: "{}"'.format(filename, directory))
    with open(path, 'r') as json_config_file:
        settings = json.load(json_config_file)
    return settings


def get_params():
    return _get_settings_file(PARAMS_FILE)


def get_config():
    return _get_settings_file(CONFIG_FILE)
