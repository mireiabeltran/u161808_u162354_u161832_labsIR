This project is in process of development

# FINAL PROJECT IRWA: TWEETS BASED SEARCH ENGINE

This project aims to build a search engine implementing different indexing and ranking
algorithms. This will be done using a file containing a set of tweets from the World Health
Organization (@WHO). 


It will be divided in four parts:
  1) Text processing
  2) Indexing and ranking
  3) Evaluation 
  4) User Interface and Web analytics

### SETUP Notes
In order to run the code, the installation of 'nltk' and 'regex' module is needed and 
the file 'dataset_tweets_WHO.txt' must be placed in this folder. After this, the code
is ready to run.

When runing the evaluation part, the following installation is needed:

- !pip install gensim==3.0
- !pip install tsne

## 1) TEXT PROCESSING

In the first part of the project, it has been pre-processed the document. To do so we have stemmed terms, 
removed stop-words, punctuation, links and emojis, we have performed a tokenization in order to get a 
list of the terms and we have transformed all text to lowercase. As for the hashtags, we decided not 
to remove them since it may be interesting to identify them and treat them separately later.

For example, from this text: 

![image](https://user-images.githubusercontent.com/93143576/139066531-8a7efff6-141c-4e33-9f76-e8e28c8373e8.png)

We obtain: 

![image](https://user-images.githubusercontent.com/93143576/139066915-7974d92d-acf6-4887-9c00-b2d6df9b0fc7.png)

## 2)  INDEXING and EVALUATION

In the next part, it has been implemented the inverted index of the tweets and a ranking function, and it has been evaluated the algorithm.
based on a query. When doing the full inverted index we get the terms as keys and the corresponding list of tweets where these keys appears in 
(and the positions) as values. This can be used afterwards to parse a query and determine the most important tweets based on the times that the words of 
the query appear in the tweets. 

For example, with the query 'global pandemic', we get the next:
![image](https://user-images.githubusercontent.com/93143576/141695035-b97af30a-3bd7-4aa6-94d1-def5195c5cc4.png)

In order to evaluate the algorithm, the following evaluation techniques have been used and commented:
    ▪ Precision@K (P@K)
    ▪ Average Precision@K (P@K)
    ▪ Mean Average Precision (MAP)
    ▪ Mean Reciprocal Rank (MRR)
    ▪ Normalized Discounted Cumulative Gain (NDCG)

Finally, a Word2Vec model has been trained and the t-sne algorithm has been used to be able to represent the tweets in a
two-dimensional scatter plot. 


