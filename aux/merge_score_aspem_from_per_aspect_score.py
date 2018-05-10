import sys
import numpy as np

input_eval = sys.argv[1]
input_score_1 = sys.argv[2]
input_score_2 = sys.argv[3]
output_score = sys.argv[4]

score_1_dict={}
with open(input_score_1, "r") as f_in:
    f_in.readline()
    for line in f_in:
        node_1, node_2, score, edge_type = line.strip().split()
        score_1_dict[(node_1, node_2, edge_type)] = float(score)

print ("Score from the first aspect loading done.")

score_2_dict={}
with open(input_score_2, "r") as f_in:
    f_in.readline()
    for line in f_in:
        node_1, node_2, score, edge_type = line.strip().split()
        score_2_dict[(node_1, node_2, edge_type)] = float(score)

print ("Score from the second aspect loading done.")

with open(input_eval, "r") as f_in, open(output_score, "w") as f_out:
    num_line_not_found = 0
    f_out.write(f_in.readline())
    for line in f_in:
        node_1, node_2, _, edge_type = line.strip().split()
        cur_score_list = []

        if (node_1, node_2, edge_type) in score_1_dict:
            cur_score_list.append(score_1_dict[(node_1, node_2, edge_type)])
        if (node_1, node_2, edge_type) in score_2_dict:
            cur_score_list.append(score_2_dict[(node_1, node_2, edge_type)])

        if not cur_score_list:
            num_line_not_found += 1
            cur_score_list.append(0.5)

        avg_score = np.mean(cur_score_list)

        f_out.write(" ".join([node_1, node_2, str(avg_score), edge_type]) + "\n")

    print "Number of lines not found:", num_line_not_found