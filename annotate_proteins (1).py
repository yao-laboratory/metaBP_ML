import pandas as pd
import numpy as np
import sys

def load_db(fps):
    df_list = []
    for i in fps:
        df_list.append(pd.read_csv(i, sep="\t"))
    db_df = pd.concat(df_list)
    db_df = db_df.reset_index()
    db_df = db_df.drop('index', axis=1)
    return db_df

def make_input_df(input_fp):
    input_df = pd.read_csv(input_fp, sep="\t")
    return input_df
    
def find_neighbor_info(nearest_neighbors, db):
    neighbor_ids = nearest_neighbors.values
    neighbor_df = pd.DataFrame(columns = db.columns)
    for i in range(1, len(neighbor_ids)):
        neighbor_row = db[db["protein_id"] == neighbor_ids[i]].copy()
        neighbor_df = pd.concat([neighbor_df, neighbor_row], ignore_index=True)
    return neighbor_df

def find_best_species(neighbor_df):
    tax_num = 0
    tax_col = neighbor_df["tax_id"]
    tax_freq = {}
    for i in tax_col:
        if i in tax_freq.keys():
            tax_freq[i] += 1
        else:
            tax_freq[i] = 1
    most_freq = max(tax_freq, key=tax_freq.get)
    if tax_freq[most_freq] == 1:
        tax_num = tax_col[0]
    else:
        tax_num = most_freq
    spec_info = neighbor_df[neighbor_df["tax_id"] == tax_num]["species"].values
    if len(spec_info) > 0:
        spec_info = spec_info[0]
    else:
        spec_info = np.nan
    return (tax_num, spec_info)

def find_best_ec(neighbor_df):
    ec_num = 0
    ec_col = neighbor_df["EC"]
    ec_freq = {}
    for i in ec_col:
        if i in ec_freq.keys():
            ec_freq[i] += 1
        else:
            ec_freq[i] = 1

    most_freq = max(ec_freq, key=ec_freq.get)
    if ec_freq[most_freq] == 1:
        ec_num = ec_col[0]
    else:
        ec_num = most_freq
        
    if ((type(ec_num) == float) and (len(ec_freq.keys()) > 1)):
        na_vals = ec_col.isnull()
        ec_num = ec_col[na_vals == False].values[0]

    return ec_num

def annotate_proteins(input_df, db):
    prot_ids = []
    tax_nums = []
    spec_info = []
    ec_nums = []
    
    for i in input_df.index:
        row = input_df.loc[i]
        prot_id = row.values[0]
        prot_ids.append(prot_id)
        n_df = find_neighbor_info(row, db)
        tax_num, spec = find_best_species(n_df)
        tax_nums.append(tax_num)
        spec_info.append(spec)
        ec = find_best_ec(n_df)
        ec_nums.append(ec)
    
    annotated = pd.DataFrame()
    annotated["protein_id"] = prot_ids
    annotated["species"] = spec_info
    annotated["tax_id"] = tax_nums
    annotated["EC"] = ec_nums
    
    return annotated

def main(argv):
    db_dir = "/work/yaolab/shared/2022_small_peptide/mitra/db_protid_split/"
    db_fps = [db_dir+"prot_ids1_annot.txt", db_dir+"prot_ids2_annot.txt", db_dir+"prot_ids3_annot.txt", db_dir+"prot_ids4_annot.txt", db_dir+"prot_ids5_annot.txt"]
    db = load_db(db_fps)
    input_df = make_input_df(argv[0])
    annotated = annotate_proteins(input_df, db)    
    path = argv[1]
    annotated.to_csv(path)
    print(path)
    print("Done")

if __name__ == "__main__":
    main(sys.argv[1:])       
