#! /usr/bin/python

import requests
import os

def fetch_cif_file(pdb_id):
        path = 'cif_data'
        if not os.path.exists(path):
            os.mkdir(path)
        # URL to download PDB/mmCIF files from RCSB
        base_url = 'https://files.rcsb.org/download/PDBID.cif'

        for id in pdb_id:
                r = requests.get(base_url.replace('PDBID', id, -1))
                file_name = id + '.cif'
                file_loc = os.path.join('cif_data/', file_name)
                with open(file_loc, 'wb') as fd:
                        fd.write(r.text)