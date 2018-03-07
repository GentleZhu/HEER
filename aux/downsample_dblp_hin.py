import sys
import random

input_hin = sys.argv[1]
output_hin = sys.argv[2]

smp_rate = 0.1

paper_set = set()
with open(input_hin, "r") as f_in:
    for line in f_in:
        node_1, node_2, _ = line.strip().split()
        if "P" in node_1:
            paper_set.add(node_1)
        if "P" in node_2:
            paper_set.add(node_2)

remaining_set = set(random.sample(paper_set, int(len(paper_set)*smp_rate)))

with open(input_hin, "r") as f_in, open(output_hin, "w") as f_out:
    for line in f_in:
        node_1, node_2, _ = line.strip().split()
        if ("P" in node_1 and node_1 not in remaining_set) or ("P" in node_2 and node_2 not in remaining_set):
            continue

        f_out.write(line)
