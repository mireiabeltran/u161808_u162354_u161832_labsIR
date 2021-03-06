This project is in process of development

# FINAL PROJECT IRWA: TWEETS BASED SEARCH ENGINE

This project aims to build a search engine implementing different indexing and ranking
algorithms. This will be done using a file containing a set of tweets from the World Health
Organization (@WHO). 


It will be divided in four parts:
  1) Text processing
  2) Indexing and evaluation
  3) Ranking 
  4) User Interface and Web analytics

### SETUP Notes
In order to run the code, the installation of 'nltk' and 'regex' module is needed and 
the file 'dataset_tweets_WHO.txt' must be placed in this folder. After this, the code
is ready to run.

When runing the evaluation part, the following installation is needed:

- !pip install gensim==3.0
- !pip install tsne

It might be the case that when doing a "run all" in the python notebook, the following import does not work: from gensim.models.word2vec import Word2Vec. To solve it it is 
just needed to run again this cell and it will work without any problem.

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
- Precision@K (P@K)
- Average Precision@K (P@K)
- Mean Average Precision (MAP)
- Mean Reciprocal Rank (MRR)
- Normalized Discounted Cumulative Gain (NDCG)

Finally, a Word2Vec model has been trained and the t-sne algorithm has been used to be able to represent the tweets in a
two-dimensional scatter plot. 

# 3) RANKING

In the third part, it has been carried out the ranking score. In three ways: tf-idf, tf + number of retweets(75% importance) and favourites(25% importance), and word2vec.
In all the approaches cosine similarity was applied somehow. 

When using the word2vec representation, the cosine similarity was applied in the following way: A query2vec was created for each query and then, for each tweet that contains the query words the cosine similarity was computed doing the np.dot between the tweet vector and the query vector. However, instead of applying a pure cosine similarity by normalizing the cosine similarity, the formula of favourites and retweets was used to rank the tweets. In this part relevance was also implemented in order to give more importance to the tweets with more likes and retweets. 

As result, we obtained that the second approach had sense and the tweets where ranked according to the afforementioned criteria. On the other hand, the rankings of the first and the third approaches return similar tweet ids. 

In conclusion, we believe that the tweet2vec representation, which is the modified version of word2vec, returns the best result since when normalizing it with pure cosine similarity all the retrieved tweets had a cosine similarity bigger than 0,999 and in this case it can be observed that it has a wider range of scores. 

