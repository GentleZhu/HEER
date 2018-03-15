# Knockout HIN

This repository provides a reference implementation of edge reconstruction for HEER as described in the paper:<br>


### Basic usage

#### Input

There are **1** required input file.
1. **input-hin-file** is the file containing all edges of the input HIN, it should be in the format of :
					
		node_name_1 node_name_2 edge_weight edge_type
					
	Note that node_name_1 and node_name_2 are in the format of :
		
		node_type:node_value
		
	For example: P:20883
		
	And also if edge is directed, edge_type should be in the format of:
	
		edge_value:d 
		
	Otherwise it is in the format of 
	
		edge_value:u
			
With another **3** required input arguments:

1. **ko-rate** stands for the knockout rate. It is a float. For example, 0.1 means you will knock out 10% of the original edges.

2. **dataset-name** is the name that the output files will use as prefix. It is a string. For example, if the dataset-name is 'dblp' then the output fils will be named as 'dblp_xxx'. 

3.  **path-output** is the path that the generator will put files to. It is a string. 

And another **2** optional input arguments:

1. (optional)**sample-number** stands for the number of new edges you want to generate. It is aa integer. For exmaple, with knocked out edge AB, sample number =10 means you will generate 10 new edges with fixed node A and another 10 edges with fixed node B. Thn default sample number =10

2. (optional)**buffer-size** is the size of temporary trunk for output saving. It is an integer. The default buffer-size = 500000.


#### Output

There will be 3 files generated. 
**first file** is named as:
		
	dataset-name_ko_ko-rate.hin

It contains all the edges from **input-hin-file** without the kicked out edges and it is in the format of:

	node_name_1 node_name_2 weight edgetype
		
**second file** is named as:
		
	dataset-name_ko_ko-rate_eval.txt

The first line of **second file** contains the basic information as :
	
	#_of_negative_example_per_direction_in_one_batch #_of_total_batches.

Note that one Batch has (1+**sample-number***2) edges, the fisrt edge in the batch is the edge that has been knocked out from 
**input-hin-file**, then the following **sample-number***2 node pairs that are not associated by edges with respect to this  knocked out edge. 
The detailed generating rule is explaned in our paper.

Each edge is in the format of:

	node_name_1 node_name_2 weight edgetype

   For one edgetype 'xxx', its reverse type will be marked as 'xxx-1'. For example, one edge type is 'hasChild', 
   then its reverse edge will be 'hasChild-1'.
   
**third file**	is name as	
	
	dataset-name.config
				
It contains following informaton:
The first line is a list of edge type, each edge type is represented as a list of left node index and right node index; 
The second line is a list of node indexes starting from 0. They are in string type;
The third line is a list of edge indexes starting from 0. They are in string type;
The fourth line is a list of each edge's directed contion. 
For this sample config file DBLP.config:

	
#### Execute and example
And we are using python3.<br/> 

Here is an exmaple of generating output files

	python ko_hin.py --input-hin-file input_data/dblp.hin --data-set-name dblp --path-output output --ko-rate 0.2

## Citing


## Miscellaneous

Please send any questions you might have about the codes and/or the algorithm to <fangguo1@illinois.edu>.



