input_hin = "../input_data/dblp_0.2_out.net"
output_pay = "../input_data/dblp_0.2_out_for_aspem_apy.net"
output_papvw = "../input_data/dblp_0.2_out_for_aspem_papvw.net"

with open(input_hin, "r") as f_in, open(output_pay, "w") as f_out_pay, open(output_papvw, "w") as f_out_papvw:
    for line in f_in:
        node_1, node_2, _ = line.strip().split()
        assert "P" in node_1
        if "A" in node_2:  # to both
            f_out_pay.write(line)
            f_out_papvw.write(line)
        elif "P" in node_2: # to papvw
            f_out_papvw.write(line)
        elif "V" in node_2: # to papvw
            f_out_papvw.write(line)
        elif "W" in node_2: # to papvw
            f_out_papvw.write(line)
        elif "Y" in node_2: # to pay
            f_out_pay.write(line)
        else:
            raise Exception("Inconsistent edge type")
