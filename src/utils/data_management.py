from cmath import pi
import logging
import random
from turtle import title
from typing import Any
from tqdm import tqdm
import xml.etree.ElementTree as ET
import re
import joblib
import numpy as np
import pandas as pd
import scipy.sparse as sparse

class data_management:
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_posts(fd_in, fd_out_train, fd_out_test, target_tag, split) -> None:
        line_num = 1
        column_names = "pid\tlabel\ttext\n"
        fd_out_train.write(column_names)
        fd_out_test.write(column_names)
        for line in tqdm(fd_in):
            try:
                fd_out = fd_out_train if random.random() > split else fd_out_test
                attr: str = ET.fromstring(line).attrib   # gets the tags
                pid: Any = attr.get('Id', "")
                label: int = 1 if target_tag in attr.get('Tags',"") else 0
                title: str = re.sub(r"\s+", " ", attr.get('Title', "")).strip()
                body: str = re.sub(r"\s+", " ", attr.get('Body', "")).strip()
                text: str = f"{title} {body}"

                fd_out.write(f"{pid}\t{label}\t{text}\n")
                line_num += 1
            except Exception as e:
                logging.error(f"skipping the broken line {line_num} : {e}")
    
    @staticmethod
    def save_matrix(df: pd.DataFrame, test_matrix,  out_path: str) -> None:
        pid_matrix = sparse.csr_matrix(df.pid.astype(np.int64)).T
        label_matrix = sparse.csr_matrix(df.label.astype(np.int64)).T
        result = sparse.hstack([pid_matrix, label_matrix, test_matrix], format="csr")

        joblib.dump(result, out_path)
        logging.info(f"The output matrix saved at {out_path} of shape: {result.shape}")
