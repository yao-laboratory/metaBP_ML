#!/bin/bash
#SBATCH --time=7-00:00:00          # Run time in hh:mm:ss
#SBATCH --mem=64000       # Maximum memory required per CPU (in megabytes)
#SBATCH --job-name=embed_proteins
#SBATCH --error=/path/to/file.err
#SBATCH --output=/path/to/file.out
#SBATCH --partition=yaolab,batch

module load anaconda
conda activate $HOME/.conda/envs/metabp_ml

date

python -u compute_bulk_embeddings.py /path/to/input-file.fasta --output_file /path/to/output-file.txt --batch-size 100 

date
conda deactivate
