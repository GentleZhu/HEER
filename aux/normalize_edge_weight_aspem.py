import sys
from collections import defaultdict

aspect = sys.argv[1]
knockout_rate = sys.argv[2]
input_hin = "../input_data/dblp_" + knockout_rate + "_out_for_aspem_" + aspect + ".net"
output_hin = "../input_data/dblp_" + knockout_rate + "_out_for_aspem_" + aspect + "_normalized.net"

total_weight_dict = defaultdict(float)
with open(input_hin, "r") as f_in:
    for line in f_in:
        node_1, node_2, weight_str = line.strip().split()
        weight = float(weight_str)
        edge_type = node_1[0] + node_2[0]
        total_weight_dict[edge_type] += weight

max_total_weight = max(total_weight_dict.values())

with open(input_hin, "r") as f_in, open(output_hin, "w") as f_out:
    for line in f_in:
        node_1, node_2, weight_str = line.strip().split()
        weight = float(weight_str)
        edge_type = node_1[0] + node_2[0]
        f_out.write(" ".join([node_1, node_2, str(weight * max_total_weight / total_weight_dict[edge_type])]) + "\n")
