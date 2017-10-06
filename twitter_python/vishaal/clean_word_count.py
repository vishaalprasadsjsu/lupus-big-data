import operator 
from collections import Counter
from nltk.corpus import stopwords
import string
import re
from nltk import bigrams 

'''
Counts the most frequent words in a text file

Output:
    First - uncleaned frequent word count (includes punctuation etc.)
    Second - cleaned frequent word count 
'''

 # stop words (insignificant words)
punctuation = list(string.punctuation)
# rt and via specific to this project, add them
stop = stopwords.words('english') + punctuation + ['RT', 'via'] 

fname = 'twython_data.txt'

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

# print common terms (not clean)
with open(fname, 'r') as f:
    count_all = Counter()
    count_hash = Counter()
    count_terms_only = Counter()
    terms_only_bigram = Counter()
    for line in f:
    	# for json: 
        # tweet = json.loads(line)

        # for plain text:

        # Create a list with all the terms
        terms_all = [term for term in preprocess(line)]
        # Update the counter
        count_all.update(terms_all)

        # clean data for a single tweet 
        terms_single = set(terms_all)
        # Count hashtags only
        terms_hash = [term for term in preprocess(line) 
                      if term.startswith('#')]
        # Count terms only (no hashtags, no mentions)
        terms_only = [term for term in preprocess(line) 
                      if term not in stop and
                      not term.startswith(('#', '@'))] 
                      # mind the ((double brackets))
                      # startswith() takes a tuple (not a list) if 
                      # we pass a list of inputs
        terms_only_bigram.update(bigrams(terms_only))
        count_terms_only.update(terms_only)
        count_hash.update(terms_hash)

# most frequent words (not cleaned, includes punctuation etc.)
print "Most common (not clean)"
print(count_all.most_common(5))

# most frequent words, cleaned 
print "Most common (clean)"
print(count_terms_only.most_common(5))

print "Bigram (clean)"
print(terms_only_bigram.most_common(10))

# most hashtags
print "Most common Hashtags"
print(count_hash.most_common(5))


