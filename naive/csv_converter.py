import json
import pandas as pd
import os

folder = './data/'
json_file = 'transactions.json'
csv_file = 'transactions.csv'
csv_file_flatten = 'flatten_transactions.csv'

if not os.path.exists(folder + json_file):
    raise 'Path does not exists'

df = pd.read_json(folder + json_file)
df.to_csv(folder + csv_file)
