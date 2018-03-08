# Evaluation

This repository provides a reference implementation of evalution of data according to embedding/score file and x_eval.txt file generated from edge knockout process:<br>


### Basic usage

#### Input

There are 2 required input files.
1. **input-embedding-file** contains embedding result, they are in the format of:
					
		To be editted
   We also provide the **input-score-file** edtion in the folder, the score file should be in the format of:
   
   		To be editted
	
2. **input-eval-file** is the eval file that we generated from edge knockout process.

			
			
And another 1 required input data:

1. **sample-number** is the number that consist with input-eval-file, which is the # of edges that we generate for each node.

#### Output

It will print the averge mrr number for each edge_type and the total average number.
							
#### Execute and example

_All the commands are executed from the project home directory. And we are using python3._<br/> 

Here is an exmaple of generating output files using embedding file:

	python mrr_from_embedding

## Citing


## Miscellaneous

Please send any questions you might have about the codes and/or the algorithm to <fangguo1@illinois.edu>.



