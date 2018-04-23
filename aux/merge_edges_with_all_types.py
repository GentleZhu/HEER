import os
import argparse

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input-ref-file", nargs="?", help="Input query filename.", type=str)
parser.add_argument("--input-score-dir", nargs="?", help="Directory for score files.", type=str)
parser.add_argument("--input-score-keywords", nargs="?", help="Keyword contained by score files.", type=str)
parser.add_argument("--output-file", nargs="?", help="Directory for output.", type=str)
args = parser.parse_args()

input_ref_file = args.input_ref_file
input_score_dir = args.input_score_dir
input_score_keywords = args.input_score_keywords
output_file = args.output_file

typed_node_pair_to_line_dict = {}
# repeat for each file in the directory
for input_score_file_basename in os.listdir(input_score_dir):
   # apply file type filter
   if input_score_keywords in input_score_file_basename:
       with open(os.path.join(input_score_dir, input_score_file_basename), "r") as f_in_score:
           for line in f_in_score:
               line_split = line.strip().split()
               typed_node_pair = "|".join([line_split[0],line_split[1],line_split[3]])
               typed_node_pair_to_line_dict[typed_node_pair] = line

with open(input_ref_file, "r") as f_in, open(output_file, "w") as f_out:
    f_out.write(f_in.readline())  # copy the first line used for sanity check: num of neg smp & num of eval batches
    for line in f_in:
        line_split = line.strip().split()
        typed_node_pair = "|".join([line_split[0],line_split[1],line_split[3]])

        assert typed_node_pair in typed_node_pair_to_line_dict, "%s not in score files." % typed_node_pair
        f_out.write(typed_node_pair_to_line_dict[typed_node_pair])
