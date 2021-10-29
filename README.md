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
Installation of 'nltk' and 'regex' module is needed. 

## 1) TEXT PROCESSING

In the first part of the project, it has pre-processed the document. To do so we have stemmed terms, removed stop-words, punctuation, links and emojis, we have performed a tokenization in order to get a list of the terms and we have transformed all text to lowercase. As for the hashtags, we decided not to remove them since it may be interesting to identify them and treat them separately later.

For example, from this text: 

![image](https://user-images.githubusercontent.com/93143576/139066531-8a7efff6-141c-4e33-9f76-e8e28c8373e8.png)

We obtain: 

![image](https://user-images.githubusercontent.com/93143576/139066915-7974d92d-acf6-4887-9c00-b2d6df9b0fc7.png)


- Stem terms
- Remove stop words
- Remove punctuation 
- Remove links
- Remove emojis
- Transform all text to lowercase
- Tokenize the text to get a list of terms

