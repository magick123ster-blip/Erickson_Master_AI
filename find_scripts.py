import pandas as pd
import numpy as np
import os

DATA_DIR = r'C:\Users\magic\Downloads\erickson_data'
INPUT_CSV = os.path.join(DATA_DIR, 'erickson_sequences.csv')

def find_script_names():
    df = pd.read_csv(INPUT_CSV)
    unique_names = df['script_id'].unique().tolist()
    for name in unique_names:
        print(name)

if __name__ == '__main__':
    find_script_names()
