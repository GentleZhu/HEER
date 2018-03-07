# the negative generation methods are approximate
import argparse
import random

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input-eval", nargs="?", help="Input evaluation filename.", type=str)
parser.add_argument("--input-hin", nargs="?", help="Input HIN filename.", type=str)
parser.add_argument("--output-file", nargs="?", help="Output matched evaluation filename.", type=str)
parser.add_argument('--neg-size', nargs="?", type=int, default=10, help="Negative pairs for each positive pair in one direction, default 10.")
args = parser.parse_args()

input_eval = args.input_eval
input_hin = args.input_hin
output_eval = args.output_file
neg_size = args.neg_size

threshold_for_valid_neg = 2

node_set = set()
with open(input_hin, "r") as f_in_hin:
    for line in f_in_hin:
        node_1, node_2, _ = line.strip().split()
        node_set.add(node_1)
        node_set.add(node_2)

with open(input_eval, "r") as f_in_eval, open(output_eval, "w") as f_out_eval:
    for idx, line in enumerate(f_in_eval):
        if idx % (2 * neg_size + 1) == 0:
            neg_left_line_list = []
            neg_right_line_list = []

            pos_line = line
            node_1, node_2, _, __ = line.strip().split()
            if node_1 not in node_set or node_2 not in node_set:
                pos_line_keep = False
            else:
                pos_line_keep = True
        elif 0 < idx % (2 * neg_size + 1) <= neg_size: # neg_left
            node_1, node_2, _, __ = line.strip().split()
            if node_1 in node_set and node_2 in node_set:
                neg_left_line_list.append(line)
        elif neg_size < idx % (2 * neg_size + 1) <= 2*neg_size: # neg_right
            node_1, node_2, _, __ = line.strip().split()
            if node_1 in node_set and node_2 in node_set:
                neg_right_line_list.append(line)
        else:
            raise Exception("Wrong index.")

        if idx % (2 * neg_size + 1) == 2*neg_size: # on end of block
            # continue is the pos in this bag is invalid
            if pos_line_keep is False:
                continue

            # continue if either left or right is invalid
            if len(neg_left_line_list) < threshold_for_valid_neg or len(neg_right_line_list) < threshold_for_valid_neg:
                continue

            len_neg_left = len(neg_left_line_list)
            new_neg_left_line_list = neg_left_line_list * int(neg_size/len_neg_left) + neg_left_line_list[:neg_size%len_neg_left]

            len_neg_right = len(neg_right_line_list)
            new_neg_right_line_list = neg_right_line_list * int(neg_size/len_neg_right) + neg_right_line_list[:neg_size%len_neg_right]

            f_out_eval.write(pos_line)
            f_out_eval.writelines(new_neg_left_line_list)
            f_out_eval.writelines(new_neg_right_line_list)

