# HEER: Easing Embedding Learning by Comprehensive Transcription of Heterogeneous Information Networks

Source code and data for KDD'18 paper *[Easing Embedding Learning by Comprehensive Transcription of
Heterogeneous Information Networks](http://yushi2.web.engr.illinois.edu/kdd18.pdf)*. 
## Dependencies

We will take Ubuntu for example.
* python 2.7
* python 3.5
* [PyTorch 4.0](https://pytorch.org/)

## Data
### HIN datasets
We use two publicly available real-world HIN datasets: DBLP and YAGO. We provide processed data links for reproducing our results. 
* **DBLP** ([Tang et al., 2008](https://dl.acm.org/citation.cfm?id=1402008)): DBLP is a bibliographical network in the computer science domain. There are five types of nodes in the network: author, paper, key term, venue, and year. The edge types include authorship (aut.), term usage (term), publishing venue(ven.), and publishing year (year) of a paper, and the reference relationship from a paper to another (ref.). [[download](https://s3.us-east-2.amazonaws.com/heer-data/dblp.zip)] [[pretrained LINE embeddings](https://s3.us-east-2.amazonaws.com/heer-data/pretrained_dblp_emb.zip)]
* **YAGO** ([Suchanek et al., 2007](https://suchanek.name/work/publications/www2007.pdf)): YAGO is a large-scale knowledge graph derived from Wikipedia, WordNet, and GeoNames. There are seven types of nodes in the network: person, location, organization, piece of work, prize, position, and event. A total of 24 edge types exist in the network, with five being directed and others being undirected. [[download](https://s3.us-east-2.amazonaws.com/heer-data/yago.zip)] [[pretrained LINE embeddings](https://s3.us-east-2.amazonaws.com/heer-data/pretrained_yago_emb.zip)]

## Train HEER
The hyperparameters for HEER are network name, epoch number, operator, edge mapping function and specified GPU ID. Please unzip the datasets into input_data/, unzip pretrained embeddings into intermediate_data/
### Example Usage
```
$ bash ./src/run.sh $network $epoch $op $mode $more_param $gpu $dump_timer
```
### Default Run & Parameters
Run HEER training on the YAGO dataset, knock out rate is 0.4
```
$ bash ./src/run.sh yago_ko_0.4 61 1 0 rescale_0.1_lr_10_lrr_10 0 6
```

## Evaluation
Run HEER evaluation on the YAGO dataset, knock out rate is 0.4. Micro-MRR, Macro-MRR and MRR for each specific edge type can be found in evaluation result files under output/
```
$ bash ./src/eval.sh yago_ko_0.4 61 1 0 rescale_0.1_lr_10_lrr_10 0 6
```
## parameter specifications
operator:

	1. hadamard product
	2. outer-product
	3. deduction
	4. addition
	
mapping function:

	-1. unimetric
	0. linear mappng(HEER)
