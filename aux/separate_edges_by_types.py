import os
import argparse

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input-file", nargs="?", help="Input query filename.", type=str)
parser.add_argument("--output-dir", nargs="?", help="Directory for output.", type=str)
args = parser.parse_args()

input_file = args.input_file
output_dir = args.output_dir

f_out_dict = {}
with open(input_file, "r") as f_in:
    f_in.readline()  # ignore the first line used for sanity check: num of neg smp & num of eval batches
    for line in f_in:
        _, __, ___, edge_type = line.strip().split()

        if edge_type not in f_out_dict:
            cur_output_file_name = os.path.join(output_dir, edge_type+"_"+os.path.basename(input_file))
            f_out_dict[edge_type] = open(cur_output_file_name, "w")

        f_out_dict[edge_type].write(line)

for edge_type in f_out_dict:
    f_out_dict[edge_type].close()