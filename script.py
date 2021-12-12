#! /usr/bin/python
import requests
import argparse
import os

import pandas as pd
import numpy as np
import matplotlib as plt

import gemmi

import web_scraper as ws

def file_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error('The file {} does not exist.'.format(arg))
    else:
        return open(arg, 'r')

parser = argparse.ArgumentParser(description='Parse .txt file.')
parser.add_argument('file', 
                     help='Input PDB IDs as txt file', 
                     type=lambda x: file_exists(parser, x))
args = parser.parse_args()

ids = args.file.read()

id_list = ids.split('\n')

ws.fetch_cif_file(id_list)

