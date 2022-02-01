# metaBP_ML

## Setting up a Conda Environment 

To setup the conda environment needed to compute the mean vectors, run:

`conda env create -f environment.yml`


## Creating a job

Refer to `compute_embeddings.sh` as a bash job to run. 

The general format of the command is: `python -u compute_bulk_embeddings.py /path/to/input_file.fasta --output-file outfile.txt --batch-size 1000`.
You should adjust the output file name for each job, and batch size can be anything, as long as is it consistent across jobs. 