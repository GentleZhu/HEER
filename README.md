# README
## Train embedding
```
source /shared/data/qiz3/qiz3/bin/activate
Format:
bash ./src/run.sh $network $epoch $op $mode $net_type $gpu

bash ./src/run.sh yago_ko_0.4 20 1 0 yago 7
bash ./src/eval.sh yago_ko_0.4 20 1 0 yago 7
```

## specifications
CHECK parameters op and map\_func in run.sh

operator:

	1. hadamard product
	2. outer-product
	3. deduction
	4. addition
	
mapping function:

	-1. unimetric
	0. linear mappng with batch norm
	1. linear mappng with batch norm
	2. linear mappng with batch norm + ReLU
	3. fully connected mappng with batch norm
