"""
Compute jaccard-like correlation, weighted and unweighted, between each pair of edge types
"""

import argparse
from collections import defaultdict
from random import random
import numpy as np

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input", nargs="?", help="Input HIN filename.", type=str)
parser.add_argument("--output-prefix", nargs="?", help="Output correlation filename prefix.", type=str)
parser.add_argument("--sample-rate", default=1.0, nargs="?", help="Output correlation filename.", type=float)
args = parser.parse_args()

"""
First pass on input file to find normalization factor for each edge type
"""
total_weights_dict = defaultdict(float)
normalization_multipliers_dict = {}
with open(args.input, "r") as f_in:
    for line in f_in:
        attr_node, center_node, weight_str, edge_type = line.strip().split()
        total_weights_dict[edge_type] += float(weight_str)

    for edge_type in total_weights_dict:
        normalization_multipliers_dict[edge_type] = 1./total_weights_dict[edge_type]

"""
Second pass on input file to find egde type set and core center nodes
"""
edge_type_set = set()
center_node_edge_dict = defaultdict(dict)  # {center_node: {edge_type: {attr_node: weight}}}
attr_node_edge_dict = defaultdict(dict)  # {attr_node: {edge_type: {center_node: weight}}}
with open(args.input, "r") as f_in:
    for idx, line in enumerate(f_in):
        attr_node, center_node, weight_str, edge_type = line.strip().split()

        edge_type_set.add(edge_type)
        if edge_type not in center_node_edge_dict[center_node]:
            center_node_edge_dict[center_node][edge_type] = defaultdict(float)
        if edge_type not in attr_node_edge_dict[attr_node]:
            attr_node_edge_dict[attr_node][edge_type] = defaultdict(float)

        center_node_edge_dict[center_node][edge_type][attr_node] += float(weight_str) * normalization_multipliers_dict[edge_type]
        attr_node_edge_dict[attr_node][edge_type][center_node] += float(weight_str) * normalization_multipliers_dict[edge_type]

        if idx % 10000 == 0:
            print "Line %d processed." % idx

edge_type_list = list(edge_type_set)

"""
Third pass on input file to compute measures
"""
for i, edge_type_i in enumerate(edge_type_list):
    for edge_type_j in edge_type_list[i:]:
        num_center_node = len(center_node_edge_dict)
        num_center_node_processed = 0
        weighted_jac_list = []
        unweighted_jac_list = []
        for center_node in center_node_edge_dict:
            if random() > args.sample_rate:
                continue

            path_count_i_dict = defaultdict(float)
            path_count_j_dict = defaultdict(float)

            if (edge_type_i not in center_node_edge_dict[center_node]) or (edge_type_j not in center_node_edge_dict[center_node]):
                continue

            for attr_node_i in center_node_edge_dict[center_node][edge_type_i]:
                cur_weight = center_node_edge_dict[center_node][edge_type_i][attr_node_i]
                for linked_center_node in attr_node_edge_dict[attr_node_i][edge_type_i]:
                    if linked_center_node == center_node:  # do not consider itself
                        continue
                    path_count_i_dict[linked_center_node] += attr_node_edge_dict[attr_node_i][edge_type_i][linked_center_node] * cur_weight

            for attr_node_j in center_node_edge_dict[center_node][edge_type_j]:
                cur_weight = center_node_edge_dict[center_node][edge_type_j][attr_node_j]
                for linked_center_node in attr_node_edge_dict[attr_node_j][edge_type_j]:
                    if linked_center_node == center_node:  # do not consider itself
                        continue
                    path_count_j_dict[linked_center_node] += attr_node_edge_dict[attr_node_j][edge_type_j][linked_center_node] * cur_weight

            linked_center_node_union_set = set(path_count_i_dict) | set(path_count_j_dict)
            if len(linked_center_node_union_set) == 0:
                continue

            weighted_numerator = 0.
            weighted_denominator = 0.
            unweighted_numerator = 0.
            unweighted_denominator = 0.
            for linked_center_node in linked_center_node_union_set:
                cur_path_count_i = path_count_i_dict[linked_center_node]
                cur_path_count_j = path_count_j_dict[linked_center_node]
                assert cur_path_count_i > 0 or cur_path_count_j > 0.
                weighted_numerator += min(cur_path_count_i, cur_path_count_j)
                weighted_denominator += max(cur_path_count_i, cur_path_count_j)
                unweighted_numerator += 1. if min(cur_path_count_i, cur_path_count_j) > 0. else 0.
                unweighted_denominator += 1.

            weighted_jac_list.append(weighted_numerator/(1.*weighted_denominator))
            unweighted_jac_list.append(unweighted_numerator/(1.*unweighted_denominator))

            num_center_node_processed += 1

            if num_center_node_processed % 1000 == 0:
                print "%d out of %d * %f center nodes processed for edge type pair %s and %s" % (num_center_node_processed, num_center_node, args.sample_rate, edge_type_i, edge_type_j)

        np.savez(args.output_prefix+"_"+edge_type_i+"_"+edge_type_j+".npz",
                 weighted=np.asarray(weighted_jac_list), unweighted=np.asarray(unweighted_jac_list))
