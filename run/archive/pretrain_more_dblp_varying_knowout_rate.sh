#!/bin/bash

for smp in 50000 
do
    #/data/yushi2/aspect_embedding_codes/baselines/line/line  -train ../input_data/dblp_0.4_out.net -output ../intermediate_data/dblp_0.4_out_line_samples"$smp"_alpha0.1_dim128.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
    #/data/yushi2/aspect_embedding_codes/baselines/line/line  -train ../input_data/dblp_0.6_out.net -output ../intermediate_data/dblp_0.6_out_line_samples"$smp"_alpha0.1_dim128.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
    /data/yushi2/aspect_embedding_codes/baselines/line/line  -train ../input_data/dblp_0.8_out.net -output ../intermediate_data/dblp_0.8_out_line_samples"$smp"_alpha0.1_dim128.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
done
