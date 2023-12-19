import argparse
import os
import subprocess
import time

def get_annotations(mean_vector_fp, output_fp, db_fp, annotation_paths, dimensions):
    start_time = time.time()
    pkl_output_fp = output_fp + "/vectors.pkl"
    pickle_vectors = "python pickle_db.py "+mean_vector_fp+" --output_file "+pkl_output_fp
    os.system(pickle_vectors)
    knn_fp = output_fp + "/knn_output.csv"
    knn_str = "python -u knn_from_pickle.py "+pkl_output_fp+" --output_fp "+output_fp+" --nodes 4 --db "+db_fp+" --dim "+str(dimensions)
    os.system(knn_str)
    annotation_fp = output_fp + "/annotated_sequences.csv"
    annotation_str = "python annotate_proteins.py "+knn_fp+" "+annotation_fp+" "+annotation_paths
    os.system(annotation_str)
    end_time = time.time()
    print("get_annotations script took " + str(end_time-start_time) + " to finish")
    
def main():
    parser = argparse.ArgumentParser(
        prog="metabp_annotation",
        description="this method executes the protein-based annotation pipeline.",
    )
    subparser = parser.add_subparsers(
        dest="method",
        help="enter the the filepath for file containing the mean vectors for the sequences and the name for the output directory.",
    )

    annotation_parser = subparser.add_parser(
        "get_annotations",
        help="this method takes in the mean vectors and returns the sequence ids along with annotations.",
    )
    annotation_parser.add_argument(
        "-i",
        dest="mean_vector_fp",
        type=str,
        help="the file path of the mean vectors of the sequences to be annotated",
    )
    annotation_parser.add_argument(
        "-o", dest="output_file_path", type=str, help="file path for the output directory"
    )
    annotation_parser.add_argument(
        "-db", dest="db_path",
        help="A path to the .pkl file for the peptide database",
    )
    annotation_parser.add_argument(
        "-a",
        dest="annotation_paths",
        type=str,
        help="The paths to the annotation .txt files that match the peptide database, separated with commas",
    )
    annotation_parser.add_argument(
        "-dim",
        dest="dimensions",
        type=int,
        help="The number of dimensions by the ESM model. Determines which ESM model is used. Options are 1280 and 2560",
        default=1280
    )
    arguments = parser.parse_args()

    if arguments.method == "get_annotations":
        mean_vector_fp = arguments.mean_vector_fp
        output_fp = arguments.output_file_path
        db_path = arguments.db_path
        annotation_paths = arguments.annotation_paths
        dimensions = arguments.dimensions
        # call function
        get_annotations(mean_vector_fp, output_fp, db_path, annotation_paths, dimensions)
    else:
        print("Incorrect input, please check parameters and try again")
        
if __name__ == "__main__":
    main()
