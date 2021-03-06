import os
import yaml
import logging
import pandas as pd
import json

class common_tasks:
    def __init__(self):
        pass
    
    # @staticmethod
    def read_yaml(self,path_to_yaml: str) -> dict:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
        logging.info(f"yaml file: {path_to_yaml} loaded successfully")
        return content

    @staticmethod
    def create_directories(path_to_directories: list) -> None:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            logging.info(f"created directory at: {path}")

    @staticmethod
    def save_json(path: str, data: dict) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"json file saved at: {path}")
    
    @staticmethod
    def get_dataframe(path_to_data: str, sep: str="\t", encoding: str="utf-8") -> pd.DataFrame:
        df = pd.read_csv(path_to_data, sep=sep, encoding=encoding)
        logging.info(f"The input dataframe {path_to_data} of size {df.shape} is being read")
        return df

