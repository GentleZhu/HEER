import sys
import random

input_hin = sys.argv[1]
input_emb = sys.argv[2]
output_emb = sys.argv[3]

node_set = set()
with open(input_hin, "r") as f_in:
    for line in f_in:
        node_1, node_2, _ = line.strip().split()
        node_set.add(node_1)
        node_set.add(node_2)

with open(input_emb, "r") as f_in, open(output_emb, "w") as f_out:
    first_line_split = f_in.readline().strip().split()
    valid_lines = []
    for line in f_in:
        line_split = line.strip().split()
        if line_split[0] not in node_set:
            continue

        valid_lines.append(line)

    num_nodes = len(valid_lines)
    f_out.write(str(num_nodes) + " " + first_line_split[1] + "\n")
    f_out.writelines(valid_lines)
