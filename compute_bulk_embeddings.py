import argparse
import os
import sys
import numpy
import torch
from Bio import SeqIO
from io import StringIO
import time

numpy.set_printoptions(threshold=sys.maxsize)


def format_data(input_file):
    with open(input_file, 'r') as f:
        proteins = []
        for line in f:
            if line.startswith('>'):
                proteins.append(line)
            else:
                proteins[-1] += line
                
    data = []
    for protein in proteins:
        for sequence in SeqIO.parse(StringIO(protein), 'fasta'):
            data.append((sequence.name, str(sequence.seq)))
            
    return data


def batch_data(data, batch_size):
    
    batched_data = []
    start = 0
    end = batch_size if (len(data) > batch_size) else len(data)

    
    while True:
        print(f'Batching proteins {start} to {end}')
        new_data = data[start:end]
        batched_data.append(new_data)
        start += batch_size
        end = (start+batch_size) if (start+batch_size < len(data)) else len(data) 
        if start >= end:
            break
            
    return batched_data
    
    
def compute_mean_vectors(prepared_data, model, alphabet, batch_converter, output_file, number_of_layers): 
   
    batch_labels, batch_strs, batch_tokens = batch_converter(prepared_data)
    
    print("Calculating mean vectors")

    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[number_of_layers], return_contacts=True)
    token_representations = results["representations"][number_of_layers]
    
    print("Mean vectors calculated")
    
    print(f"Writing output to {output_file}")
    with open(output_file, 'a') as out_file:
        for i, (name, seq) in enumerate(prepared_data):
            mean_vec = token_representations[i, 1 : len(seq)+1].mean(0).numpy()
            mean_str = str(mean_vec).replace("\n", "")
            out_file.write(f'{name}, {mean_str}\n')
     
    
def main(input_file, output_file, batch_size, model_version):
    start_time = time.time()
    data = format_data(input_file)
    batched_data = batch_data(data, batch_size)
    
    print("Loading models")
    if model_version == "old":
        model, alphabet = torch.hub.load("facebookresearch/esm:main", "esm1b_t33_650M_UR50S") # 1280 dimensions
        number_of_layers = 33
    elif model_version == "new_1280":
        model, alphabet = torch.hub.load("facebookresearch/esm:main", "esm2_t33_650M_UR50D") # 1280 dimensions
        number_of_layers = 33
    else:
        model, alphabet = torch.hub.load("facebookresearch/esm:main", "esm2_t36_3B_UR50D") # 2560 dimensions
        number_of_layers = 36
    
    batch_converter = alphabet.get_batch_converter()
    print("Models loaded")
    
    for batch in batched_data:
        compute_mean_vectors(batch, model, alphabet, batch_converter, output_file, number_of_layers)
    end_time = time.time()
    print("Finished processing")
    print(end_time-start_time)
    

def parse_args():
    parser = argparse.ArgumentParser(
        description="This script will compute an output file that contains protein names alongside their mean vectors."
    )
    parser.add_argument(
        "input_file",
        help="An input file of FASTA format that contains proteins and their sequences.",
    )
    parser.add_argument(
        "--output_file",
        default="./embedding_output.txt",
        help="A file path (absolute or relative) to the desired output file.",
    )
    parser.add_argument(
        "--batch_size",
        help="Number of proteins you want to process together.",
        type=int,
        default="100",
    )
    parser.add_argument(
        "--model",
        help="Which ESM model is being used. Options are 'old', 'new_1280', and 'new_2560'",
        type=str,
        default="new_1280",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    
    args = parse_args()
    main(args.input_file, args.output_file, args.batch_size, args.model)
