import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        entry_1, entry_2 = line.strip().split()[:2]
        if "W:" in entry_1 or "W:" in entry_2:
            continue
        f_out.write(line)