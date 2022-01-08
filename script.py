#! /usr/bin/python

import requests
import argparse
import os

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
paser.add_argument('--result_dir', dest='rdir',
                    required=True, help="""absolute path to the 
                    directory to store the results""",
                    type=str)

args = parser.parse_args()

# opens .txt file of PDB IDs and formats them as a list
ids = args.file.read()
id_list = ids.split('\n')
result_dir = args.rdir

# fetches all the cif files from RCSB and puts them in a folder 
ws.fetch_cif_file(id_list, result_dir)

amino_counts = []
files_not_read = []

cif_plt_path = os.path.join(result_dir, 'cif_plots')
cif_data_path = os.path.join(result_dir, 'cif_data')
if not os.path.exists(cif_plt_path):
    os.mkdir(cif_plt_path)             
for file_name in os.listdir(cif_data_path):
    cif_file = os.path.join(cif_data_path, file_name)
    if os.path.exists(cif_file):
        amino_counts = rc.get_amino_counts(cif_file)
        
        for amino_dict in amino_counts: 
            
            # removes an - in amino dict
            if '-' in amino_dict.keys():
                count = amino_dict['_']
                del(amino_dict['-'])
                amino_dict['total'] = amino_dict['total'] - count
                
            # creates new dict to house counts & percentages for each amino acid in unique sequence 
            new_dict = {}
            for key in amino_dict.keys():
                if key != 'total':
                    new_dict[key] = [amino_dict[key], (float(amino_dict[key]) / float(amino_dict['total']) * 100)]
    
            # put all values into a list to make pd dataframe for plotting
            plot_list = []
            for key in new_dict.keys():
                plot_list.append([key, new_dict[key][0], new_dict[key][1]])
                
            names_list = []
            counts_list = []
            percents_list = []
            
            for list in plot_list:
                names_list.append(list[0])
                counts_list.append(list[1])
                percents_list.append(list[2])
               
            # create plot
            w = 0.4
            bar1 = np.arange(len(names_list))
            bar2 = [i + w for i in bar1]
            
            plt.bar(bar1, counts_list, w, label="Count")
            plt.bar(bar2, percents_list, w, label="Percentage)
                    
            plt.xlabel("Amino Acids")
            plt.ylabel("Frequency")
            plt.xticks(bar1 + (w/2), names_list)
            plt.title("Amino Acid Count Frequency")

            # save figure & add to plots folder
            plot_name = file_name + str(amino_dict.index()) + '.png'
            plot_file = os.path.join(cif_plt_path, plot_name)
            plt.savefig(plot_file)
    else:
        files_not_read.append(file_name) 

print(files_not_read)
print("Sequence Completed.")
