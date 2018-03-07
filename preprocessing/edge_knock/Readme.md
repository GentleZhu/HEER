# Edge Knockout

This repository provides a reference implementation of edge reconstruction for HEER as described in the paper:<br>


### Basic usage

#### Input

There are 3 required input files.
1. **p2afile** contains the edges between papers and authors, they are in the format of:
					
		paper_index author_index edge_weight
					
	Note that edge_weight=0 means the edge does not exist.
	
2. **p2ofile** contains the edges between papers and other type nodes, they are in the format of:

		paper_index other_type_node_index edge_weight
			
3. **index2name** contains a dictionary between node indexs and node information, they are in the format of:
		
		node_index node_info
		
	Note that node_name is formatted as 
		
		node_type.node_name
			
And another 3 required input datas:

1. **ko-rate** stands for the knockout rate. It is float type. For example, 0.1 means you will knock out 10% of the original edges.

2. **sample-number** stands for the number of new edges you want to generate. It is int type. For exmaple, with knocked out edge AB, sample number =10 means you will generate 10 new edges with fixed node A and another 10 edges with fixed node B.

3. **dataset-name** is the name that the output files will use as prefix. It is string type. For example, if the dataset-name is 'DBLP' then the output fils will be named as 'DBLP_xxx'. The default name is 'unknown'.

4. **path-output** is the path that the generator will put files to. It is string type. The dafault value is ''.

5. **buffer-size** is the size of temporary trunk for output saving. The default value is 50000.


#### Output

There will be 2 files generated. First file is named as 
		
	dataset-name_ko_ko-rate.hin

It contains edges from the input network without the kicked out edges and it is in the format of:

	node_name node_name weight edgetype
	
   For edgetype, it is in the format of "node1node2"
		
And the second file is named as 
		
	dataset-name_ko_ko-rate_sample-number_eval.txt

It contains edges that being kickout out and the new generated edges with ko-rate. It is in the format of:

	node_name node_name weight edgetype

   For edge type, if it truely exists in the network, then it is in the format of **'node1node2'**; if it is 
   
   generated and not exists in the network, then it is in the format of **'node1node2-1'**
		
   And the first line of second file contain the basic information as :
	
	#of negative example per direction in one batch, #total batches.

		
							
#### Execute and example

_All the commands are executed from the project home directory. And we are using python3._<br/> 

Here is an exmaple of generating output files

	python edge_knock.py --input-p2afile data/all_p2a.txt --input-p2ofile data/all_p2o.txt --input-index2name data/index2name.txt --ko-rate 0.2 --data-set-name DBLP --path-output data 

## Citing


## Miscellaneous

Please send any questions you might have about the codes and/or the algorithm to <fangguo1@illinois.edu>.



