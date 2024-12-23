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
The example input file looks like this:

[  103.030429] "4. PF addr and ip", 7f723dc74000, 564e99125b4c
[  103.036384] "4. PF addr and ip", 7f7240110000, 564e99125b4c
[  103.039074] "4. PF addr and ip", 7f7240057000, 564e99125b4c
[  103.040801] "4. PF addr and ip", 7f723ad44000, 564e99125b4c
[  103.041854] "4. PF addr and ip", 7f723d731000, 564e99125b4c
[  103.048419] "4. PF addr and ip", 7f723edfa000, 564e99125b4c
[  103.049278] "4. PF addr and ip", 7f7240bfd000, 564e99125b4c
[  103.050232] "4. PF addr and ip", 7f723f633000, 564e99125b4c
[  103.051541] "4. PF addr and ip", 7f7242c76000, 564e991260ce
[  103.057721] "4. PF addr and ip", 7f7237684000, 564e9912602f
[  103.059359] "4. PF addr and ip", 7f72409a1000, 564e99125b4c
[  103.062051] "4. PF addr and ip", 7f723ed53000, 564e99125b4c
[  103.066602] "4. PF addr and ip", 7f724005a000, 564e99125b4c
[  103.068920] "4. PF addr and ip", 7f723d72d000, 564e99125b4c
'''

# read input file, filter out all other lines, only keep the page fault lines
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    outfile.write("pc,addr\n")
    for line in infile:
        if "PF addr and pc" in line:
            parts = line.split(',')
            if len(parts) == 3:
                address = parts[1].strip()
                ip = parts[2].strip()
                outfile.write(f"{ip},{address}\n")
