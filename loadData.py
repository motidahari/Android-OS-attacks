

import json
import pandas as pd
from setting import config


def load_data():
    path = config['apksResultJsonPath']
    with open(path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    return 'sdcsdcdscdscdsc'
    return df