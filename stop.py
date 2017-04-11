import operator 
import json
import sys
from collections import Counter
from collections import defaultdict

import string
 
punctuation = list(string.punctuation)

import re	

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


search_word = sys.argv[1] # pass a term as a command-line argument
count_search = Counter()


stop = punctuation + ['de', 've','ki','ya','da','gibi','bir','bu','spoiler','ş','o','çok','ama','için','ne','ile','daha','bkz','şey','ben']
com = defaultdict(lambda : defaultdict(int))
fname = 'eksi-data'
with open(fname, 'r') as f:
    count_all = Counter()
    for line in f:
        a_split = line.split(';')
        #tweet = json.loads(line)
        # Create a list with all the terms
        terms_only = [term for term in preprocess(a_split[1]) if term not in stop]
        # Update the counter
        count_all.update(terms_only)
        if search_word in terms_only:
            count_search.update(terms_only)
    # Print the first 5 most frequent words
    #print("Co-occurrence for %s:" % search_word)
    print(count_all.most_common(20))
    print("Co-occurrence for %s:" % search_word)
    print(count_search.most_common(20))

