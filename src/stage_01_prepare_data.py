import argparse
import os
import logging
from src.utils.common import common_tasks
from src.utils.data_management import data_management
import random


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
        self.tasks = common_tasks()
        self.data_mgnmt = data_management()

    def main(self):
        ## read config files
        config = self.tasks.read_yaml(self.config_path)
        params = self.tasks.read_yaml(self.params_path)
        
        source_data_dir = config["source_data"]["data_dir"]
        source_data_file = config["source_data"]["data_file"]
        source_data_path = os.path.join(source_data_dir, source_data_file)

        split = params["prepare"]["split"] # split ratio
        seed = params["prepare"]["seed"]
        tag = params["prepare"]["tag"]

        random.seed(seed)

        artifacts = config["artifacts"]
        prepare_data_dir_path = os.path.join(artifacts["ARTIFACTS_DIR"], artifacts["PREPARED_DATA"])
        self.tasks.create_directories([prepare_data_dir_path])

        train_data_path = os.path.join(prepare_data_dir_path,artifacts["TRAIN_DATA"])
        test_data_path = os.path.join(prepare_data_dir_path,artifacts["TEST_DATA"])

        encode = "utf8"
        with open(source_data_path, encoding=encode) as fd_in: # actual input data that we are reading
            with open(train_data_path, "w", encoding=encode) as fd_out_train: # writing train data
                with open(test_data_path, "w", encoding=encode) as fd_out_test: # writing test data
                    self.data_mgnmt.process_posts(fd_in, fd_out_train, fd_out_test, tag, split)

data_prep = prepare_dataset(config_path="configs/config.yaml", params_path="params.yaml")
data_prep.main()
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