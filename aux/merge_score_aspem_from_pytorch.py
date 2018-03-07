import sys
import numpy as np

input_eval = sys.argv[1]
input_emb_1 = sys.argv[2]
input_emb_2 = sys.argv[3]
output_prefix = sys.argv[4]

output_1_score = output_prefix + "_1_score.txt"
output_2_score = output_prefix + "_2_score.txt"
output_mean_score = output_prefix + "_avg_score.txt"

output_1_score_first_half = output_prefix + "_1_score_first_half.txt"
output_2_score_first_half = output_prefix + "_2_score_first_half.txt"
output_mean_score_first_half = output_prefix + "_avg_score_first_half.txt"

output_1_score_second_half = output_prefix + "_1_score_second_half.txt"
output_2_score_second_half = output_prefix + "_2_score_second_half.txt"
output_mean_score_second_half = output_prefix + "_avg_score_second_half.txt"

emb_1_dict={}
with open(input_emb_1, "r") as f_in:
    #num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        emb_1_dict[line_split[0]] = np.asarray(a)
        dim = len(a)
    #assert len(emb_1_dict) == num_nodes, "Number of nodes does not agree."
print ("Embedding loading done.", len(emb_1_dict), "nodes with dim", dim, "from", input_emb_1)

emb_2_dict={}
with open(input_emb_2, "r") as f_in:
    #num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        emb_2_dict[line_split[0]] = np.asarray(a)
        dim = len(a)
    #assert len(emb_2_dict) == num_nodes, "Number of nodes does not agree."
print ("Embedding loading done.", len(emb_2_dict), "nodes with dim", dim, "from", input_emb_2)

assert dim % 2 == 0
half_dim = int(dim) / 2

with open(input_eval, "r") as f_in, \
        open(output_mean_score, "w") as f_out_mean, open(output_1_score, "w") as f_out_1, open(output_2_score, "w") as f_out_2, \
        open(output_mean_score_first_half, "w") as f_out_mean_first_half, open(output_1_score_first_half, "w") as f_out_1_first_half, \
        open(output_2_score_first_half, "w") as f_out_2_first_half, \
        open(output_mean_score_second_half, "w") as f_out_mean_second_half, open(output_1_score_second_half, "w") as f_out_1_second_half, open(output_2_score_second_half, "w") as f_out_2_second_half:
    num_line_not_found = 0
    for line in f_in:
        node_1, node_2, _, edge_type = line.strip().split()
        cur_1_score = None
        cur_2_score = None
        cur_avg_score = None

        if node_1 in emb_1_dict and node_2 in emb_1_dict:
            cur_1_score = emb_1_dict[node_1].dot(emb_1_dict[node_2])
            cur_1_score_first_half = (emb_1_dict[node_1][:half_dim]).dot(emb_1_dict[node_2][:half_dim])
            cur_1_score_second_half = (emb_1_dict[node_1][half_dim:]).dot(emb_1_dict[node_2][half_dim:])
        if node_1 in emb_2_dict and node_2 in emb_2_dict:
            cur_2_score = emb_2_dict[node_1].dot(emb_2_dict[node_2])
            cur_2_score_first_half = (emb_2_dict[node_1][:half_dim]).dot(emb_2_dict[node_2][:half_dim])
            cur_2_score_second_half = (emb_2_dict[node_1][half_dim:]).dot(emb_2_dict[node_2][half_dim:])
        if (cur_1_score is not None) and (cur_2_score is not None):
            cur_avg_score = (cur_1_score + cur_2_score) / 2.
            cur_avg_score_first_half = (cur_1_score_first_half + cur_2_score_first_half) / 2.
            cur_avg_score_second_half = (cur_1_score_second_half + cur_2_score_second_half) / 2.

        if cur_avg_score is not None:  # P-A
            f_out_mean.write(" ".join([node_1, node_2, str(cur_avg_score), edge_type]) + "\n")
            f_out_1.write(" ".join([node_1, node_2, str(cur_1_score), edge_type]) + "\n")
            f_out_2.write(" ".join([node_1, node_2, str(cur_2_score), edge_type]) + "\n")
            f_out_mean_first_half.write(" ".join([node_1, node_2, str(cur_avg_score_first_half), edge_type]) + "\n")
            f_out_1_first_half.write(" ".join([node_1, node_2, str(cur_1_score_first_half), edge_type]) + "\n")
            f_out_2_first_half.write(" ".join([node_1, node_2, str(cur_2_score_first_half), edge_type]) + "\n")
            f_out_mean_second_half.write(" ".join([node_1, node_2, str(cur_avg_score_second_half), edge_type]) + "\n")
            f_out_1_second_half.write(" ".join([node_1, node_2, str(cur_1_score_second_half), edge_type]) + "\n")
            f_out_2_second_half.write(" ".join([node_1, node_2, str(cur_2_score_second_half), edge_type]) + "\n")
        elif cur_1_score is not None:  # P-Y
            f_out_mean.write(" ".join([node_1, node_2, str(cur_1_score), edge_type]) + "\n")
            f_out_1.write(" ".join([node_1, node_2, str(cur_1_score), edge_type]) + "\n")
            f_out_2.write(" ".join([node_1, node_2, str(cur_1_score), edge_type]) + "\n")
            f_out_mean_first_half.write(" ".join([node_1, node_2, str(cur_1_score_first_half), edge_type]) + "\n")
            f_out_1_first_half.write(" ".join([node_1, node_2, str(cur_1_score_first_half), edge_type]) + "\n")
            f_out_2_first_half.write(" ".join([node_1, node_2, str(cur_1_score_first_half), edge_type]) + "\n")
            f_out_mean_second_half.write(" ".join([node_1, node_2, str(cur_1_score_second_half), edge_type]) + "\n")
            f_out_1_second_half.write(" ".join([node_1, node_2, str(cur_1_score_second_half), edge_type]) + "\n")
            f_out_2_second_half.write(" ".join([node_1, node_2, str(cur_1_score_second_half), edge_type]) + "\n")
        elif cur_2_score is not None:  # P-P, P-V, P-W
            f_out_mean.write(" ".join([node_1, node_2, str(cur_2_score), edge_type]) + "\n")
            f_out_1.write(" ".join([node_1, node_2, str(cur_2_score), edge_type]) + "\n")
            f_out_2.write(" ".join([node_1, node_2, str(cur_2_score), edge_type]) + "\n")
            f_out_mean_first_half.write(" ".join([node_1, node_2, str(cur_2_score_first_half), edge_type]) + "\n")
            f_out_1_first_half.write(" ".join([node_1, node_2, str(cur_2_score_first_half), edge_type]) + "\n")
            f_out_2_first_half.write(" ".join([node_1, node_2, str(cur_2_score_first_half), edge_type]) + "\n")
            f_out_mean_second_half.write(" ".join([node_1, node_2, str(cur_2_score_second_half), edge_type]) + "\n")
            f_out_1_second_half.write(" ".join([node_1, node_2, str(cur_2_score_second_half), edge_type]) + "\n")
            f_out_2_second_half.write(" ".join([node_1, node_2, str(cur_2_score_second_half), edge_type]) + "\n")
        else:
            print "Line not found: " + line
            num_line_not_found += 1
            f_out_mean.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_1.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_2.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_mean_first_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_1_first_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_2_first_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_mean_second_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_1_second_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            f_out_2_second_half.write(" ".join([node_1, node_2, str(0.), edge_type])+"\n")
            #raise Exception("Node missing. " + node_1 + "|" + node_2)
    print "Number of lines not found:", num_line_not_found