#!/usr/bin/env python

'''
Kristopher Overholt
7/23/2014
This script will offset specified data columns in a .csv file.
For example, this is useful when adjusting gas concentration data
to account for the sample lag time (e.g., a 10 second delay).

Example usage to offset all gas concentration columns by 10 seconds:
python Offset_Data.py Test_Input.csv Test_Output.csv 'CO_A,CO2_A,O2_A,CO_B,CO2_B,O2_B' 10
'''

import sys
import argparse
import numpy as np
import pandas as pd

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='File name of input .csv file')
parser.add_argument('output_file', help='File name of output .csv file')
parser.add_argument('columns', help='Names of column headers to offset, separated by commas')
parser.add_argument('seconds', help='Number of seconds to offset column data')
args = parser.parse_args()

# Convert offset to integer
offset = int(args.seconds)

# Read in input CSV file
data = pd.read_csv(args.input_file, index_col=0)

# Loop through column names and offset each column
for column in args.columns.split(','):
    try:
        data[column] = data[column].shift(-offset)
    except KeyError:
        # Exit program if the column name does not exist
        print 'Error: Column ' + column + ' does not exist in input file'
        sys.exit()

# Offset entire data file
data = data[:-offset]

# Write output .csv data file
data.to_csv(args.output_file)
