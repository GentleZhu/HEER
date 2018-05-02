import sys

input_file_aspect = sys.argv[1]
input_file_hin = sys.argv[2]
output_file_hin = sys.argv[3]
input_file_eval = sys.argv[4]
output_file_eval = sys.argv[5]

edge_type_set = set()
with open(input_file_aspect, "r") as f_in:
    for line in f_in:
        edge_type_set.add(line.strip())

with open(input_file_hin, "r") as f_in, open(output_file_hin, "w") as f_out:
    for line in f_in:
        edge_type = line.strip().split()[3].strip("-1")
        if edge_type in edge_type_set:
            f_out.write(line)

with open(input_file_eval, "r") as f_in, open(output_file_eval, "w") as f_out:
    neg_rate, num_pos = map(int, f_in.readline().strip().split())
    lines_out = []
    for line in f_in:
        edge_type = line.strip().split()[3].strip("-1")
        if edge_type in edge_type_set:
            lines_out.append(line)

    f_out.writelines([str(neg_rate) + " " + str(len(lines_out)/(neg_rate*2+1))+ "\n"] + lines_out)


