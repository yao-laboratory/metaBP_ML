# metaBP_ML

## Setting up a Conda Environment 

To setup the conda environment needed to compute the mean vectors, run:

`conda env create -f environment.yml`

(In metaBP-ML, ESM and its model are used. The original codes and models can be found from their GitHub: https://github.com/facebookresearch/esm. The pre-trained model for general purpose "esm1b_t33_650M_UR50S" is used for our embedding work.)

## Creating a job to create mean vectors

Refer to `compute_embeddings.sh` as a bash job to run. 

The general format of the command is: `python compute_bulk_embeddings.py /path/to/input_file.fasta --output_file outfile.txt --batch_size 100 --model new_1280`.
You should adjust the output file name for each job, and batch size can be anything, as long as is it consistent across jobs. The model denotes the ESM model to be used in the embedding process. The current options are 'old', 'new_1280', 'new_2560' with the default being 'new_1280'. Note that increasing the batch size will increase the memory usage. The default batch_size 100 is recommended for most use cases.

## Annotating Sequences
Once the mean vectors have been calculated for the sequences, we can start the process to get annotation information for them. This will be done using the metabp_annotations.py script. 
The general format of the command looks something like this:
```
  python metabp_annotations.py get_annotations -i path/to/mean_vectors_file.txt -o path/to/output_directory -db path/to/peptide_db.pkl -a path/to/annotation_files,path/to/annotation_files -dim 1280
```
This command must be run in the same environment as the command to create the mean vectors. The xml file for this environment can be found in the repository (environment.yml). This environment is named metabp_ml and contains all the necessary packages for the scripts to run without error. The annotation files must be separated by a single comma and no spaces as an argument. The annotation files must correlate with peptides in the peptide database to get proper results. The dimensions should correlate to the number of dimensions for vectors in the mean vectors file and the peptide database file. Any discrepancy will result in errors.

In the testing folder are a database file and an annotation file that can be used to test the functionality of the annotations script.

## MetaBP Annotation Output Files
- vectors.pkl: mean vector pickle file
- index.pkl: faiss index file used in k nearest neighbors search
- knn_output.csv: file containing the id for each sequence, as well as the ids for the 10 nearest neighbors
- distance_output.csv: file containing the id for each sequence, as well the distance to the 10 nearest neighbors
- annotated_sequences.csv: file containing the sequence ids and the annotation information based on nearest neighbors (the taxonomic id, the species, and the EC number)

## Database File Format
Annotating the peptides requires access to a .pkl file of vectorized protein sequences that make up your database. These sequences must be provided to the mean vectorization script in .fasta format and then converted to a .pkl file before the file path is inputed for sequence annotation.
To convert the vectors in pickle file:
```
  python pickle_db.py all_vectors.txt --output_file all_vectors.pkl
```

## Create Annotation Files
To annotate the peptides, you need annotation files. To get these files, you can use the get_annot_from_uniprot.py script. You need an input file as ids that fit UniProt formatting. The general format of the command is: `python get_annot_from_uniprot.py /path/to/input_file.txt --output_file outfile.txt --batch_size 100 --model new_1280`