#!/bin/bash
#SBATCH --time=12:00:00          # Run time in hh:mm:ss
#SBATCH --mem=64000       # Maximum memory required per CPU (in megabytes)
#SBATCH --job-name=embed_ten_thousand
#SBATCH --error=/work/yaolab/bjohnson/esm/embedding.%J.err
#SBATCH --output=/work/yaolab/bjohnson/esm/embedding.%J.out
#SBATCH --partition=yaolab,batch

module load anaconda
conda activate $HOME/.conda/envs/metabp_ml

date

python -u compute_bulk_embeddings.py /work/yaolab/bjohnson/data/tens_of_proteins.fasta

date
conda deactivate
