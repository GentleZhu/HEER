#!/bin/bash

for i in 0.2
do
    #for smp in 5000 10000 20000 50000 100000 200000
    for smp in 500 1000 2000 5000 10000 20000
    do
        /data/yushi2/aspect_embedding_codes/baselines/line/line -train ../input_data/dblp_"$i"_out_for_aspem_pay_normalized.net -output ../intermediate_data/dblp_"$i"_out_aspem_samples"$smp"_pay_normalized.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
        /data/yushi2/aspect_embedding_codes/baselines/line/line -train ../input_data/dblp_"$i"_out_for_aspem_papvw_normalized.net -output ../intermediate_data/dblp_"$i"_out_aspem_samples"$smp"_papvw_normalized.emb -size 128 -order 1 -negative 5 -samples "$smp" -alpha 0.1 -threads 30
        python ../aux/merge_score_aspem.py ../intermediate_data/dblp_"$i"_out_aspem_samples"$smp"_pay_normalized.emb ../intermediate_data/dblp_"$i"_out_aspem_samples"$smp"_papvw_normalized.emb ../intermediate_data/dblp_"$i"_out_aspem_samples"$smp"_normalized
    done
done

