import argparse
import pickle
from datetime import datetime
import multiprocessing
import functools
import numpy as np
import os
import pandas as pd
import pickle
import time
import faiss

def load_database(db_file):
    print("Loading database at " + str(datetime.now()))
    print("Database: " + db_file)
    with open(db_file, "rb") as f:
        peptide_db = pickle.load(f)
    print("Database loaded at " + str(datetime.now()))
    return peptide_db

def faiss_k_nearest_neighbors(num_thread, threshold, k, db, input_protein_list, index_file_path, dimensions):
    if not os.path.exists(index_file_path):
        # Create new index
        print("Creating index")
        numpy_db = convert_to_numpy_array(db)
        d = dimensions                           # dimensions
        index = faiss.IndexFlatL2(d)   # build the index
        index.add(numpy_db)                  # add vectors to the index
        with open(index_file_path, "wb") as pick:
            pickle.dump(index, pick)
    else:
        # Load index
        print("Loading index")
        with open(index_file_path, "rb") as f:
            index = pickle.load(f)
    print("Index loaded")

    vectors_to_search = convert_to_numpy_array(input_protein_list)
    D, I = index.search(vectors_to_search, k)

    # Converts the indexes back into their id
    array_with_query_id = np.empty((len(I), len(I[0]) + 1)).astype(str)
    distance_array_with_query_id = np.empty((len(D), len(D[0]) + 1)).astype(str)
    for row in range(0, len(I)):
        array_with_query_id[row][0] = input_protein_list[row][0]
        distance_array_with_query_id[row][0] = input_protein_list[row][0]
        for col in range(0, len(I[0])):
            index = int(I[row][col])
            array_with_query_id[row][col + 1] = str(db[index][0])
            distance_array_with_query_id[row][col + 1] = str(D[row][col])
    results_df = pd.DataFrame.from_records(array_with_query_id,columns=['query_id']+["top_"+str(i+1) for i in range(0,k)])
    distance_results_df = pd.DataFrame.from_records(distance_array_with_query_id,columns=['query_id']+["top_"+str(i+1) for i in range(0,k)])
    return (results_df, distance_results_df)
    
def convert_to_numpy_array(list):
    # Removes index from array and then converts to numpy array
    array = []
    valid_lines = 0
    invalid_lines = 0
    for line in list:
        array.append(line[1])
        if(len(line[1]) != 1280):
            invalid_lines += 1
        else:
            valid_lines += 1
    print(invalid_lines)
    print(valid_lines)
            
    return np.array(array)

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

def main(input_file, output_fp, nodes, db_file, dimensions):
    #global variable for db
    db=load_database(db_file)
    num_thread=nodes
    threshold=9999999999
    k=10


    
    print("Loading input file at " + str(datetime.now()))
    with open(input_file, "rb") as f:
        input_protein_list = pickle.load(f)
    print("Input file loaded at " + str(datetime.now()))
    
    print("Calculating nearest neighbors at " + str(datetime.now()))

    index_file_path = output_fp + "/index.pkl"
    
    start_time = time.time()
    faiss_results = faiss_k_nearest_neighbors(num_thread, threshold, k, db, input_protein_list, index_file_path, dimensions)
    faiss_id_results = faiss_results[0]
    faiss_distance_results = faiss_results[1]
    end_time = time.time()
    print("K nearest neighbors took " + str(end_time-start_time) + " seconds to run")

    knn_output_fp = output_fp + "/knn_output.csv"
    distance_output_fp = output_fp + "/distance_output.csv"
    faiss_id_results.to_csv(knn_output_fp,index=None, sep="\t")
    faiss_distance_results.to_csv(distance_output_fp,index=None, sep="\t")
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
        "--output_fp",
        help="An output file path containing proteins and their distances between each other and other files.",
    )
    parser.add_argument(
        "--nodes",
        default=24
    )
    parser.add_argument(
        "--db",
        help="A path to the .pkl file for the peptide database",
    )
    parser.add_argument(
        "--dim",
        help="Number of dimensions in vector embeddings",
        type=int,
        default=1280
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args.input_file, args.output_fp, args.nodes, args.db, args.dim)
