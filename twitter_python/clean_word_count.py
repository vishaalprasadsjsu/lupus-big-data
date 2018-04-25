import operator 
from collections import Counter
from nltk.corpus import stopwords
import string
import re
from nltk import bigrams 
from collections import defaultdict
import vincent 

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
# for co-occurrences 
com = defaultdict(lambda : defaultdict(int))

# file
fname = 'tweet_content.txt'

# for co-occurrences
search_word = 'Lupus'

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
    count_search = Counter()
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

        # for all co-occurrences
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1

        # for search word co-occurrences
        if search_word in terms_only:
            count_search.update(terms_only)


'''
Custom co-occurrence lookup 
'''
# search_word = 'sys.argv[1]' # pass a term as a command-line argument
print("Co-occurrence for %s:" % search_word)
print(count_search.most_common(20))
print()


'''
Co-occurrences 
'''
com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print("co-occurrences")
print(terms_max[:5])


'''
Most frequent terms 
'''
print()
# most frequent words (not cleaned, includes punctuation etc.)
print("Most common (not clean)")
print(count_all.most_common(5))
print()

# most frequent words, cleaned 
print("Most common (clean)")
print(count_terms_only.most_common(5))
print()

print("Bigram (clean)")
print(terms_only_bigram.most_common(10))
print()

# most hashtags
print("Most common Hashtags")
print(count_hash.most_common(5))

'''
Vincent, run with: 
$ python3 -m http.server 8888
'''
# word_freq = terms_only_bigram.most_common(10)
word_freq = count_terms_only.most_common(10)
labels, freq = zip(*word_freq)
data = {'data': freq, 'x': labels}
bar = vincent.Bar(data, iter_idx='x')
bar.to_json('term_freq.json')
