import pandas as pd
import numpy as np

df = pd.read_csv('F:/DataScience/New folder/Latest/finalcode/04-08-2021/pan_batch_upload_sample.csv', encoding='latin1')
print(df.info())
print(df)
print(df.iloc[0]['f_name'])
print(df.shape)
print(df.shape[0])
print(df.columns)
