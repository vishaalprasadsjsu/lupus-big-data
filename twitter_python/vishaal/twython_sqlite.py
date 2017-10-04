import sys
import urllib
import string
import simplejson
import sqlite3
import time
import datetime
from pprint import pprint
import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode #
from sqlalchemy import Text #
from sqlalchemy import DECIMAL
from sqlalchemy import Unicode
from sqlalchemy.sql import join
from types import *
from datetime import datetime, date, time
import keys

'''
Uses twython to make API calls to twitter 
This will output all data into a SQLITE database
'''

# search terms 
ids = ['lupus']
       
from twython import Twython
t = Twython(app_key=keys.app_key,
    app_secret=keys.app_secret, 
    oauth_token=keys.oauth_token, 
    oauth_token_secret=keys.oauth_token_secret)

Base = declarative_base()


class Messages(Base):
    __tablename__ = 'hashtags'
    
    id = Column(Integer, primary_key=True)  
    query = Column(String)
    tweet_id = Column(Integer, unique=True) 
    inserted_date = Column(DateTime)
    truncated = Column(String)
    language = Column(String)
    possibly_sensitive = Column(String)  ### NEW 
    coordinates = Column(String)
    retweeted_status = Column(String)
    created_at_text = Column(String)  
    created_at = Column(DateTime)
    content = Column(Text)
    from_user_screen_name = Column(String)
    from_user_id = Column(String)   
    from_user_followers_count = Column(Integer)  
    from_user_friends_count = Column(Integer)  
    from_user_listed_count = Column(Integer)  
    from_user_statuses_count = Column(Integer)  
    from_user_description = Column(String)  
    from_user_location = Column(String)  
    from_user_created_at = Column(String)  
    retweet_count = Column(Integer)
    entities_urls = Column(Unicode(255))
    entities_urls_count = Column(Integer)        
    entities_hashtags = Column(Unicode(255))
    entities_hashtags_count = Column(Integer)    
    entities_mentions = Column(Unicode(255))    
    entities_mentions_count = Column(Integer)  
    in_reply_to_screen_name = Column(String)    
    in_reply_to_status_id = Column(String)  
    source = Column(String)
    entities_expanded_urls = Column(Unicode(255)) 
    json_output = Column(String)
    entities_media_count = Column(Integer)
    media_expanded_url = Column(Text) 
    media_url = Column(Text) 
    media_type = Column(Text) 
    video_link = Column(Integer)
    photo_link = Column(Integer)
    twitpic = Column(Integer)
    
    def __init__(self, query, tweet_id, inserted_date, truncated, language, possibly_sensitive, coordinates, 
    retweeted_status, created_at_text, created_at, content, 
    from_user_screen_name, from_user_id, from_user_followers_count, from_user_friends_count,   
    from_user_listed_count, from_user_statuses_count, from_user_description,   
    from_user_location, from_user_created_at, retweet_count, entities_urls,entities_urls_count,         
    entities_hashtags, entities_hashtags_count,entities_mentions,entities_mentions_count, in_reply_to_screen_name, in_reply_to_status_id, source, entities_expanded_urls, json_output, 
    entities_media_count, media_expanded_url, media_url, media_type,video_link, photo_link,twitpic  
    ):        
        self.query = query
        self.tweet_id = tweet_id
        self.inserted_date = inserted_date
        self.truncated = truncated
        self.language = language
        self.possibly_sensitive = possibly_sensitive
        self.coordinates = coordinates
        self.retweeted_status = retweeted_status
        self.created_at_text = created_at_text
        self.created_at = created_at 
        self.content = content
        self.from_user_screen_name = from_user_screen_name
        self.from_user_id = from_user_id       
        self.from_user_followers_count = from_user_followers_count
        self.from_user_friends_count = from_user_friends_count
        self.from_user_listed_count = from_user_listed_count
        self.from_user_statuses_count = from_user_statuses_count
        self.from_user_description = from_user_description
        self.from_user_location = from_user_location
        self.from_user_created_at = from_user_created_at
        self.retweet_count = retweet_count
        self.entities_urls = entities_urls
        self.entities_urls_count = entities_urls_count        
        self.entities_hashtags = entities_hashtags
        self.entities_hashtags_count = entities_hashtags_count
        self.entities_mentions = entities_mentions
        self.entities_mentions_count = entities_mentions_count     
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.in_reply_to_status_id = in_reply_to_status_id
        self.source = source
        self.entities_expanded_urls = entities_expanded_urls
        self.json_output = json_output
        self.entities_media_count = entities_media_count
        self.media_expanded_url = media_expanded_url
        self.media_url = media_url
        self.media_type = media_type
        self.video_link = video_link
        self.photo_link = photo_link
        self.twitpic = twitpic
  

    def __repr__(self):
       return "<Organization, Sender('%s', '%s')>" % (self.from_user_screen_name,self.created_at)

def get_data(kid, max_id=None):
    try:
        d = t.search(q=kid, count = '100', result_type = 'recent', lang = 'en', max_id = max_id, tweet_mode='extended') 
        
    except Exception, e:
        print "Error reading id %s, exception: %s" % (kid, e)
        return None
    # print "d.keys(): ", d.keys()   
    # print "######## # OF STATUSES IN THIS GRAB: ", len(d['statuses'])
    # print "max_id VALUE USED FOR THIS GRAB-->", max_id
    return d
    
def write_data(self, d):   

    collisions = 0
    new_tweets = 0

    query = d['search_metadata']['query']
    
    number_on_page = len(d['statuses'])
    ids = []
    for entry in d['statuses']:
        json_output = str(entry)
        tweet_id = entry['id']
        inserted_date = datetime.now()
        truncated = entry['truncated']
        language = entry['lang']

        if 'possibly_sensitive' in entry:
            possibly_sensitive= entry['possibly_sensitive']
        else:
            possibly_sensitive = ''
        
        coordinates = []
        if 'coordinates' in entry and entry['coordinates'] != None:
            # print entry['coordinates']['coordinates']
            for coordinate in entry['coordinates']['coordinates']:
                # print coordinate, type(coordinate)
                coordinates.append(coordinate)
           
            coordinates = ', '.join(map(str, coordinates))							
            # print type(coordinates), len(coordinates), coordinates
        else:
            coordinates = ''
            
        if 'retweeted_status' in entry:
            retweeted_status = 'THIS IS A RETWEET --> DOUBLE-CHECK JSON'
        else:
            retweeted_status = ''  
        
        content = entry['full_text']
        # content = content.replace('\n','')

        created_at_text = entry['created_at']     
        created_at = datetime.strptime(created_at_text, '%a %b %d %H:%M:%S +0000 %Y')   
        created_at2 = created_at.strftime('%Y-%m-%d %H:%M:%S')   
    
        from_user_screen_name = entry['user']['screen_name']
        from_user_id = entry['user']['id'] 
        from_user_followers_count = entry['user']['followers_count']
        from_user_friends_count = entry['user']['friends_count']   
        from_user_listed_count = entry['user']['listed_count']
        from_user_statuses_count = entry['user']['statuses_count'] 
        from_user_description = entry['user']['description'] 
        from_user_location = entry['user']['location'] 
        from_user_created_at = entry['user']['created_at']
        
        retweet_count = entry['retweet_count'] 
        
        in_reply_to_screen_name = entry['in_reply_to_screen_name']
        in_reply_to_status_id = entry['in_reply_to_status_id']
        entities_urls_count = len(entry['entities']['urls'])    
        entities_hashtags_count = len(entry['entities']['hashtags'])   
        entities_mentions_count = len(entry['entities']['user_mentions']) 
    
        source = entry['source']          
        entities_urls = []
        entities_expanded_urls = []
        
        for link in entry['entities']['urls']:
            if 'url' in link:
                url = link['url']
                expanded_url = link['expanded_url']
                entities_urls.append(url)
                entities_expanded_urls.append(expanded_url)
            # else:
                # print "No urls in entry"
        
        entities_hashtags = []
        for hashtag in entry['entities']['hashtags']:
            if 'text' in hashtag:
                tag = hashtag['text']
                entities_hashtags.append(tag)
            # else:
                # print "No hashtags in entry"
        
        entities_mentions = []
        for at in entry['entities']['user_mentions']:
            if 'screen_name' in at:
                mention = at['screen_name']
                entities_mentions.append(mention)
            # else:
                # print "No mentions in entry"
                
        entities_mentions = string.join(entities_mentions, u", ")
        entities_hashtags = string.join(entities_hashtags, u", ")
        entities_urls = string.join(entities_urls, u", ")
        entities_expanded_urls = string.join(entities_expanded_urls, u", ")    
        
        video_link = 0
        if 'vimeo' in entities_expanded_urls or 'youtube' in entities_expanded_urls or 'youtu' in entities_expanded_urls or 'vine' in entities_expanded_urls:
            video_link = 1					
            # print "Found video"
        else:
            video_link = 0
            
        if 'twitpic' in entities_expanded_urls:
            twitpic = 1						
            # print "Found a twitpic link"
        else:
            twitpic = 0
        if 'twitpic' in entities_expanded_urls or 'instagram' in entities_expanded_urls or 'instagr' in entities_expanded_urls:
            photo_link = 1					
            # print "Found a twitpic or instagram link"
        else:
            photo_link = 0

       
        entities_urls = unicode(entities_urls)
        entities_expanded_urls = unicode(entities_expanded_urls)
        entities_hashtags = unicode(entities_hashtags)
        entities_mentions = unicode(entities_mentions)
    
        # print "urls...?....", 
        # print "user_mentions...?....", 
        # print "hashtags...?....", 
        

      #   if 'symbols' in entry['entities']:
		    # print "HERE ARE THE SYMBOLS.......", 
      #   else:
		    # print "NO entry['entities']['symbols']"
		
        if 'media' in entry['entities']:
			# print "HERE ARE THE MEDIA.......", #entry['entities']['media']
			entities_media_count = len(entry['entities']['media'])   
        else:
            entities_media_count = ''
        

        if 'media' in entry['entities']:
            if 'expanded_url' in entry['entities']['media'][0]:
		        media_expanded_url = entry['entities']['media'][0]['expanded_url']
            else:
                # print "NO expanded_url in entry['entities']['media']"
                media_expanded_url = ''
					    
            if 'media_url' in entry['entities']['media'][0]:
		        media_url = entry['entities']['media'][0]['media_url']
            else:
		        # print "NO media_url in entry['entities']['media']"
		        media_url = ''
					    
            if 'type' in entry['entities']['media'][0]:
		        media_type = entry['entities']['media'][0]['type']
            else:
		        # print "NO type in entry['entities']['media']"
		        media_type = ''
        else:
		    media_type = ''
		    media_url = ''
		    media_expanded_url = ''


      
        # updates = self.session.query(Messages).filter_by(query=query, from_user_screen_name=from_user_screen_name,
                # content=content).all() 
        # if not updates:
            # print "inserting, query:", query                   

        # only add if tweet's content contains keyword 
        # if (query.lower() in content.lower()): 

                    
        upd = Messages(query, tweet_id, inserted_date, truncated, language, possibly_sensitive, 
            coordinates, retweeted_status, created_at_text, 
            created_at, content, from_user_screen_name, from_user_id, from_user_followers_count, 
            from_user_friends_count, from_user_listed_count, from_user_statuses_count, from_user_description,   
            from_user_location, from_user_created_at, retweet_count, entities_urls, entities_urls_count,         
            entities_hashtags, entities_hashtags_count, entities_mentions,entities_mentions_count, in_reply_to_screen_name, in_reply_to_status_id, source, entities_expanded_urls, json_output, 
            entities_media_count, media_expanded_url, media_url, media_type,video_link, photo_link,twitpic
            )
        self.session.add(upd)
      
                
        # else:
        #     if len(updates) > 1:
        #         print "Warning: more than one update matching to_user=%s, text=%s"\
        #                 % (to_user, content)
        #     else:
        #         print "Not inserting, dupe.."
        
        # self.session.commit()

        try:
            self.session.commit()
            new_tweets += 1
        except:
            self.session.rollback()
            collisions += 1

    print "\t", new_tweets, "\t", collisions

class Scrape:
    def __init__(self):    
        engine = sqlalchemy.create_engine("sqlite:///en_lupus.sqlite", echo=False)  
        Session = sessionmaker(bind=engine)
        self.session = Session()  
        Base.metadata.create_all(engine)

    def main(self):

        for n, kid in enumerate(ids):
            print "\rprocessing id %s/%s" % (n+1, len(ids)),
            sys.stdout.flush()
            print ""

            print "Page\tnew\tcollisions"

            d = get_data(kid)
            if not d:
                continue	 
            
            if len(d['statuses'])==0:
                print "No statuses returned -- moving to next ID"
                continue
                
            write_data(self, d) 

            self.session.commit() 
                    
            last_status = d['statuses'][-1]
            min_id = last_status['id']
            
            max_id = min_id-1        
            # print 'THIS IS THE min_id IN THE CURRENT SET OF TWEETS: ', max_id
           
            if len(d['statuses']) >1:
          
                # print "THERE WAS AT LEAST 1 STATUS ON THE FIRST PAGE! NOW MOVING TO GRAB EARLIER TWEETS"

                count = 2
                max_count = 40
                while count < max_count:
                    print "\r%s" % (count),
                    sys.stdout.flush()

                    d = get_data(kid, max_id)
                    
                    if not d:
                        break
                    elif not d['statuses']:
                        break	
                    
                    last_status = d['statuses'][-1]
                    min_id = last_status['id']
                  
                    max_id = min_id-1
                    # print 'THIS IS THE min_id IN THE CURRENT SET OF TWEETS: ', max_id

                    if not d:
                        continue	       

                    write_data(self, d) 
                    self.session.commit()
                    
                    # print "FINISHED WITH PAGE", len(d['statuses']), count
                    # print "finished page ", count
                    if not len(d['statuses']) > 0:

                        print "REACHED THE LAST PAGE -- MOVING TO NEXT ID"
                        break                    
                    count += 1
                    if count > max_count:
                        print "At page ", max_count
                        break
            self.session.commit()

        self.session.close()


if __name__ == "__main__":
    s = Scrape()
    s.main()
