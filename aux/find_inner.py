import sys
import numpy as np

input_eval = sys.argv[1]
input_emb = sys.argv[2]
output_score = sys.argv[3]


emb_dict={}
with open(input_emb, "r") as f_in:
    num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    count=0
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        emb_dict[line_split[0]] = np.asarray(a)
    assert len(emb_dict) == num_nodes, "Number of nodes does not agree."
print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_emb)

with open(input_eval, "r") as f_in, open(output_score, "w") as f_out:
    for line in f_in:
        node_1, node_2, _, edge_type = line.strip().split()

        cur_score = emb_dict[node_1].dot(emb_dict[node_2])

        f_out.write(" ".join([node_1, node_2, str(cur_score), edge_type])+"\n")