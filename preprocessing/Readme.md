# Knockout HIN

This repository provides a reference implementation of edge reconstruction for HEER as described in the paper:<br>


### Basic usage

#### Input

There are **1** required input files.
1. **input-hin-file** is the file containing all edges of the input HIN, it should be in the format of :
					
		node_name_1 node_name_2 edge_weight edge_type
					
	Note that node_name_1 and node_name_2 are in the format of :
		
		node_type:node_value
	
	For example: P:20883
			
And another **3** required input arguments:

1. **ko-rate** stands for the knockout rate. It is float type. For example, 0.1 means you will knock out 10% of the original edges.

2. **dataset-name** is the name that the output files will use as prefix. It is in string type. For example, if the dataset-name is 'dblp' then the output fils will be named as 'dblp_xxx'. 

3.  **path-output** is the path that the generator will put files to. It is in string type. 

And another **2** optional input arguments:

1. (optional)**sample-number** stands for the number of new edges you want to generate. It is int type. For exmaple, with knocked out edge AB, sample number =10 means you will generate 10 new edges with fixed node A and another 10 edges with fixed node B. Thn default sample number =10

2. (optional)**buffer-size** is the size of temporary trunk for output saving. The default buffer-size = 500000.


#### Output

There will be 2 files generated. 
**First file** is named as 
		
	dataset-name_ko_ko-rate.hin

It contains edges from the input network without the kicked out edges and it is in the format of:

	node_name_1 node_name_2 weight edgetype
		
And the **second file** is named as 
		
	dataset-name_ko_ko-rate_eval.txt

The first line of **second file** contains the basic information as :
	
	#of_negative_example_per_direction_in_one_batch #total batches.

One Batch has (1+**sample-number***2) edges, the fisrt edge in the batch is the edge that has been knocked out from 
**input-hin-file**, then the following **sample-number***2 edges are ones that being generated from this knocked out edge. 
The detailed generating rule is explaned in the paper.

It is in the format of:

	node_name_1 node_name_2 weight edgetype

   For one edgetype 'xxx', its reverse value will be marked as 'xxx-1'. For example, one edge type is '<hasChild>', 
   then its reverse value will be '<hasChild>-1'
		
   

		
							
#### Execute and example
And we are using python3.<br/> 

Here is an exmaple of generating output files

	python ko_hin.py --input-hin-file input_data/dblp.hin --data-set-name dblp --path-output output --ko-rate 0.2

## Citing


## Miscellaneous

Please send any questions you might have about the codes and/or the algorithm to <fangguo1@illinois.edu>.



