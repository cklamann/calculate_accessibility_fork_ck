#!/usr/bin/env python
# coding: utf-8
# Author: Bo Lin, Madeleine Bonsma-Fisher

from functools import reduce
from typing import Dict

from networkx.algorithms.shortest_paths.weighted import (
    single_source_dijkstra_path_length,
)
import numpy as np


# this is modified from the original to speed up calculating multiple destination types
def cal_acc(
    args,
    new_projects,
    new_signals,
    impedence="time",
    potentials=["job", "populations"],
):
    """
    calculate the accessibility of the instance given the selected projects and signals
    :param args:
    :param new_projects: list of project indices for args['projects']
    :param new_signals: list of node IDs to add intersection control
    :return: accessibility
    """
    # retrieve information

    G_curr = args["G_curr"].copy()
    G = args["G"].copy()
    T = args["travel_time_limit"]
    destinations: Dict[np.int64, Dict[np.int64, int | np.float64]] = args[
        "destinations"
    ]
    projs = args["projects"]
    travel_time = args["travel_time"]
    unsig_inters = args["signal_costs"] # currently unsignalized intersections
    # get new edges
    new_edges, new_nodes = [], set([])
    for idx in new_projects:
        new_edges += projs[idx]
        for i, j in projs[idx]:
            new_nodes.add(i)
            new_nodes.add(j)
    # new nodes get added if they were unsignalized and now fall on a low-stress link
    new_nodes = list(new_nodes.intersection(unsig_inters).difference(new_signals))

    for idx in new_signals + new_nodes: # add edges next to identified nodes and new signals
        new_edges += [(i, j) for (i, j) in G.out_edges(idx) if j in destinations]

    # get attributes for new edges
    edges_w_attr = [(i, j, {impedence: travel_time[i, j]}) for (i, j) in new_edges]
    # add new edges
    G_curr.add_edges_from(edges_w_attr)
    # calculate change in accessibility
    acc_by_orig = {}
    for potential in potentials:
        acc_by_orig[potential] = {}
    for orig in destinations:
        lengths: Dict[np.int64, int] = single_source_dijkstra_path_length(
            G=G_curr, source=orig, cutoff=T, weight=impedence
        )

        reachable_des = set(lengths).intersection(set(destinations[orig]))

        for (
            potential
        ) in (
            potentials
        ):  # do multiple destination types here instead of re-solving the lengths every time
            dest_val = args[potential]
            orig_acc = 0
            if reachable_des:
                orig_acc = reduce(
                    lambda acc, curr: acc + dest_val[curr], reachable_des, orig_acc
                )

            acc_by_orig[potential][orig] = orig_acc

    return acc_by_orig
