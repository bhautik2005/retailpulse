import pandas as pd

def load_data(config):

    base_path = config["data"]["raw_path"]
    files = config["files"]

    data = {}

    for key, filename in files.items():
        data[key] = pd.read_csv(base_path + filename)

    return data