import nltk
from flask import Flask, render_template
from flask import request
import httpagentparser 
from app.analytics.analytics_data import *
from app.core import utils
from app.search_engine.search_engine import SearchEngine
from datetime import timedelta, datetime
import time
app = Flask(__name__)

searchEngine = SearchEngine()
analytics_data = AnalyticsData()
corpus = utils.load_documents_corpus()


@app.route('/')
def search_form():
    browser = request.user_agent.browser
    platform = request.user_agent.platform
    language = request.user_agent.version
    user_agent = request.headers.get('User-Agent')
    print('Raw User Agent', user_agent)
    user_ip = request.remote_addr
    print("IP", user_ip)

    analytics_data.user.append(user_ip)
    analytics_data.user.append(browser)
    analytics_data.user.append(platform)
    analytics_data.user.append(language)
    agent = httpagentparser.detect(user_agent)
    
    return render_template('index.html', page_title="Welcome")


@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    results = searchEngine.search(search_query)
    found_count = len(results)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)


@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')
    clicked_doc_id = int(request.args["id"])
    analytics_data.fact_clicks.append(Click(clicked_doc_id))
    click_time = time.time()
    time_elapsed = click_time-searchEngine.start
    analytics_data.fact_time.append(Time(clicked_doc_id, time_elapsed))

    doc= corpus[int(clicked_doc_id)]

    id = int(request.args.get('id'))
    text = request.args.get('text')
    likes = request.args.get('likes')
    retweets = request.args.get('retweets')
    date = request.args.get('date')
    title = request.args.get('title')

    print("click in id={} - fact_clicks len: {}".format(clicked_doc_id, len(analytics_data.fact_clicks)))

    return render_template('doc_details.html', doc=doc, id = id, title= title, text = text, likes = likes, retweets = retweets, date=date )


@app.route('/stats', methods=['GET'])
def stats():
    """
    Show simple statistics example. ### Replace with dashboard ###
    :return:
    """
    ### Start replace with your code ###
    times={}
    clicks = {}
    for time in analytics_data.fact_time:
        if time.doc_id not in clicks:
            clicks[time.doc_id] = 1
        else:
            clicks[time.doc_id] = clicks[time.doc_id] + 1

        if time.doc_id not in times:
            times[time.doc_id] = [time.time]
        else:
            times[time.doc_id].append(time.time)

    #for clk in analytics_data.fact_clicks:
        ##docs.append(clk.doc_id)
    ip = analytics_data.user[0]
    browser = analytics_data.user[1]
    platform = analytics_data.user[2]
    language = analytics_data.user[3]
    time = analytics_data.fact_time[0].time
    date = analytics_data.fact_date
    _Terms = analytics_data.fact_terms
    _nTerms = analytics_data.fact_nterms
    query= analytics_data.fact_query
    return render_template('stats.html',query=query, browser=browser, language=language,platform=platform,ip=ip,times=times, clicks = clicks, date=date, terms=_Terms, nterms=_nTerms)
    ### End replace with your code ###

@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port="8088", host="0.0.0.0", threaded=False, debug=True)
