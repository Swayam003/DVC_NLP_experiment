import json
import os
from typing import Optional, Any

class Config(object):
    #########################
    # Singleton Design Pattern
    #########################

    _CONFIF_FILE: Optional[str] = None
    _CONFIG: Optional[dict] = None

    def __init__(self, config_file=None):

        if config_file is None:
            self._CONFIF_FILE = config_file
        
        assert os.path.exists(config_file)    # check if config file exists
        Config._CONFIF_FILE = config_file
        with open(config_file,'r') as file:
            Config._CONFIG = json.load(file)
    
    @staticmethod
    def get_config_file() -> str:
        return Config._CONFIF_FILE
    
    @staticmethod
    def get_required_config_var(configvar: str) -> Any:
        """ Return required config variable """

        assert Config._CONFIG
        if configvar not in Config._CONFIG:
            raise KeyError(f"{configvar} is not present in {Config._CONFIF_FILE}") 
        return Config._CONFIG[configvar]

config = Config(config_file='configs/config.yaml')