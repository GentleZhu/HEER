import sys
import numpy as np

input_eval = "../input_data/dblp_0.2_out_20neg_eval_fast.txt"
input_emb_pay = sys.argv[1]
input_emb_papvw = sys.argv[2]
output_prefix = sys.argv[3]

output_pay_score = output_prefix + "_pay_score.txt"
output_papvw_score = output_prefix + "_papvw_score.txt"
output_mean_score = output_prefix + "_mean_score.txt"

emb_pay_dict={}
with open(input_emb_pay, "r") as f_in:
    num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    count=0
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        emb_pay_dict[line_split[0]] = np.asarray(a)
    assert len(emb_pay_dict) == num_nodes, "Number of nodes does not agree."
print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_emb_pay)

emb_papvw_dict={}
with open(input_emb_papvw, "r") as f_in:
    num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    count=0
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        emb_papvw_dict[line_split[0]] = np.asarray(a)
    assert len(emb_papvw_dict) == num_nodes, "Number of nodes does not agree."
print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_emb_papvw)

with open(input_eval, "r") as f_in, open(output_mean_score, "w") as f_out_mean, \
        open(output_pay_score, "w") as f_out_pay, open(output_papvw_score, "w") as f_out_papvw:
    num_line_not_found = 0
    for line in f_in:
        node_1, node_2, _, edge_type = line.strip().split()
        cur_pay_score = None
        cur_papvw_score = None
        cur_mean_score = None

        if node_1 in emb_pay_dict and node_2 in emb_pay_dict and ("P" not in node_1 or "P" not in node_2):
            cur_pay_score = emb_pay_dict[node_1].dot(emb_pay_dict[node_2])
        if node_1 in emb_papvw_dict and node_2 in emb_papvw_dict:
            cur_papvw_score = emb_papvw_dict[node_1].dot(emb_papvw_dict[node_2])
        if (cur_pay_score is not None) and (cur_papvw_score is not None):
            cur_mean_score = (cur_pay_score + cur_papvw_score)/2.

        if cur_mean_score is not None:  # P-A
            f_out_mean.write(" ".join([node_1, node_2, str(cur_mean_score), edge_type])+"\n")
            f_out_pay.write(" ".join([node_1, node_2, str(cur_pay_score), edge_type])+"\n")
            f_out_papvw.write(" ".join([node_1, node_2, str(cur_papvw_score), edge_type])+"\n")
        elif cur_pay_score is not None:  # P-Y
            f_out_mean.write(" ".join([node_1, node_2, str(cur_pay_score), edge_type])+"\n")
            f_out_pay.write(" ".join([node_1, node_2, str(cur_pay_score), edge_type])+"\n")
            f_out_papvw.write(" ".join([node_1, node_2, str(cur_pay_score), edge_type])+"\n")
        elif cur_papvw_score is not None:  # P-P, P-V, P-W
            f_out_mean.write(" ".join([node_1, node_2, str(cur_papvw_score), edge_type])+"\n")
            f_out_pay.write(" ".join([node_1, node_2, str(cur_papvw_score), edge_type])+"\n")
            f_out_papvw.write(" ".join([node_1, node_2, str(cur_papvw_score), edge_type])+"\n")
        else:
            print "Line not found: " + line
            num_line_not_found += 1
            f_out_mean.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_pay.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_papvw.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
    print "Number of lines not found:", num_line_not_found