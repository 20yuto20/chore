import pandas as pd
from datetime import datetime

students_df = pd.read_csv('/Users/yutokohata/Desktop/chores/stinfo_20240616.csv', delimiter='\t', error_bad_lines = False, encoding='UTF-8')
nrt_by_hs_df = pd.read_csv('/Users/yutokohata/Desktop/chores/nrt_by_hs.csv', delimiter=',', error_bad_lines = False, encoding='shift-jis', skiprows=2)
st_by_high_df = pd.read_csv('/Users/yutokohata/Desktop/chores/st_by_high.csv', delimiter=',', error_bad_lines = False, encoding='shift-jis', skiprows=2)
uni_df = pd.read_csv('/Users/yutokohata/Desktop/chores/uni_code.csv', delimiter=',', error_bad_lines = False, encoding='shift', skiprows=2)

all_inst_df = pd.concat([nrt_by_hs_df, st_by_high_df, uni_df], index = True)
print(all_inst_df)