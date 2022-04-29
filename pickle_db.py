import numpy as np
import pickle
import argparse

def main(input_file, output_file):
    proteins = []
    with open(input_file, "r") as f, open(output_file, "wb") as pick:
        for line in f:
            prot = line.split(",")[0]
            arr = (
                line.split(",")[1]
                .lstrip()
                .replace("[ ", "[")
                .replace(" ]", "]")
                .replace("  ", " ")
                .replace("\n", "")
            )
            seq_arr = np.fromstring(arr.strip("[]"), sep=" ")
            proteins.append((prot, seq_arr))
        pickle.dump(proteins, pick)
        
        
def parse_args():
    parser = argparse.ArgumentParser(
        description="This script takes in the output of compute_bulk_embeddings.py (of format (prot, mean_vector)) and outputs a pkl file.)"
    )
    parser.add_argument(
        "input_file",
        help="An input file of (protein, mean_vector) tuples seperated by newlines.",
    )
    parser.add_argument(
        "--output_file",
        default="./pickle_output.pkl",
        help="A binary output file containing python objects of tuples.",
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    main(args.input_file, args.output_file)
