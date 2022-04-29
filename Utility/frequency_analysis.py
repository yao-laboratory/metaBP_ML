import pandas as pd
import numpy as np

def get_ec_frequency(annotations_fp, outputfp):
    df = pd.read_csv(annotations_fp, low_memory=False)
    ec_na = df["EC"].isnull()
    ec_m = df[ec_na == False]["EC"]
    ec_freq = pd.DataFrame(ec_m.value_counts())
    ec_freq = ec_freq.reset_index()
    ec_freq.columns=["EC", "frequency"]
    ec_freq.to_csv(outputfp)
    return outputfp

def get_taxid_frequency(annotations_fp, outputfp):
    df = pd.read_csv(annotations_fp, low_memory=False)
    tax_na = df["tax_id"].isnull()
    tax_m = df[tax_na == False]["tax_id"]
    tax_df = pd.DataFrame(data=[tax_m])
    tax_df = tax_df.transpose()
    tax_df.columns = ["tax_id"]
    freq_vals = pd.DataFrame(tax_df["tax_id"].value_counts())
    freq_vals = freq_vals.reset_index()
    freq_vals.columns = ["tax_id", "frequency"]
    freq_vals.to_csv(outputfp)
    return outputfp