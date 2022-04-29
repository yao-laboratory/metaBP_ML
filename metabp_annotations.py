import argparse
import os

def get_annotations(mean_vector_fp, output_fp):
    pkl_outfp = output_fp + "/vectors.pkl"
    pickle_vectors = "python pickle_db.py -u "+mean_vector_fp+" --output_file "+pkl_outputfp
    os.system(pickle_vectors)
    knn_fp = output_fp + "/knn_output.csv"
    knn_str = "python -u knn_from_pickle.py "+pickle_outfp+" --output_file "+knn_fp+" --nodes 4"
    os.system(knn_str)
    annotation_fp = output_fp + "/annotated_sequences.csv"
    annotation_str = "python annotate_proteins.py "+knn_fp+" "+annotation_fp
    os.system(annotation_str)
    
def main():
    parser = argparse.ArgumentParser(
        prog="metabp_annotation",
        description="this method executes the protein-based annotation pipeline.",
    )
    subparser = parser.add_subparsers(
        dest="method",
        help="enter the the filepath for file containing the mean vectors for the sequences and the name for the output directory.",
    )

    mutation_id_parser = subparser.add_parser(
        "get_annotations",
        help="this method takes in the mean vectors and returns the sequence ids along with annotations.",
    )
    mutation_id_parser.add_argument(
        "-i",
        dest="mean_vector_fp",
        type=str,
        help="the file path of the mean vectors of the sequences to be annotated",
    )
    mutation_id_parser.add_argument(
        "-o", dest="output_file_path", type=str, help="file path for the output directory"
    )
    
    arguments = parser.parse_args()

    if arguments.method == "metabp_annotation":
        mean_vector_fp = arguments.mean_vectorfp
        output_file_path = arguments.output_file_path
        
        # call function
        get_annotations(mean_vector_fp, output_fp)
    else:
        print("Incorrect input, please check parameters and try again")
        
if __name__ == "__main__":
    main()