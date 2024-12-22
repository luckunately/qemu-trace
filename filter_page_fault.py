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

print(f"Reading input file {input_file}")
print(f"Writing output file {output_file}")

'''
[  116.658909] "4. Page fault at address", 7ff06583b000
[  116.659819] "4. Page fault at address", 7fff8968a000
[  116.661104] "4. Page fault at address", 55e0c76d3000
[  116.663539] "4. Page fault at address", 55e0c6434000
[  116.707381] "4. Page fault at address", 55e0c76d4000
[  116.743045] "4. Page fault at address", 55e0c76d5000
[  116.775877] "4. Page fault at address", 55e0c76d6000
[  116.806779] "4. Page fault at address", 55e0c76d7000
[  116.833698] "4. Page fault at address", 55e0c76d8000
[  116.858970] "4. Page fault at address", 55e0c76d9000
[  116.882494] "4. Page fault at address", 55e0c76da000
[  116.905252] "4. Page fault at address", 55e0c76db000
[  116.928025] "4. Page fault at address", 55e0c76dc000
[  116.950235] "4. Page fault at address", 55e0c76dd000
'''

# read input file, filter out all other lines, only keep the page fault lines, they contain the word "Page fault"
page_faults = []

with open(input_file, 'r') as file:
    for line in file:
        if "Page fault at address" in line:
            parts = line.split(',')
            if len(parts) == 2:
                address = parts[1].strip()
                page_faults.append(address)

# write the filtered page fault addresses to the output file
with open(output_file, 'w') as file:
    file.write("addr\n")
    for address in page_faults:
        file.write(f"{address}\n")
