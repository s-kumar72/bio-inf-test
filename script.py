#! /usr/bin/python
import requests
import argparse
import os

import pandas as pd
import numpy as np
import matplotlib as plt

import gemmi

import web_scraper as ws
import read_cif as rc

def file_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error('The file {} does not exist.'.format(arg))
    else:
        return open(arg, 'r')

parser = argparse.ArgumentParser(description='Parse a .txt file.')
parser.add_argument('file', 
                     help='Input PDB IDs as txt file', 
                     type=lambda x: file_exists(parser, x))
args = parser.parse_args()

# opens .txt file of PDB IDs and formats them as a list
ids = args.file.read()
id_list = ids.split('\n')

# fetches all the cif files from RCSB and puts them in a folder 
ws.fetch_cif_file(id_list)

amino_counts = []

for file_name in os.listdir('/data'):
    amino_counts = rc.get_amino_counts(file_name)
    for amino_dict in amino_counts: 
        # creates new dict to house counts & percentages for each amino acid in unique sequence 
        new_dict = {}
        for key in amino_dict.keys():
            if key not 'total':
                new_dict[key] = [amino_dict[key], (amino_dict[key] / amino_dict['total'] * 100)]
        
        # put all values into a list to make pd dataframe for plotting
        plot_list = []
        for key in new_dict.keys():
            plot_list.append([key, new_dict[key][0], new_dict[key][1]])

        # create pd dataframe from plot_list
        amino_data = pd.DataFrame(plot_list, columns = ['Name', 'Count', 'Percentage'])

        # create plots
        fig, axs = plt.subplots(2)
        axs[0].bar(amino_data['Name'], amino_data['Count'], align='center', alpha=0.5)
        axs[0].set_title('Amino Acid Counts')
        axs[0].set_xlabel('Amino Acid')
        axs[0].set_ylabel('Count')
        
        axs[1].bar(amino_data['Name'], amino_data['Percentage'], align='center', alpha=0.5) 
        axs[1].set_title('Amino Acid Percentages')
        axs[1].set_xlabel('Amino Acid')
        axs[1].set_ylabel('Percentage')

        # save figure
        plt.save_fig('file_name' + str(amino_dict.index()) + '.png')



