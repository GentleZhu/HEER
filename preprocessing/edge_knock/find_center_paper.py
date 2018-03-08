#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:56:40 2018

@author: fangguo1
"""

if __name__ == '__main__':
    author_set_dic={}
    venue_set_dic={}
    paper_set_dic={}#key-paper ,value- papers that cite key
    year_set_dic={}
    paper_connect_dic={}
    
    index2type={}
    '''
    First we build a dictionary, between index and type
    '''
    with open('index2name.txt',encoding="utf-8") as file:
        for line in file:
            line=line.split()
            second_part=line[1].split(".")
            itemtype=second_part[0]
            index2type[line[0]]=itemtype
    print('finished index2name')
    
    
    '''
    We start to save the edges in a dictionary called paper_connect_dic from reading p2a,
    And another dictionary called author_set_dic, each author will have a list of his papers
    '''
    with open('all_p2a.txt',encoding="utf-8") as file:
        for line in file:
            line=line.split()
            paper=line[0]
            author=line[1]
            if author not in author_set_dic:
                author_set_dic[author]={}
            author_set_dic[author][paper]=1
            if paper not in paper_connect_dic:
                paper_connect_dic[paper]={}
                paper_connect_dic[paper]['author']={}
                paper_connect_dic[paper]['venue']={}
                paper_connect_dic[paper]['paper']={}
                paper_connect_dic[paper]['pap']={}
                paper_connect_dic[paper]['pvp']={}
                paper_connect_dic[paper]['ppp']={}
                paper_connect_dic[paper]['pyp']={}
                paper_connect_dic[paper]['totalp']=set()

            if paper not in paper_set_dic:
                paper_set_dic[paper]={}
            if author not in paper_connect_dic[paper]['author']:
                paper_connect_dic[paper]['author'][author]=1
    print('finished reading p2a')
    
    '''
    After reading p2a, we will do pruning first, which will add qualified 
    pap to a list called qualified_papers_pap
    '''
    qualified_papers_pap=[]
    count=0
    for paper,dic in paper_connect_dic.items():
        #print(paper)
        for author in dic['author']:
            #print(author)
            for i in author_set_dic[author].keys():
                if i not in dic['pap'] and i != paper:
                    dic['pap'][i]=1
        #print(len(dic['pap']))
        if len(dic['pap']) >=200:
            qualified_papers_pap.append(paper)
        count+=1
    print(len(qualified_papers_pap))
    
    '''
    We start to reaing from p2o, for type paper, venue and year, we will build their own dictionary.
    Ex, for Venue, we will have venue_set_dic, each venue will have a list of its related papers.
    And we continue adding edges to paper_connect_dic
    '''
    with open('all_p2o.txt',encoding="utf-8") as file:
        count=0
        for line in file:
            line=line.strip().split()
            paper=line[0]
            node_2=line[1]
            name=index2type[node_2]
            tp=name[0]
            count+=1
            if tp!='P' and  tp!='V' and tp!='Y':
                continue
            if tp=='V':
                venue=node_2
                if paper in paper_connect_dic:  
                    if venue not in venue_set_dic:
                        venue_set_dic[venue]={}
                    venue_set_dic[venue][paper]=1
                    if venue not in paper_connect_dic[paper]['venue']:
                        paper_connect_dic[paper]['venue'][venue]=1
            if tp=='P':
                #paper_cited is being cited
                paper_cited=node_2
                if paper_cited in paper_connect_dic:
                    paper_set_dic[paper_cited][paper]=1
                    if paper not in paper_connect_dic[paper_cited]['paper']:
                        paper_connect_dic[paper_cited]['paper'][paper]=1   
            if tp=='Y':
                year=node_2
                paper_connect_dic[paper]['year']=year
                if year not in year_set_dic:
                    year_set_dic[year]={}
                if paper not in year_set_dic[year]:
                    year_set_dic[year][paper]=1

    print('finished reading p2o')
    #print(paper_connect_dic['287144']['venue'])
    
    
    '''After we finished all above dicitonaries, we start to prune from qualified_papers_pap. First we 
        do with pvp and will add qualified paper to qualified_papers_pvp untill the count is 60000.
    '''
    count=0
    qualified_papers_pvp=[]
    for paper in qualified_papers_pap:
        pap=paper_connect_dic[paper]['pap'].keys()
        size_pap=len(pap)
        for venue in paper_connect_dic[paper]['venue']:
            for i in venue_set_dic[venue].keys():
                if i not in paper_connect_dic[paper]['pap'] and i not in paper_connect_dic[paper]['pvp'] and i!=paper:
                    paper_connect_dic[paper]['pvp'][i]=1
        size_pvp=len(paper_connect_dic[paper]['pvp'])
        
        if size_pvp>=200 and size_pvp/size_pap <=4 and size_pap/size_pvp <=4:
            qualified_papers_pvp.append(paper)
            #print(paper,size_pap, size_pvp)
        count+=1
        if(count%5000==0):
            print(count,' papers checked')
        if len(qualified_papers_pvp)==60000:
            break

    '''Then we do pruning with ppp, add papers from qualified_papers_pvp to qualified_papers_ppp until count
    is 1000
    '''
    
    qualified_papers_ppp=[]
    for paper in qualified_papers_pvp:
        count=0
        for i in paper_connect_dic[paper]['paper']:
            if i not in paper_connect_dic[paper]['pvp'] and i not in paper_connect_dic[paper]['pap']:
                paper_connect_dic[paper]['ppp'][i]=1
                count+=1
        size_ppp=len(paper_connect_dic[paper]['ppp'])
        size_pap=len(paper_connect_dic[paper]['pap'])
        size_pvp=len(paper_connect_dic[paper]['pvp'])
        if count >=200 and size_ppp/size_pvp<=4 and size_pvp/size_ppp<=4 and size_pap/size_ppp<=4 and size_ppp/size_pap<=4:
            qualified_papers_ppp.append(paper)
            #print(paper,size_pap, paper_connect_dic[paper]['venue'],size_pvp,size_ppp)

        if len(qualified_papers_ppp)==1000:
            break
    print('finished ppp')
    
    '''
    Finally we do pruning on pyp and stop when we have find 10 qualified papers.
    '''
        
    qualified_papers_pyp=[]    
    count=0
    for paper in qualified_papers_ppp:
        if 'year' not in paper_connect_dic[paper]:
            print('year not exist ',paper)
            continue
        year=paper_connect_dic[paper]['year']
        same_year_paper_count=0
        for i in year_set_dic[year].keys():
            if i not in paper_connect_dic[paper]['pap'] and i not in paper_connect_dic[paper]['pvp'] and i not in paper_connect_dic[paper]['ppp']and i!=paper:
                paper_connect_dic[paper]['pyp'][i]=1
                same_year_paper_count+=1
                if same_year_paper_count==500:
                    break
        if len(paper_connect_dic[paper]['pyp'])>=500:
            qualified_papers_pyp.append(paper)
            count+=1
            if count==10:
                break
            
    
    for paper in qualified_papers_pyp:
        file_to_write='path/center_paper_'+paper+'.txt'
        file=open(file_to_write,'w+')
        for reached_paper in paper_connect_dic[paper]['pap']:
            content=reached_paper+' PAP\n'
            file.write(content)
        for reached_paper in paper_connect_dic[paper]['pvp']:
            content=reached_paper+' PVP\n'
            file.write(content)
        for reached_paper in paper_connect_dic[paper]['ppp']:
            content=reached_paper+' PPP\n'
            file.write(content)
        for reached_paper in paper_connect_dic[paper]['pyp']:
            content=reached_paper+' PYP\n'
            file.write(content)
        file.close()
        print(paper,'finished writing')

        

            

        
            

            
        
        
        
        
                
            
            
        
