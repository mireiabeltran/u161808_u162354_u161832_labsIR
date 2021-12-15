import random
from app.search_engine.algorithms import search_us
from app.core.utils import get_random_date
from datetime import timedelta, datetime
import time
from app.analytics.analytics_data import *

def build_demo_data():
    """
    Helper method, just to demo the app
    :return: a list of demo docs sorted by ranking
    """
    samples = ["Messier 81", "StarBurst", "Black Eye", "Cosmos Redshift", "Sombrero", "Hoags Object",
            "Andromeda", "Pinwheel", "Cartwheel",
            "Mayall's Object", "Milky Way", "IC 1101", "Messier 87", "Ring Nebular", "Centarus A", "Whirlpool",
            "Canis Major Overdensity", "Virgo Stellar Stream"]

    res = []
    for index, item in enumerate(samples):
        res.append(DocumentInfo(item, (item + " ") * 5, get_random_date(),
                                "doc_details?id={}&param1=1&param2=2".format(index), random.random()))
    # simulate sort by ranking
    res.sort(key=lambda doc: doc.ranking, reverse=True)
    return res


class SearchEngine:
    """educational search engine"""
    i = 12345
    def __init__(self):
        self.start = time.time()
        self.query_time = datetime.now()

    def search(self, search_query):
        print("Search query:", search_query)
        results = []
        ##### your code here #####
        AnalyticsData.fact_query.append(Query(self.query_time, search_query.split(), len(search_query.split())))
        AnalyticsData.fact_date.append(Date(self.query_time))
        AnalyticsData.fact_terms.append(Terms(search_query.split()))
        AnalyticsData.fact_nterms.append(nTerms(len(search_query.split())))
        results = search_us(search_query)  # replace with call to search algorithm
        ##### your code here #####

        return results


class DocumentInfo:
    def __init__(self, id, title, description, likes, retweets, url, ranking, date):
        self.id = id
        self.title = title
        self.description = description
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.ranking = ranking
        self.date = date
