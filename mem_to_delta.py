import os, sys
import pandas as pd
from collections import Counter

# check input file and destination file, there might be a third argument as an integer
if len(sys.argv) < 3:
    print("Usage: python3 filter_page_fault.py <input_file> <output_file>")
    sys.exit(1)
    
input_file = sys.argv[1]
output_file = sys.argv[2]
    
# check if input file exists and change to absolute path
if not os.path.isfile(input_file):
    print("Input file does not exist")
    sys.exit(1)
else:
    input_file = os.path.abspath(input_file)
    
output_file = os.path.abspath(output_file)

df = pd.read_csv(input_file, nrows = 500_000_000)

addrs = df['addr'].apply(lambda x: int(x, 16) >> 12).tolist()
with open(output_file, 'w') as f:
    f.write("delta_in,delta_out\n")
    
    for i in range(1, len(df) - 1):
        delta_in = addrs[i] - addrs[i-1]
        delta_out = addrs[i + 1] - addrs[i]
        # if delta_in == 0:
        #     print(f"Page fault at {i}")
        # assert delta_in != 0 # delta_in should not be 0, no page fault twice in a row
        f.write(f"{(delta_in)},{(delta_out)}\n")
        