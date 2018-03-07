import sys
import numpy as np
from sklearn.linear_model import LogisticRegression # use this package
from sklearn.utils import shuffle
import time
import threading
import argparse


# for counting file lines
def file_len(f_name):
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

parser = argparse.ArgumentParser(description="Read in input and output filenames.")
parser.add_argument("--input-label-train", nargs="?", help="Input label train.", type=str)
parser.add_argument("--input-label-test", nargs="?", help="Input label test.", type=str)
parser.add_argument("--input-embedding", nargs="?", help="Input embedding", type=str)
parser.add_argument("--output-file", nargs="?", help="Output filename.", type=str)
args = parser.parse_args()


input_label_train = args.input_label_train
input_label_test = args.input_label_test
input_embedding=args.input_embedding
output_test_score = args.output_file





"""
Train logit model
"""
start_time = time.time()
embedding_dict={}
with open(input_embedding, "r") as f_in:
    num_nodes, dim = map(int, f_in.readline().strip().split())  # first line is special
    count=0
    for line in f_in:
        line_split = line.strip().split()
        a=list(map(float, line_split[1:]))
        embedding_dict[line_split[0]] = np.asarray(a)
        count+=1
    assert len(embedding_dict) == num_nodes, "Number of nodes does not agree."
    
print ("Embedding loading done.", num_nodes, "nodes with dim", dim, "from", input_embedding)

feature_train_dic={}
feature_train_list = []
with open(input_label_train, "r") as f_in:
    count=0
    for line in f_in:
        line=line.strip().split()
        node_1=embedding_dict[line[0]]

        node_2=embedding_dict[line[1]]
        edge=line[-1]
        y_value=line[2]
        if edge not in feature_train_dic:
            feature_train_dic[edge]={}
            feature_train_dic[edge]['tuple']=[]
            feature_train_dic[edge]['yvalue']=[]
        feature_train_dic[edge]['tuple'].append(np.multiply(node_1,node_2))
        feature_train_dic[edge]['yvalue'].append(y_value)
        if edge!='PP':
            edge_reverse=edge[::-1]
            if edge_reverse not in feature_train_dic:
                feature_train_dic[edge_reverse]={}
                feature_train_dic[edge_reverse]['tuple']=[]
                feature_train_dic[edge_reverse]['yvalue']=[]
            feature_train_dic[edge_reverse]['tuple'].append(np.multiply(node_1,node_2))
            feature_train_dic[edge_reverse]['yvalue'].append(y_value)
        count+=1
        if count%100000==0:
            print(count,' tuples read')
        
for edge in feature_train_dic.keys():
    f=[]
    f.append(np.array(feature_train_dic[edge]['tuple']))
    feature_train_dic[edge]['Xtrain']= np.hstack(tuple(f))
    num_instance_train = len(feature_train_dic[edge]['tuple'])
    feature_train_dic[edge]['tuple']=[]
    assert num_instance_train == feature_train_dic[edge]['Xtrain'].shape[0], "Train instance numbers do not match."
    y_train = np.zeros(num_instance_train)
    for i in range(num_instance_train):
        y_train[i] = int(feature_train_dic[edge]['yvalue'][i])
    feature_train_dic[edge]['ytrain']=y_train
    print(edge,' finished')

end_time = time.time()
print ("Train features loading and stacking done. Time: {0}s seconds. ".format((end_time - start_time)))
    
start_time = time.time()
for edge in feature_train_dic.keys():
    print('now training ',edge)
    logit_model = LogisticRegression(solver="sag",max_iter=10)  
    feature_train_dic[edge]['model']=logit_model

threads=[]
for edge in feature_train_dic.keys():
    t = threading.Thread(target=feature_train_dic[edge]['model'].fit, args=(feature_train_dic[edge]['Xtrain'], feature_train_dic[edge]['ytrain']),name=edge)
    threads.append(t)
    t.start()
    '''
    X_shuf, Y_shuf = shuffle(feature_train_dic[edge]['Xtrain'], feature_train_dic[edge]['ytrain'])
    logit_model = logit_model.fit(X_shuf, Y_shuf)  
    feature_train_dic[edge]['model']=logit_model
    print(edge,' training is done.')'''
has_running = True
while has_running:
    num_done = 0
    for t in threads:
        if not t.isAlive():
            # get results from thtead
            print(t.getName(),' training is done')
            num_done += 1
    if num_done == len(threads):
        break
    else:
        time.sleep(3)
end_time = time.time()

print ("Logit model fitting done. Training time: %s seconds" % (end_time - start_time))



"""
Predict on test
"""
start_time = time.time()
feature_test_dic={}
with open(input_label_test, "r") as f_in:
    count=0
    for line in f_in:
        line=line.strip().split()
        node_1=embedding_dict[line[0]]
        node_2=embedding_dict[line[1]]
        edge=line[-1]
        yvalue=line[2]
        if edge not in feature_test_dic:
            feature_test_dic[edge]={}
            feature_test_dic[edge]['tuple']=[]
            #feature_test_dic[edge]['line']=[]
            feature_test_dic[edge]['current']=0
        feature_test_dic[edge]['tuple'].append(np.multiply(node_1,node_2))
        #feature_test_dic[edge]['line'].append([line[0],line[1]])
end_time = time.time()
print('finished reading test file, time: ', (end_time - start_time))


for edge in feature_test_dic.keys():
    f=[]
    f.append(np.array(feature_test_dic[edge]['tuple']))
    feature_test_dic[edge]['Xtest']=np.hstack(tuple(f))
    num_instance_test = len(feature_test_dic[edge]['tuple'])
    assert num_instance_test == feature_test_dic[edge]['Xtest'].shape[0], "Test instance numbers do not match."
# compute predicted value for file_2; a row of X_test is the vector -- emb(node_1) 
#hadamard-prod emb(node_2) -- where node_1 and node_2 are the two nodes on a line of file *2*
    proba_test = logit_model.predict_proba(feature_test_dic[edge]['Xtest'])
    #print(proba_test[:,1])
    feature_test_dic[edge]['p_test']=proba_test[:,1]
    feature_test_dic[edge]['Xtest']=[]
    print('finished proba: ', edge)


## output a file with same format as file_2, with the third column replaced by your predicted value as in proba_test

## summary: input -- file_2, file_3, embedding file;
##			output -- the file similar to file_2 with third column replace and 
## note: please be careful that for each edge type (r), a different model will be trained and used for prediction
## example files: 	file_2 -- /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_20neg_eval_fast.txt
## 					file_3 -- /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_for_logit_training.txt
## 					emb_file -- /shared/data/yushi2/edge_rep_codes/input_data/dblp_0.2_out_line_samples100000_alpha0.1_dim128.emb

with open(input_label_test, "r") as f_in,open(output_test_score, "w+") as f_out:
    content=""
    rd=0
    for line in f_in:
        line=line.strip().split()
        edge=line[-1]
        current=feature_test_dic[edge]['current']
        temp=line[0]+' '+line[1]+' '+str(feature_test_dic[edge]['p_test'][current])+' '+edge+'\n'
        #print(temp)
        current+=1
        feature_test_dic[edge]['current']=current
        content=content+temp
        rd+=1
        if rd%50000==0:
            print (rd,'lines finished')
            f_out.write(content)
            content=''
    f_out.write(content)
    f_out.close()
        








