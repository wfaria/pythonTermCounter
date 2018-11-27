# Library imports.
from flask import abort, Flask, jsonify, make_response, redirect, request
from redis import Redis, RedisError
import os
import socket
import time

# Local file imports.
from term_parser import *

# Connecting to Redis.
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

# Declaring flask application object.
app = Flask(__name__)
   
@app.route('/<string:term>', methods=['GET'])
def get_term_count(term):
    '''
    Route handler to access the number of time that the
    string 'term' parameter appeared on the files processed
    by our server.
    
    We will compare it removing elements like accents and other
    diacritics to avoid duplicated terms.
    '''
    start = time.clock()
    countValue = redis.get(get_term_key(term))
    if (countValue is None):
        countValue = 0
    else:
        countValue = int(countValue)
    
    totalTime = time.clock() - start
    ret = {"count": countValue, "processTime" : totalTime}
    return jsonify(ret), 200

def get_term_key(term):
    '''
    Small method to create the key used on Redis
    to access the count value of each term processed by this server.
    '''
    return "termcounter:{0}".format(sanitize_text(term))
    
@app.route('/load_default', methods=['GET'])
def load_default():
    '''
    Route handler to get all terms from a default set
    of text files. This should be called after creating
    a new empty Redis database.
    '''
    start = time.clock()
    defaultTerms = count_from_default_files()    
    try:
        store_term_count(defaultTerms)            
    except RedisError:
        abort(500);
    
    totalTime = time.clock() - start
    ret = {"updatedTerms": len(defaultTerms), "processTime" : totalTime}
    return jsonify(ret), 200
    
def store_term_count(termCount):
    '''
    Auxiliar method which receives a sanitized dictionary
    with <term, count> and insert each tuple on Redis database.
    '''
    for term, value in termCount.iteritems():
        redis.incrby(get_term_key(term), value)
    
@app.route('/upload_terms', methods=['POST'])
def upload_terms():
    '''
    Route handler for post request to insert new terms.
    It expects to receive a text on the post body using utf-8 encode.
    It will process it, cleaning the text and spliting it into multiple terms
    to create/increase the count amount stored on the database.
    '''
    start = time.clock()
    termCount = {}
    termCount = count_terms(request.get_data(as_text=True), termCount)
    try:
        store_term_count(termCount)            
    except RedisError:
        abort(500);
    
    totalTime = time.clock() - start
    ret = {"updatedTerms": len(termCount), "processTime" : totalTime}
    return jsonify(ret), 201

@app.route("/")
def hello():
    '''
    Test route for demonstration.
    '''
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>Cannot connect to Redis, counter disabled.</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(threaded=True)
