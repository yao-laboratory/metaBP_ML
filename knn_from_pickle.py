import argparse
import pickle
from datetime import datetime
import multiprocessing
import functools
import numpy as np
import pandas as pd
import time

db_file = "./peptide_db.pkl"
print("Loading database at " + str(datetime.now()))
with open(db_file, "rb") as f:
    peptide_db = pickle.load(f)
print("Database loaded at " + str(datetime.now()))

#global variable for db
db=peptide_db


def nearest_k_neighbors(threshold, k, input_protein):
    result = [("",threshold)]*(k+1)
    for d in db:
        temp = np.subtract(input_protein[1],d[1])
        distance = np.dot(temp,temp)
        for i in range(0,k):
            j = k-1-i
            if distance<=result[j][1]:
                result[j+1]=result[j]
                new_tuple=(d[0],distance)
                result[j]=new_tuple
    result_list=[input_protein[0]]+[result[i][0] for i in range(0,k)]
    return tuple(result_list)
    

def multiple_process(num_thread, threshold, k, input_protein_list):
       
    pool = multiprocessing.Pool(int(num_thread))
    
    partial_function=functools.partial(nearest_k_neighbors, threshold, k)
    
    results=pool.map(partial_function, input_protein_list)
    
    pool.close()
    pool.join()
    
    results_df=pd.DataFrame.from_records(results,columns=['query_id']+["top_"+str(i+1) for i in range(0,k)])

    return results_df

'''
def main(thread):
    num_thread=thread
    threshold=99999999
    k=3
    input_protein_list=mock_db[0:20]
    start = time.time()
    result_df = multiple_process(num_thread, threshold, k, input_protein_list)
    end = time.time()
    print(end-start)
    return result_df
'''

def main(input_file, output_file, nodes):
    
    num_thread=nodes
    threshold=9999999999
    k=10


    
    print("Loading input file at " + str(datetime.now()))
    with open(input_file, "rb") as f:
        input_protein_list = pickle.load(f)
    print("Input file loaded at " + str(datetime.now()))
    
    print("Calculating nearest neighbors at " + str(datetime.now()))
    
    result_df = multiple_process(num_thread, threshold, k, input_protein_list)
    
    result_df.to_csv(output_file,index=None, sep="\t")
    
    print("Distances nearest neighbors at " + str(datetime.now()))

def parse_args():
    parser = argparse.ArgumentParser(
        description="This script takes in the output of compute_bulk_embeddings.py (of format (prot, mean_vector)) and outputs a pkl file.)"
    )
    parser.add_argument(
        "input_file",
        help="A .pkl input file containing a list of tuples of the form (prot_name, seq).",
    )
    parser.add_argument(
        "--output_file",
        default="./distances.txt",
        help="An output file containing proteins and their distances between each other.",
    )
    parser.add_argument(
        "--nodes",
        default=24
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args.input_file, args.output_file, args.nodes)
