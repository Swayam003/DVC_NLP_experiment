import argparse
import os
import logging
import traceback
import src.utils as utils
# from src.utils.data_management import data_management
import random
from configs import config_settings


STAGE = "Prepare_data"

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )

class prepare_dataset:
    def __init__(self, config_path: str, params_path: str) -> None:
        self.config_path = config_path
        self.params_path = params_path
        self.tasks = utils.common_tasks()
        self.data_mgnmt = utils.data_management()

    def main(self):
        ## read config files
        # config = self.tasks.read_yaml(self.config_path)
        # params = self.tasks.read_yaml(self.params_path)
        
        config_obj = config_settings.config
        config = config_obj.get_required_config_var("source_data")
        source_data_dir = config.get("data_dir", None)
        source_data_file = config.get("data_file",None)

        # source_data_dir = config["source_data"]["data_dir"]
        # source_data_file = config["source_data"]["data_file"]
        source_data_path = os.path.join(source_data_dir, source_data_file)

        params_obj = config_settings.params
        params = params_obj.get_required_config_var("prepare")
        split = params.get("split", None)
        tag = params.get("tag",None)
        seed = params.get("seed",None)
        # split = params["prepare"]["split"] # split ratio
        # tag = params["prepare"]["tag"]
        # seed = params["prepare"]["seed"]

        random.seed(seed)

        # artifacts = config["artifacts"]
        artifacts = config_obj.get_required_config_var("artifacts")
        artifacts_dir = artifacts.get("ARTIFACTS_DIR", None)
        prepared_data = artifacts.get("PREPARED_DATA", None)
        train_data = artifacts.get("TRAIN_DATA", None)
        test_data = artifacts.get("TEST_DATA", None)

        # prepare_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DATA"])
        prepare_data_dir_path = os.path.join(artifacts_dir, prepared_data)
        self.tasks.create_directories([prepare_data_dir_path])

        train_data_path = os.path.join(prepare_data_dir_path,train_data)
        test_data_path = os.path.join(prepare_data_dir_path,test_data)

        encode = "utf8"
        with open(source_data_path, encoding=encode) as fd_in: # actual input data that we are reading
            with open(train_data_path, "w", encoding=encode) as fd_out_train: # writing train data
                with open(test_data_path, "w", encoding=encode) as fd_out_test: # writing test data
                    self.data_mgnmt.process_posts(fd_in, fd_out_train, fd_out_test, tag, split)

try:
    logging.info("\n********************")
    logging.info(f">>>>> stage {STAGE} started <<<<<")
    data_prep = prepare_dataset(config_path="configs/config.yaml", params_path="params.yaml")
    data_prep.main()
    logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
except Exception as e:
    logging.error(traceback.print_exc())
    raise e
# if __name__ == '__main__':
#     args = argparse.ArgumentParser()
#     args.add_argument("--config", "-c", default="configs/config.yaml")
#     args.add_argument("--params", "-p", default="params.yaml")
#     parsed_args = args.parse_args()

#     try:
#         logging.info("\n********************")
#         logging.info(f">>>>> stage {STAGE} started <<<<<")
#         main(config_path=parsed_args.config, params_path=parsed_args.params)
#         logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
#     except Exception as e:
#         logging.exception(e)
#         raise e