import json
import os
from typing import Optional, Any
import yaml

class Config:
    #########################
    # Singleton Design Pattern
    #########################

    # _CONFIF_FILE: Optional[str] = None
    # _CONFIG: Optional[dict] = None

    def __init__(self, config_file=None):

        if config_file is None:
            self._CONFIF_FILE = config_file
        
        assert os.path.exists(config_file)    # check if config file exists
        # Config._CONFIF_FILE = config_file
        self._CONFIF_FILE = config_file
        with open(config_file,'r') as file:
            # Config._CONFIG = yaml.safe_load(file)
            self._CONFIG = yaml.safe_load(file)
            
    # @staticmethod
    def get_config_file(self) -> str:
        return self._CONFIF_FILE
    
    # @staticmethod
    def get_required_config_var(self,configvar: str) -> Any:
        """ Return required config variable """

        assert self._CONFIG
        if configvar not in self._CONFIG:
            raise KeyError(f"{configvar} is not present in {self._CONFIF_FILE}") 
        return self._CONFIG[configvar]

config = Config(config_file='configs/config.yaml')
params = Config(config_file='params.yaml')