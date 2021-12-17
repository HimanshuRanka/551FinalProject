import pandas as pd
import os.path as osp

# names of the data files
unseen = "data_test_500_rand1_unseen.json"
seen = "data_test_500_rand1_seen.json"

data = pd.read_csv(osp.join("data", unseen))

