#import argparse
#import pickle
from datetime import datetime
import multiprocessing
import functools
import numpy as np
import pandas as pd
import time
import sys

import urllib
import urllib.request
import urllib.error

def annotate_from_uniprot(protein_id_string):

    #protein_id="P12345"
    #protein_id_string="sp|P27333|TGB3_LSV"
    protein_id=protein_id_string
    pos_1=protein_id_string.find("|")
    if pos_1>=0:
        pos_2=protein_id_string.find("|",pos_1+1)
        protein_id=protein_id_string[pos_1+1:pos_2]


    url = "https://www.uniprot.org/uniprot/"+protein_id+".txt"

    #page = urllib.request.urlopen(url)
    #html_bytes = page.read()

    
    html_bytes=""
    error_message=""

    try:
        page = urllib.request.urlopen(url)
        html_bytes = page.read()
    except urllib.error.HTTPError as err:
        if err.code == 404:
            error_message="Error code: Page not found!"
        elif err.code == 403:
            error_message="Error code: Access denied!"
        else:
            error_message="Something happened! Error code :"+err.code
        pass
    except urllib.error.URLError as err:
        error_message="Some other error happened: Error code :"+err.reason
        pass

    if error_message!="":
        result_tuple=(protein_id_string,error_message,"","")
        return result_tuple

    data = html_bytes.decode("utf-8")
    pos=data.find("OS ")
    pos_end=data.find(".\n",pos)
    species=""
    ec=""
    tax=""
    if pos>=0 and pos_end>=pos:
        species=data[pos+3:pos_end].strip()
        species=species.replace("\nOS  ","")

    ec_pos=data.find("EC=")
    if ec_pos>=0:
        ec_end=data.find(" ",ec_pos)
        ec_end_2=data.find(";",ec_pos)
        ec=data[ec_pos+3:min(ec_end,ec_end_2)]

    tax_pos=data.find("NCBI_TaxID=")
    if tax_pos>=0:
        tax_end=data.find(" ",tax_pos)
        tax_end_2=data.find(";",tax_pos)
        tax=data[tax_pos+11:min(tax_end,tax_end_2)]

    go_values = []
    go_value_not_found = True
    go_pos = 0
    while(go_value_not_found):
        go_pos=data.find("GO:",go_pos+1)
        if go_pos > 0:
            go_end=data.find(";",go_pos)
            go_values.append(data[go_pos+3:go_end])
        else:
            go_value_not_found = False
    go_value_string = ''
    for go_value in go_values:
        go_value_string += go_value
        go_value_string += ','
    go_value_string = go_value_string[:-1]

    #output_file.write(protein_id_string+"\t"+species+"\t"+tax+"\t"+ec+"\n")
    result_tuple=(protein_id_string,species,tax,ec, go_value_string)
    return result_tuple

def annotate_from_uniprot_parallel(inputfilename, outputfilename, num_thread):
    
    protein_id_list = [line.rstrip() for line in open(inputfilename,'r')]
    
    start = time.time()
    pool = multiprocessing.Pool(num_thread)
    result_tuples=pool.map(annotate_from_uniprot, protein_id_list)
    
    pool.close()
    pool.join()
    end = time.time()
    print(end-start)
    
    result_df=pd.DataFrame.from_records(result_tuples,columns=["protein_id","species","tax_id","EC", "GO values"])
    
    result_df.to_csv(outputfilename,index=None, sep="\t")


def main(argv):
    print('python get_annot_from_uniprot.py <inputfile> <outputfile> <num_of_thread>')
    inputfilename =argv[0]
    outputfilename = argv[1]
    num_thread=int(argv[2])
    annotate_from_uniprot_parallel(inputfilename, outputfilename, num_thread)

if __name__ == "__main__":
    main(sys.argv[1:])
    #test_cmd="get_annot_from_uniprot.py yao/test_ids.txt yao/test_ids_annot.txt 4".split(" ")
    #main(test_cmd[1:])
