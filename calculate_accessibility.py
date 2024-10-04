# ---
# usage: python calculate_accessibility.py potentials
# example usage: python calculate_accessibility.py job populations
# ---

import numpy as np
import pandas as pd
import os, argparse


from cal_acc_functions import cal_acc, load_file

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Calculate change in accessibility')
    parser.add_argument('potentials', nargs='*', help = 'types of destination accessibility')
    
    args_script = parser.parse_args()
    
    # define parameters
    new_projects = pd.read_csv("data/new_projects.csv")
    potentials = args_script.potentials

    city_wide_model_acc = pd.read_csv("data/city_wide_model_accessibility_results.csv")

    args, _ = load_file("data/args.pkl") # Bo's original
    acc, acc_by_orig = cal_acc(args, list(new_projects['projects']), [], impedence='time', potentials=potentials, by_orig=True)  

    # perhaps we want to give each set of projects an ID and cache the results, that way if someone chooses a set of projects that has been chosen by someone else it can load faster? Way too many possible groupings though...
    
    # export results
    df = city_wide_model_acc[['origin', 'job_original', 'populations_original', 'origin_DA_id']]

    for potential in potentials:
        df['%s_increase' %potential] = df['origin'].map(acc_by_orig[potential])

    df.to_csv("city_wide_model_accessibility_custom_list.csv", index = None)