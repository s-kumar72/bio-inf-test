#! /usr/bin/python

import gemmi 
import os

def get_amino_counts(file_name):
    model = gemmi.read_structure(file_name)[0]

    chain_list = []
    for i in model:
        chain_list.append(model[i.name])
    
    chain = []
    for i in chain_list:
        holder = i.whole()
        chain.append(holder.make_one_letter_sequence())
    
    sequences = []
    for i in chain:
        i.replace('X', '', -1)
        i.replace('-', '', -1)
        sequences.append(i)
    # coverting list to a set keeps only unique entries
    unique_sequences = set(sequences)
    # convert unique set to a list
    unique_seq_list = list(unique_sequences)

    amino_acids = []
    
    # for each unique sequence
    for i in unique_seq_list:
        # split sequence into list of chars
        i_split = list(i)
        amino_acid_dict = {}
        # loop through list of chars
        for alph in i_split:
            # if char not already counted, count & add to dict
            if alph not in amino_acid_dict.keys():
                amino_acid_dict[alph] = i_split.count(alph)
        amino_acid_dict['total'] = len(i_split)
        # append dict to list 
        amino_acids.append(amino_acid_dict)

    return amino_acids
