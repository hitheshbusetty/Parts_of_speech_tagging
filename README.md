# Parts_of_speech_tagging

Aim: to find the parts of speech for the words in the snetence.
observed variables: words in states

Training the model:
 while training the model with large set of labeled training data, we have created the following dictionaries which will help in calculating the emission and transition probability of Bayes net.

word_frequency: this dictionary will store how many times a word is present the given training data
pos_frequency:  this dictionary will store how many times a particular part of speech
word_pos_frequency: this dictionary will store how many times a combination of word and part of speech is repeated in training data
transition_frequency: this dictionary will store how many times a combination of two parts of speech repeated one after other in training data

1) Simplified Bayes net:
<img width="270" alt="Screen Shot 2021-12-03 at 9 03 07 PM" src="https://media.github.iu.edu/user/18547/files/0600be80-547d-11ec-8681-0b473fecb5fe">

we have calculated fixed the part of speech tag to the word by maximizing the P(parts of speech/word).
P(S/w) = P(s,w)/P(w) = frequency of word and part of speech  in training set/ frequency of word in training set

if the given word is not present in training set, we have assigned "noun" to the word.

for calulating the posterior. we have multiplied emission probability p(w/s) for all the words and respective labels and applied logarithm to it.

2)

<img width="289" alt="Screen Shot 2021-12-03 at 9 35 52 PM" src="https://media.github.iu.edu/user/18547/files/10bd5280-5481-11ec-9041-645954a69860">


for this bayes net, we have used viterbi algorithm.

In v-table the intial probabilites are calculated by multiplying the emission probability P(w/s) and probability that sentence starts with this parts of speech

the probabilties at the other time steps is calculated by multiplying  emission probability P(w/s) and P(Si/Si-1) and vi(t-1)

for back tracking, we have implemented the which table which stores the  POS for which we got maximum product of P(Si/Si-1) and vi(t-1).

if the word is not present in training set, i have given very small probability of 10**-10 in the v-table.

3) Complex bayes net:

<img width="291" alt="Screen Shot 2021-12-03 at 9 36 48 PM" src="https://media.github.iu.edu/user/18547/files/2df22100-5481-11ec-8e5e-e44d920ea36d">


we have mcmc algorithm for this bayes net to calculate the max probability of mcmc sequence.

we have the taken intial sequence as all nouns.

after that we have created 100 samples using gibbs sampling and assinged parts of speech which is most repeated to the word 








  
  


