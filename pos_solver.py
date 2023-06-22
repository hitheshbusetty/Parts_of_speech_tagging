###################################
# CS B551 Spring 2021, Assignment #3
#
# 
# Hithesh Busetty and bhithesh
# 
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import statistics
from statistics import mode  


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    def __init__(self):
        self.pos_frequency={'noun':0, 'adj':0, 'adv':0, 'adp':0, 'conj':0, 'det':0, 'num':0, 'pron':0, 'prt':0, 'verb':0, 'x':0, '.':0}
        self.transition_frequency={}
        self.word_pos_frequency={}
        self.word_frequency={}
        self.emission_prob={}
        self.transition_prob={}
        self.trained_words=0
        self.trained_sentences=0
        self.pos_type=['noun', 'adj', 'adv', 'adp', 'conj', 'det', 'num', 'pron', 'prt', 'verb', 'x', '.']
        self.transition_s3_s1={}
        self.transition_prob_s3_s1={}
        
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post=0
            for i in  range(len(sentence)):
                if (sentence[i],label[i]) not in self.word_pos_frequency:
                    post+=math.log(10**-10)
                else:
                    post+=math.log(self.word_pos_frequency[sentence[i],label[i]]/self.pos_frequency[label[i]])
            return post
                
        elif model == "HMM":
            post=0
            if (sentence[0],label[0]) not in self.word_pos_frequency:
                post+=math.log(10**-10)
            else:
                post+=math.log(self.word_pos_frequency[sentence[0],label[0]]/self.pos_frequency[label[0]])
                post+=math.log(self.transition_prob["start",label[0]])
            for i in range(1,len(sentence)):
                if (sentence[i],label[i]) not in self.word_pos_frequency:
                    post+=math.log(10**-10)
                else:
                    post+=math.log(self.word_pos_frequency[sentence[i],label[i]]/self.pos_frequency[label[i]])
                    post+=math.log(self.transition_prob[label[i-1],label[i]])
                
            return post
        elif model == "Complex":
            post=0
            for i in range(0,len(sentence)):
                if i==0:
                    if ((sentence[0],label[0]) not in self.word_pos_frequency) or (("start",label[0]) not in self.transition_prob):
                        post+=math.log(10**-10)
                    else:
                        post+=math.log(self.word_pos_frequency[sentence[0],label[0]]/self.pos_frequency[label[0]])
                        post+=math.log(self.transition_prob["start",label[0]])
                if i==1:                                                                   
                    if ((sentence[1],label[1]) not in self.word_pos_frequency) or ((label[0],label[1]) not in self.transition_prob):
                        post+=math.log(10**-10)
                    else:
                        post+=math.log(self.word_pos_frequency[sentence[1],label[1]]/self.pos_frequency[label[1]])
                        post+=math.log(self.transition_prob[label[0],label[1]])
                if i!=1 and i!=0:
                    if ((sentence[i],label[i]) not in self.word_pos_frequency.keys()) or ((label[i-1],label[i]) not in self.transition_prob.keys()) or ((label[i-2],label[i]) not in self.transition_prob_s3_s1.keys()):
                        post+=math.log(10**-10)
                    else:
                        post+=math.log(self.word_pos_frequency[sentence[i],label[i]]/self.pos_frequency[label[i]])
                        post+=math.log(self.transition_prob[label[i-1],label[i]])
                        post+=math.log(self.transition_prob_s3_s1[label[i-2],label[i]])
                
            return post
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):
        self.trained_sentences=len(data)
        for i in data:
            for j in i[1]:
                self.pos_frequency[j]+=1
                self.trained_words+=1
            for word in i[0]:
                if word not in self.word_frequency.keys():
                    self.word_frequency[word]=1
                else:
                    self.word_frequency[word]+=1
            for j in range(0,len(i[1])):
                if (i[0][j],i[1][j]) not in self.word_pos_frequency.keys():
                    self.word_pos_frequency[(i[0][j],i[1][j])]=1
                else:
                    self.word_pos_frequency[(i[0][j],i[1][j])]+=1
            for j in range(0,len(i[1])):
                if j==0:
                    if ("start",i[1][j]) not in self.transition_frequency.keys():
                        self.transition_frequency[("start",i[1][j])]=1
                    else:
                        self.transition_frequency[("start",i[1][j])]+=1
                else:
                    if (i[1][j-1],i[1][j]) not in self.transition_frequency.keys():
                        self.transition_frequency[(i[1][j-1],i[1][j])]=1
                    else:
                        self.transition_frequency[(i[1][j-1],i[1][j])]+=1
            for j in range(0,len(i[1])):
                if (i[1][j-1],i[1][j]) not in self.transition_s3_s1.keys():
                    self.transition_s3_s1[(i[1][j-1],i[1][j])]=1
                else:
                    self.transition_s3_s1[(i[1][j-1],i[1][j])]+=1     
            
                   
            for j in self.transition_s3_s1:
                self.transition_prob_s3_s1[j]=self.transition_s3_s1[j]/self.pos_frequency[j[0]]
           
            # calculating transition probabilities
            for j in self.transition_frequency:
                if j[0]!="start":
                    self.transition_prob[j]=self.transition_frequency[j]/self.pos_frequency[j[0]]
                else:
                    self.transition_prob[j]=self.transition_frequency[j]/self.trained_sentences
            
            
                    
            # calculating emission probabilities
            #for i in self.word_pos_frequency:
                #self.emission_prob[i]=self.word_pos_frequency[i]/self.pos_frequency[i[1]]
            
   
    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        pos_sequence=[]
        for i in sentence:
            max_probability=0
            max_pos_type="noun"
            for j in self.pos_type:
                if (i,j) not in self.word_pos_frequency.keys():
                    current_probability=0
                else:
                    current_probability=self.word_pos_frequency[(i,j)]/self.word_frequency[i]
                #print(current_probabilty)
                if current_probability>max_probability:
                    max_probability=current_probability
                    max_pos_type=j
            pos_sequence.append(max_pos_type)
                
        return pos_sequence

    def hmm_viterbi(self, sentence):
        N=len(sentence)
        observed=sentence
        v_table={}
        which_table={}
        for i in self.pos_type:
            v_table[i]=[0]*N
            which_table[i]=[0]*N
        
        for pos in self.pos_type:
            if (observed[0],pos) not in self.word_pos_frequency:
                v_table[pos][0]=10**-10
            else:
                v_table[pos][0]= self.transition_prob["start",pos]*(self.word_pos_frequency[(observed[0],pos)]/self.pos_frequency[pos])
            
        for i in range(1, N):
            for pos in self.pos_type:
                if (observed[i],pos) not in self.word_pos_frequency:
                    v_table[pos][i]=10**-10
                else:
                    v_table[pos][i]= (self.word_pos_frequency[(observed[i],pos)]/self.pos_frequency[pos])
                max_trans=0
                for z in self.pos_type:
                    if (z,pos) not in self.transition_prob:
                        trans_prob=0
                    else:
                        trans_prob = v_table[z][i-1]*self.transition_prob[(z,pos)]
                    if max_trans<trans_prob:
                        max_trans=trans_prob
                        which_table[pos][i] = z
                    #if max_trans==0:
                        #which_table[pos][i]="noun"
                v_table[pos][i]*=max_trans
        viterbi_seq = [""] * N
        #print(v_table)
        #print(which_table)
        for pos in self.pos_type:
            max_v_value=0
            if max_v_value<v_table[pos][N-1]:
                max_v_value=v_table[pos][N-1]
                viterbi_seq[N-1] = pos
    
        for i in range(N-2, -1, -1):
            #print(viterbi_seq[i+1],[i+1])
            viterbi_seq[i] = which_table[viterbi_seq[i+1]][i+1]
        return viterbi_seq

    def complex_mcmc(self, sentence):
        import statistics
        from statistics import mode  
        intial=["noun"]*len(sentence)
        sample_counter=0
        final_sample=[]
        final_sample.append(intial)
        while sample_counter<100:
            for i in range(len(intial)):
                max_prob=0
                max_pos=intial[i]
                for pos in self.pos_type:
                    if i==0:
                        if (sentence[i],pos) not in self.word_pos_frequency.keys():
                            curr_prob=10**-10
                        else:
                            curr_prob=(self.word_pos_frequency[(sentence[i],pos)]*self.transition_prob[("start",pos)])

                    if i==1:
                        if ((sentence[i],pos) not in self.word_pos_frequency) or ((intial[i-1],intial[i]) not in self.transition_prob):
                            curr_prob=10**-10
                        else:
                            curr_prob=self.word_pos_frequency[(sentence[i],pos)]*self.transition_prob[(intial[i-1],intial[i])]

                    if i!=1 and i!=0:
                        if ((sentence[i],pos) not in self.word_pos_frequency.keys())  or ((intial[i-1],intial[i]) not in self.transition_prob.keys()) or ((intial[i-2],intial[i]) not in self.transition_prob_s3_s1.keys()) :
                            curr_prob=10**-10
                        else:
                            curr_prob=self.transition_prob[(intial[i-1],intial[i])]*self.transition_prob_s3_s1[(intial[i-2],intial[i])]*self.word_pos_frequency[(sentence[i],pos)]

                    if max_prob<curr_prob:
                            max_prob=curr_prob
                            max_pos=pos
                    #print(max_prob)
                    #print(max_pos)
                intial[i]=max_pos
                final_sample.append(intial)
                sample_counter+=1
        final_sequence=[]

        for i in range(len(sentence)):
            freq=[]
            for j in range(100):
                freq.append(final_sample[j][i])
            final_sequence.append(mode(freq))

        return final_sequence

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")





