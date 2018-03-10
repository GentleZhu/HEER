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

lines_to_write = []
with open(input_eval, "r") as f_in_eval, open(output_eval, "w") as f_out_eval:
    first_line = f_in_eval.readline()
    lines_to_write.append(first_line)  # the number of batches is to be updated

    neg_size_from_file, num_batches_from_file = map(int, first_line.strip().split())
    assert neg_size == neg_size_from_file

    new_num_batches = 0
    cur_batch = ""
    for idx, line in enumerate(f_in_eval):
        cur_batch += line
        if (idx + 1) % (2 * neg_size + 1) == 0:
            if random.random() < smp_rate:
                lines_to_write.append(cur_batch)
                new_num_batches += 1
            cur_batch = ""
    assert (idx + 1)/(2*neg_size + 1) == num_batches_from_file, "Number of positive edges does not agree."

    lines_to_write[0] = str(neg_size) + " " + str(new_num_batches) + "\n"
    f_out_eval.writelines(lines_to_write)
