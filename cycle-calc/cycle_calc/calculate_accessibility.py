# ---
# usage: python calculate_accessibility.py potentials
# example usage: python calculate_accessibility.py job populations
# ---

import argparse
import pickle
from typing import Dict, List

import numpy as np
import pandas as pd

from cycle_calc.cal_acc_functions import cal_acc


def main(project_ids: List[int], potentials: List[str]) -> Dict[str, List[np.int64]]:
    """
    Calculate the accessibility scores for the network of projects

        Parameters

        project_ids : the projects to calculate the scores for
        potentials : the metrics (currently "job" and "populations")

        Returns

        Dict[str, np.int64] : A dictionary with a row for each DA and a column for each potential

    """

    with open("./data/args.pkl", "rb") as f:
        args = pickle.load(f)

    _, acc_by_orig = cal_acc(
        args,
        project_ids,
        [],
        impedence="time",
        potentials=potentials,
        by_orig=True,
    )

    return acc_by_orig


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Calculate change in accessibility")
    parser.add_argument(
        "--potentials",
        type=str,
        default="job",
        help="types of destination accessibility",
    )
    parser.add_argument(
        "--projects_path",
        type=str,
        help="path to project csv",
        default="./data/new_projects.csv",
    )

    args_script = parser.parse_args()

    new_projects = list(pd.read_csv(args_script.projects_path)["projects"])
    # define parameters
    potentials = args_script.potentials.split(",")

    # perhaps we want to give each set of projects an ID and cache the results, that way if someone chooses a set of projects that has been chosen by someone else it can load faster? Way too many possible groupings though...
    city_wide_model_acc = pd.read_csv("data/city_wide_model_accessibility_results.csv")

    # export results
    df = city_wide_model_acc[
        ["origin", "job_original", "populations_original", "origin_DA_id"]
    ]

    acc_by_orig = main(new_projects, potentials)

    for potential in potentials:
        df["%s_increase" % potential] = df["origin"].map(acc_by_orig[potential])

    df.to_csv("./data/city_wide_model_accessibility_custom_list.csv", index=None)
