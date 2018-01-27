import sys

input_nih = sys.argv[1]
input_eval = sys.argv[2]
output_eval = sys.argv[3]

neg_size = 10

node_set = set()
with open(input_nih, "r") as f_in_hin:
    for line in f_in_hin:
        node_1, node_2, _ = line.strip().split()
        node_set.add(node_1)
        node_set.add(node_2)

with open(input_eval, "r") as f_in_eval, open(output_eval, "w") as f_out_eval:
    cur_batch = ""
    cur_validity = True
    for idx, line in enumerate(f_in_eval):
        cur_batch += line
        node_1, node_2, _, __ = line.strip().split()
        if node_1 not in node_set or node_2 not in node_set:
            cur_validity = False

        if idx % (2 * neg_size + 1) == 20:
            if cur_validity is True:
                f_out_eval.write(cur_batch)
            cur_batch = ""
            cur_validity = True
