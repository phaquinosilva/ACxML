from decimal import *
import pandas as pd

# read dataset into dataframes

# map to integers
def quantize(dataset):
    # find precision for each attr
    # multiply each attr column by 10^precision
    # save prec information for each attr
    # save precision information
    pass

def map_naturals(dataset):
    # find larges value below zero for each column (min if min < 0)
    # sum -min for each row in each attr column
    # save change for each attr
    pass

def process(dataset):
    quantize(dataset)
    map_naturals(dataset)
    # save values to .data file for training, testing and classification
    