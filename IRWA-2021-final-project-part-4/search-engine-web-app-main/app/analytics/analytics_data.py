class AnalyticsData:
    fact_clicks = []
    fact_time = []
    fact_query = []
    fact_date = []
    fact_terms = []
    fact_nterms = []
    user=[]



class Click:
    def __init__(self, doc_id):
        self.doc_id = doc_id

class Time:
    def __init__(self, doc_id, time):
        self.doc_id = doc_id
        self.time = time

class Query:
    def __init__(self, date,terms,nterms):
        self.date = date
        self.terms = terms
        self.nterms = nterms
class Date:
    def __init__(self, date):
        self.date = date
class Terms:
    def __init__(self,terms):
        self.terms = terms
        

class nTerms:
    def __init__(self,nterms):
        self.nterms = nterms

