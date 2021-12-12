#! /usr/bin/python

import requests

def fetch_cif_file(pdb_id):
        # URL to download PDB/mmCIF files from RCSB
        base_url = 'https://files.rcsb.org/download/PDBID.cif'

        for id in pdb_id:
                r = requests.get(base_url.replace('PDBID',id,-1))
                file_name = "data/" + id + ".cif"
                with open(file_name, 'wb') as fd:
                        fd.write(r.text)