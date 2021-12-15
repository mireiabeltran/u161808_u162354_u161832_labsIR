#from scipy.special import logsumexp
from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
import numpy as np
import collections
from numpy import linalg as la
# if you do not have 'nltk', the following command should work "python -m pip install nltk"
import nltk
nltk.download('stopwords')
from collections import defaultdict
from array import array
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import math
import numpy as np
import collections
#from numpy import linalg as la
import json
import regex as re 
import string
from app.core import utils
from app.search_engine import search_engine

#Load data into memory


#Dataset Creation
import pandas as pd

# Build DataFrame of tweet texts and languages
tweets_data = utils.load_documents_corpus()

#create a new variable called 'texts' which will contain in each position of the array a tweet
texts=[]
for i in range(len(tweets_data)):
    line =  tweets_data[i].description
    texts.append(str(line))

#Text Processing
def build_terms(text):
    """
    Preprocess the article text (title + body) removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.
    
    Argument:
    text -- string (text) to be preprocessed
    
    Returns:
    text - a list of tokens corresponding to the input text after the preprocessing
    """
    # create the pattern
    stemmer = PorterStemmer()
    
    stop_words = set(stopwords.words("english"))
    remove = string.punctuation
    remove = remove.replace("#", "–")# don't remove hashtags
    remove = remove+'¿'
    pattern = r"[{}]".format(remove) # create the pattern
    text = re.sub(pattern, "", text)
    text = re.sub(r'http\S+', '', text)
    
    #compile a regular expression pattern into a regular expression object
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
                        "]+", flags=re.UNICODE)
    #Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement
    text = emoji_pattern.sub(r'', text) # no emoji
    
    # Transform in lowercase
    text=  str.lower(text) 
    # Tokenize the text to get a list of terms
    text=  text.split() 
    # Eliminate the stopwords
    text=[l for l in text if l not in stop_words] 
    

    # Perform stemming 
    text=[stemmer.stem(word) for word in text]
    
    return text

texts_processed = []
for i in range(len(texts)):
    texts_processed.append(build_terms(texts[i]))

#index and evaluation
def create_index(texts, num_documents):
    """
    Implement the inverted index
    
    Argument:
    lines -- collection of Wikipedia articles
    
    Returns:
    index - the inverted index (implemented through a Python dictionary) containing terms as keys and the corresponding
    list of documents where these keys appears in (and the positions) as values.
    idf,tf,df """
    
    index = defaultdict(list)
    tf = defaultdict(list)  #term frequencies of terms in documents (documents in the same order as in the main index)
    df = defaultdict(int)  #document frequencies of terms in the corpus
    title_index = {}  # dictionary to map page titles to page ids
    idf = defaultdict(float)
    tweet_id = 0
    for text in texts:  # Remember, lines contain all documents
        terms = build_terms(text) #page_title + page_text
        tweet_id += 1
        title_index[tweet_id]=text  
        
        
        doc_freq = {i:terms.count(i) for i in terms}
        current_page_index = {}
        
        for position, term in enumerate(terms): # terms contains page_title + page_text. Loop over all terms
            
            try:
                # if the term is already in the index for the current page (current_page_index)
                # append the position to the corresponding list
                

                current_page_index[term][1].append(position)  
            except:
                # Add the new term as dict key and initialize the array of positions and add the position
                current_page_index[term] = [tweet_id, array('I',[position])] #'I' indicates unsigned int (int in Python)
        
        norm = 0
        for term, posting in current_page_index.items():
            # posting will contain the list of positions for current term in current document. 
            # posting ==> [current_doc, [list of positions]] 
            # you can use it to infer the frequency of current term.
            norm += len(posting[1]) ** 2
        norm = math.sqrt(norm)
            

        #calculate the tf(dividing the term frequency by the above computed norm) and df weights
        for term, posting in current_page_index.items():
            # append the tf for current term (tf = term frequency in current doc/norm)
            tf[term].append(np.round(len(posting[1])/norm,4)) ## SEE formula (1) above
            #increment the document frequency of current term (number of documents containing the current term)
            df[term] +=1 # increment DF for current term

        #merge the current page index with the main index
        for term_page, posting_page in current_page_index.items():
            index[term_page].append(posting_page)

        # Compute IDF following the formula (3) above. HINT: use np.log
        for term in df:
            idf[term] = np.round(np.log(float(num_documents/df[term])), 4)

    return index, tf, df, idf, title_index

index, tf, df, idf, title_index = create_index(texts, len(texts))


retweets=[]
likes=[]
for i in range(len(tweets_data)):
    ret =  tweets_data[i].retweets
    like =  tweets_data[i].likes
    retweets.append(ret)
    likes.append(like)

likes = np.array(likes)
likes2 = likes.copy()
ret2 = retweets.copy()
retweets = np.array(retweets)
likes = likes/np.linalg.norm(likes)
retweets = retweets/np.linalg.norm(retweets)

def search_us(search_query):
    def rank_documents_modified(terms, docs, index, idf, tf, title_index):
        """
        Perform the ranking of the results of a search based on the tf-idf weights
        
        Argument:
        terms -- list of query terms
        docs -- list of documents, to rank, matching the query
        index -- inverted index data structure
        idf -- inverted document frequencies
        tf -- term frequencies
        title_index -- mapping between page id and page title
        
        Returns:
        Print the list of ranked documents
        """

        # I'm interested only on the element of the docVector corresponding to the query terms 
        # The remaining elements would became 0 when multiplied to the query_vector
        doc_vectors = defaultdict(lambda: [0] * len(terms)) # I call doc_vectors[k] for a nonexistent key k, the key-value pair (k,[0]*len(terms)) will be automatically added to the dictionary
        query_vector = [0] * len(terms)

        # compute the norm for the query tf
        query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query. 
        # Example: collections.Counter(["hello","hello","world"]) --> Counter({'hello': 2, 'world': 1})
        #HINT: use when computing tf for query_vector

        query_norm = la.norm(list(query_terms_count.values()))

        for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
            if term not in index:
                continue

            ## Compute tf*idf(normalize TF as done with documents)
            query_vector[termIndex]=query_terms_count[term]/query_norm * idf[term] 

            # Generate doc_vectors for matching docs
            for doc_index, (doc, postings) in enumerate(index[term]):
                # Example of [doc_index, (doc, postings)]
                # 0 (26, array('I', [1, 4, 12, 15, 22, 28, 32, 43, 51, 68, 333, 337]))
                # 1 (33, array('I', [26, 33, 57, 71, 87, 104, 109]))
                # term is in doc 26 in positions 1,4, .....
                # term is in doc 33 in positions 26,33, .....

                #tf[term][0] will contain the tf of the term "term" in the doc 26    
                if doc in docs:
                    doc_vectors[doc][termIndex] = tf[term][doc_index] * (0.75*retweets[doc_index]+0.25*likes[doc_index])  # TODO: check if multiply for idf

        # Calculate the score of each doc 
        # compute the cosine similarity between queyVector and each docVector:
        # HINT: you can use the dot product because in case of normalized vectors it corresponds to the cosine similarity
        # see np.dot
        
        doc_scores=[[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items() ]
        doc_scores.sort(reverse=True)
        result_docs = [x[1] for x in doc_scores]
        #print document titles instead if document id's
        #result_docs=[ title_index[x] for x in result_docs ]
        if len(result_docs) == 0:
            print("No results found, try again")
            query = input()
            docs = search_modified(query, index)
        #print ('\n'.join(result_docs), '\n')
        return result_docs, doc_scores

    def search_modified(query, index):
        """
        The output is the list of documents that contain any of the query terms. 
        So, we will get the list of documents for each query term, and take the union of them.
        """
        query = build_terms(query)
        docs = set()
        for term in query:
        ## START DODE
            try:
                # store in term_docs the ids of the docs that contain "term"                        
                term_docs=[posting[0] for posting in index[term]]
                # docs = docs intersection term_docs
                if len(docs)==0:
                    docs |= set(term_docs)
                else:
                    docs = docs.intersection(set(term_docs))
            except:
                #term is not in index
                pass
        docs = list(docs)
        ranked_docs, scores = rank_documents_modified(query, docs, index, idf, tf, title_index)
        return ranked_docs, scores

    #DOC INFO
    
    docs,scores = search_modified(search_query, index)

    top =20
    results_ = []
    c=0
    
    for d_id in docs[:top]:
        date = tweets_data[d_id].date
        title = tweets_data[d_id].title
        results_.append(search_engine.DocumentInfo(d_id, title, title_index[d_id], likes2[d_id], ret2[d_id], 'doc_details?id={}&title={}&text={}&likes={}&retweets={}&date={}'.format(d_id, title, title_index[d_id], likes2[d_id], ret2[d_id], date),c, date))
        c+=1
    
    return results_
        




        



