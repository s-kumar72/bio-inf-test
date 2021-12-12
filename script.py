#! /usr/bin/python
import requests
import argparse
import os

import pandas as pd
import numpy as np
import matplotlib as plt

import gemmi

def file_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error('The file {} does not exist.'.format(arg))
    else:
        return open(arg, 'r')

parser = argparse.ArgumentParser(description='Parse .txt file.')
parser.add_argument('file', required=True, 
                     help='Input PDB IDs as txt file', 
                     type=lambda x: file_exists(parser, x))
args = parser.parse_args()

print(args)
