import pandas as pd
df = pd.read_csv("test_example.csv", header=None).rename(
                 columns={0:'chapter', 1:'sentence', 2:'text'})
