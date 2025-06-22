import os
import pickle


def read_dict_pickle(read_file_path: str) -> dict:
    with open(read_file_path, 'rb') as f:
        return pickle.load(f)


def write_dict_pickle(data: dict, write_file_path: str) -> None:
    dirpath = os.path.dirname(write_file_path)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)
    with open(write_file_path, 'wb') as f:
        pickle.dump(data, f)
