#!/bin/bash

# e.g.: ./knock_out_hin_and_pretrain.sh ../input_data/yago_original.hin yago 0.1

# find relative root directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
script_dir="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
root_dir="$( dirname $script_dir )"

# input variables
input_hin=$1  # the path to the complete HIN with format of knocked_out_hin_file
hin_name=$2
ko_rate=$3
if (( $# == 4 )); then
	num_edge_smp=$4  # number of million edges sampled by LINE
else
	if [[ "$hin_name" = *"yago"* ]]; then
		num_edge_smp=10000
	else
		if [[ "$hin_name" = *"dblp"* ]]; then
			num_edge_smp=100000
		else
			echo "Sampling 100000 edges for pretrain using LINE. This variable can be specified as the fourth argument."
			num_edge_smp=100000
		fi
	fi
fi

# files
knocked_out_hin_file="$root_dir"/input_data/"$hin_name"_ko_"$ko_rate".hin
eval_file="$root_dir"/input_data/"$hin_name"_ko_"$ko_rate"_eval.txt
fast_eval_file="$root_dir"/input_data/"$hin_name"_ko_"$ko_rate"_eval_fast.txt
knocked_out_hin_file_for_line="$knocked_out_hin_file".temp
line_emb="$root_dir"/intermediate_data/line_"$hin_name"_ko_"$ko_rate".emb

# knock out HIN
python3 "$root_dir"/preprocessing/ko_hin.py --input-hin-file "$input_hin" --data-set-name "$hin_name" --path-output "$root_dir"/input_data --ko-rate "$ko_rate"

# down sample eval file to generate the fast version
python2 "$root_dir"/aux/downsample_eval_file.py --input-file "$eval_file" --output-file "$fast_eval_file"

# pretrain by LINE
awk '{print $1, $2, $3}' "$knocked_out_hin_file" > "$knocked_out_hin_file_for_line"
"$root_dir"/pretrain/line -train "$knocked_out_hin_file_for_line" -output "$line_emb" -size 128 -order 1 -negative 5 -samples "$num_edge_smp"
rm "$knocked_out_hin_file_for_line"


