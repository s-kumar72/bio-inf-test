#! /usr/bin/python

import gemmi 

def get_amino_counts(file):
    model = gemmi.read_structure(file)[0]

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
    
    unique_sequences = set(sequences)
    unique_seq_list = list(unique_sequences)

    amino_acids = []
    
    # dictlist = [dict() for x in range(n)]

    for i in unique_seq_list:
        i_split = list(i)
        amino_acid_dict = {}
        for alph in i_split:
            if alph not in amino_acid_dict.keys():
                amino_acid_dict[i] = unique_seq_list.count(i)
        amino_acids.append(amino_acid_dict)

    return amino_acids
