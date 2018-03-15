#!/bin/bash

for smp in 500 1000 2000 5000 10000 20000
do
    /data/yushi2/aspect_embedding_codes/baselines/line/line  -train ../input_data/dblp_0.2_out_downsampled.net -output ../intermediate_data/dblp_0.2_out_downsampled_line_samples"$smp"_alpha0.1_dim128.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 20
done
