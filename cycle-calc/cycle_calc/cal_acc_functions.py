#!/usr/bin/env python
# coding: utf-8
# Author: Bo Lin, Madeleine Bonsma-Fisher

import pandas as pd
import os, pickle
from tqdm import tqdm
from networkx.algorithms.shortest_paths.weighted import (
    single_source_dijkstra_path_length,
)


# this is modified from the original to speed up calculating multiple destination types
def cal_acc(
    args,
    new_projects,
    new_signals,
    impedence="time",
    potentials=["job", "populations"],
    by_orig=True,
):
    """
    calculate the accessibility of the instance given the selected projects and signals
    :param args:
    :param new_projects: list of project indices for args['projects']
    :param new_signals:
    :return: accessibility
    """
    # retrieve information
    G_curr = args["G_curr"].copy()
    G = args["G"].copy()
    T = args["travel_time_limit"]
    destinations = args["destinations"]
    projs = args["projects"]
    travel_time = args["travel_time"]
    unsig_inters = args["signal_costs"]
    # get new edges
    new_edges, new_nodes = [], set([])
    for idx in new_projects:
        new_edges += projs[idx]
        for i, j in projs[idx]:
            new_nodes.add(i)
            new_nodes.add(j)
    # new nodes get added if they were unsignalized and now fall on a low-stress link
    new_nodes = [
        idx for idx in new_nodes if idx in unsig_inters and idx not in new_signals
    ]
    for idx in new_signals + new_nodes:
        new_edges += [(i, j) for (i, j) in G.out_edges(idx) if j in destinations]
    # get attributes for new edges
    edges_w_attr = [(i, j, {impedence: travel_time[i, j]}) for (i, j) in new_edges]
    # add new edges
    G_curr.add_edges_from(edges_w_attr)
    # calculate change in accessibility
    acc = {}
    acc_by_orig = {}
    for potential in potentials:
        acc[potential] = 0
        acc_by_orig[potential] = {}
    for orig in tqdm(destinations):
        lengths = single_source_dijkstra_path_length(
            G=G_curr, source=orig, cutoff=T, weight=impedence
        )
        reachable_des = [des for des in lengths if des in destinations[orig]]
        for (
            potential
        ) in (
            potentials
        ):  # do multiple destination types here instead of re-solving the lengths every time
            dest_val = args[potential]
            orig_acc = 0
            for des in reachable_des:
                acc[potential] += dest_val[des]
                orig_acc += dest_val[des]
            acc_by_orig[potential][orig] = orig_acc
    if by_orig:
        return acc, acc_by_orig
    return acc


def load_file(path):
    if os.path.exists(path):
        if path[-4:] == ".csv":
            file = pd.read_csv(path)
        else:
            with open(path, "rb") as f:
                file = pickle.load(f)
                f.close()
        return file, True
    else:
        return None, False
