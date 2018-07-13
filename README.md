# HEER: Easing Embedding Learning by Comprehensive Transcription of Heterogeneous Information Networks

Source code and data for KDD'18 paper *[Easing Embedding Learning by Comprehensive Transcription of
Heterogeneous Information Networks](https://arxiv.org/abs/1807.03490)*. 

KDD promotional video *[Click Here!](https://m.youtube.com/watch?v=LsOHdQ1Xdn8&feature=youtu.be)*
## Dependencies
* python 2.7
* python 3.5
* [PyTorch 4.0](https://pytorch.org/) with GPU support

## Data
We use two publicly available real-world HIN datasets: DBLP and YAGO. We provide processed data links to reproduce our results. 
* **DBLP** ([Tang et al., 2008](https://dl.acm.org/citation.cfm?id=1402008)): DBLP is a bibliographical network in the computer science domain. There are five types of nodes in the network: author, paper, key term, venue, and year. The edge types include authorship (aut.), term usage (term), publishing venue(ven.), and publishing year (year) of a paper, and the reference relationship from a paper to another (ref.). [[download](https://s3.us-east-2.amazonaws.com/heer-data/dblp.zip)] [[pretrained LINE embeddings](https://s3.us-east-2.amazonaws.com/heer-data/pretrained_dblp_emb.zip)]
* **YAGO** ([Suchanek et al., 2007](https://suchanek.name/work/publications/www2007.pdf)): YAGO is a large-scale knowledge graph derived from Wikipedia, WordNet, and GeoNames. There are seven types of nodes in the network: person, location, organization, piece of work, prize, position, and event. A total of 24 edge types exist in the network, with five being directed and others being undirected. [[download](https://s3.us-east-2.amazonaws.com/heer-data/yago.zip)] [[pretrained LINE embeddings](https://s3.us-east-2.amazonaws.com/heer-data/pretrained_yago_emb.zip)]

## Train HEER
The hyperparameters for HEER are network name and epoch number. Regarding our proposed edge reconstruction task, the $network is formatted as *$data-name*\_*ko*\_*$ko-rate*, e.g. yago_ko_0.4. You can find both DBLP and YAGO datasets with knock out rate from 0.1 to 0.9 in above link.
### Example Usage
```
$ ./src/run.sh $network $epoch
```
### Default Run & Parameters
Run HEER training on the YAGO dataset for 61 epochs, knock out rate is 0.4. We set the default model dump timer as 6, so you will have 10 models.
```
$ ./src/run.sh yago_ko_0.4 61
```

## Evaluation
Similar with training, here we show how to evaluate HEER on the YAGO dataset, knock out rate is 0.4. Micro-MRR, Macro-MRR and MRR for each specific edge type can be found in evaluation result files under output/. 
```
$ ./src/eval.sh yago_ko_0.4 61
```
## Play with Your Own Data
We also provide tools to generate train and test data from any HINs. You can find detailed instructions under [preprocessing/](https://github.com/GentleZhu/HEER/tree/master/preprocessing). In short, you need to prepare a formatted edge list and a data-specific config file. Then pre-train LINE embedding via [pretrain/](https://github.com/GentleZhu/HEER/tree/master/pretrain). Take **yago.config** for example, 
	
    [[0, 1], [0, 2], [0, 2], [0, 1], [0, 3], [0, 4], [4, 4], [0, 4], [0, 4], [0, 1], [0, 4], [0, 0], [0, 0], [0, 1], [0, 5], [0, 0], [2, 4], [0, 2], [0, 0], [6, 4], [0, 1], [0, 4], [0, 0], [4, 4]]
    ['PE', 'WO', 'AS', 'PR', 'AD', 'PO', 'EV']
    ['<created>:u', '<isAffiliatedTo>:u', '<playsFor>:u', '<actedIn>:u', '<hasWonPrize>:u', '<diedIn>:u', '<isPartOf>:d', '<isCitizenOf>:u', '<wasBornIn>:u', '<wroteMusicFor>:u', '<livesIn>:u', '<hasChild>:d', '<isMarriedTo>:u', '<directed>:u', '<holdsPosition>:u', '<influences>:d', '<isLocatedIn>:u', '<graduatedFrom>:u', '<isConnectedTo>:u', '<happenedIn>:u', '<edited>:u', '<isPoliticianOf>:u', '<isAdvisedBy>:d', '<hasCapital>:d']
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1]
  
The first line describes left and right node types of a specific edge types, in which you need to index them in the node type list. The second line is the node type list. The third and fourth line describes edge types and directions. For example, `<created>:u` means `created` is an un-directed relation. Moreover, the first `0` in the fourth line indicates it is un-directed as well.

You can create your own train and evaluation file using, please refer [preprocessing/ (https://github.com/GentleZhu/HEER/blob/master/preprocessing/Readme.md) for more details:
```
$ python ./preprocessing/ko_hin.py --input-hin-file your-data --data-set-name preferred-network-name --path-output output-path --ko-rate 0.x
```
