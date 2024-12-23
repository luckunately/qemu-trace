import os, sys
import pandas as pd
from collections import Counter

# check input file and destination file, there might be a third argument as an integer
if len(sys.argv) < 3:
    print("Usage: python3 fltrace_to_mem_access.py <input_file> <output_file> [top_x]")
    sys.exit(1)
    
input_file = sys.argv[1]
output_file = sys.argv[2]
top_x = None
if len(sys.argv) == 4:
    top_x = int(sys.argv[3])
else:
    top_x = 50000
    print(f"Top_x not specified, using default value {top_x}")
    
# check if input file exists and change to absolute path
if not os.path.isfile(input_file):
    print("Input file does not exist")
    sys.exit(1)
else:
    input_file = os.path.abspath(input_file)
    
output_file = os.path.abspath(output_file)

print(f"Reading input file {input_file}")
print(f"Writing output file {output_file}")

# read input file
df = pd.read_csv(input_file, sep=',')

def filter_top_x_entries(df, columns, x):
    # Step 2: Identify top x entries for each column
    top_x_entries = {}
    for column in columns:
        counts = Counter(df[column])
        top_x = counts.most_common(x)
        top_x_entries[column] = {entry for entry, count in top_x}

    
    # Step 3: Filter rows
    for column in columns:
        df = df[df[column].isin(top_x_entries[column])]
    
    return df

# Columns to filter and top x value
columns = ['pc', 'delta_in', 'delta_out']

# Filter DataFrame
filtered_df = filter_top_x_entries(df, columns, top_x)

# write to output file
filtered_df.to_csv(output_file, index=False)

    
