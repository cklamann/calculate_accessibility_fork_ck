# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import numpy as np
import pandas as pd
import os

from cal_acc_functions import cal_acc, load_file

city_wide_model_acc = pd.read_csv("data/city_wide_model_accessibility_results.csv")

args, _ = load_file("data/args.pkl") # Bo's original

potentials = ['job', 'populations'] # what are the destination types we have available?

# test project set - 10 km city-wide budget, from seed 38
new_projects = [76,
 79,
 147,
 161,
 227,
 333,
 334,
 377,
 414,
 724,
 785,
 837,
 901,
 1073,
 1162,
 1242,
 1247,
 1279]

acc, acc_by_orig = cal_acc(args, new_projects, [], impedence='time', potentials=potentials, by_orig=True)  

# +
# perhaps we want to give each set of projects an ID and cache the results, that way if someone chooses a set of projects that has been chosen by someone else it can load faster? Way too many possible groupings though...

# +
df = city_wide_model_acc[['origin', 'job_original', 'pop_original', 'origin_DA_id']]

for potential in potentials:
    df['%s_increase' %potential] = df['origin'].map(acc_by_orig[potential])
    
df.to_csv("city_wide_model_accessibility_custom_list.csv", index = None)
# -

df


