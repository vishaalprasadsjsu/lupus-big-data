from py2neo import Graph
import re, string

from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:76877", auth=basic_auth("neo4j", "neo4j"))
session = driver.session()


# default uri for local Neo4j instance
graphdb = Graph('http://neo4j:neo4j@localhost:7474/db/data')

# parameterized Cypher query for data insertion
# t is a query parameter. a list with two elements: [word1, word2]
INSERT_QUERY = '''
    FOREACH (t IN {wordPairs} |
        MERGE (w0:Word {word: t[0]})
        MERGE (w1:Word {word: t[1]})
        CREATE (w0)-[:NEXT_WORD]->(w1)
        )
'''

# convert a sentence string into a list of lists of adjacent word pairs
# also convert to lowercase and remove punctuation using a regular expression
# arrifySentence("Hi there, Bob!) = [["hi", "there"], ["there", "bob"]]
def arrifySentence(sentence):
    sentence = sentence.lower()
    sentence = sentence.strip()
    exclude = set(string.punctuation)
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    sentence = regex.sub('', sentence)
    wordArray = sentence.split()
    tupleList = []
    for i, word in enumerate(wordArray):
        if i+1 == len(wordArray):
            break
        tupleList.append([word, wordArray[i+1]])
    return tupleList

# load our text corpus into Neo4j
def loadFile():
    tx = graphdb.begin()
    with open('../twitter_python/twython_data.txt', encoding='UTF-8') as f:
        count = 0
        for l in f:
            params = {'wordPairs': arrifySentence(l)}
            tx.append(INSERT_QUERY, params)
            tx.process()
            count += 1
            # process in batches of 100 insertion queries
            if count > 100:
                tx.commit()
                tx = graphdb.begin()
                count = 0
    f.close()
    tx.commit()
