import os
import argparse
import random

def len_file(input_file):
    with open(input_file) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input-file", nargs="?", help="Input evaluation filename.", type=str)
parser.add_argument("--output-file", nargs="?", help="Output downsampled evaluation filename.", type=str)
#parser.add_argument('--sample-rate', nargs="?", type=float, default=0.1, help="Sample rate, default 0.1.")
parser.add_argument('--sample-number', nargs="?", type=int, default=4000000,
                    help="Sample number to approximate, inc. both pos and neg, 4000000.")
parser.add_argument('--neg-size', nargs="?", type=int, default=10, help="Negative pairs for each positive pair in one direction, default 10.")
args = parser.parse_args()

input_eval = args.input_file
output_eval = args.output_file
neg_size = args.neg_size
sample_number = args.sample_number

input_eval_file_len = len_file(input_eval)
smp_rate = 1.*sample_number/input_eval_file_len

with open(input_eval, "r") as f_in_eval, open(output_eval, "w") as f_out_eval:
    f_out_eval.write(f_in_eval.readline())
    cur_batch = ""
    for idx, line in enumerate(f_in_eval):
        cur_batch += line
        if (idx + 1) % (2 * neg_size + 1) == 0:
            if random.random() < smp_rate:
                f_out_eval.write(cur_batch)
            cur_batch = ""
