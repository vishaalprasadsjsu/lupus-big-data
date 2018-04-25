import sqlalchemy
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Unicode #
from sqlalchemy import Text #
from sqlalchemy import DECIMAL
from sqlalchemy import Unicode
from sqlalchemy.sql import join


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
    utc_offset = Column(Integer)
    
    def __init__(self, query, tweet_id, inserted_date, truncated, language, possibly_sensitive, coordinates, 
    retweeted_status, created_at_text, created_at, content, 
    from_user_screen_name, from_user_id, from_user_followers_count, from_user_friends_count,   
    from_user_listed_count, from_user_statuses_count, from_user_description,   
    from_user_location, from_user_created_at, retweet_count, entities_urls,entities_urls_count,         
    entities_hashtags, entities_hashtags_count,entities_mentions,entities_mentions_count, in_reply_to_screen_name, in_reply_to_status_id, source, entities_expanded_urls, json_output, 
    entities_media_count, media_expanded_url, media_url, media_type,video_link, photo_link,twitpic, utc_offset
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
        self.utc_offset = utc_offset
  

    def __repr__(self):
       return "<Organization, Sender('%s', '%s')>" % (self.from_user_screen_name,self.created_at)

class Fix:
	def __init__(self):
		engine = sqlalchemy.create_engine("sqlite:///en_lupus.sqlite", echo=False)
		Session = sessionmaker(bind=engine)
		self.session = Session()  
		Base.metadata.create_all(engine)
		# print engine.table_names()

	def main(self):

		q = self.session.query(Messages).filter(Messages.utc_offset == None)

		# print q
		count = 0
		count_in_second = 0
		count_all = 0
		updated_count = 0
		collisions = 0
		cannot_update = 0

		for row in q:
			# print row.tweet_id, " : ", str(row.utc_offset)

			count_all += 1

			if count_all % 100 == 0: 
				print "current count: " + str(count_all)

			offset_index = row.json_output.find("utc_offset", 0, len(row.json_output))
			value_start_index = row.json_output.find(" ", offset_index + 1, len(row.json_output)) + 1
			value_end_index = row.json_output.find(",", offset_index + 1, len(row.json_output)) 

			new_offset_one = row.json_output[value_start_index:value_end_index] 

			if(new_offset_one == 'None'):

				count += 1
				
				# if utc_offset exists second time  
				if row.json_output.find("utc_offset", value_end_index, len(row.json_output)) != -1:

					second_offset_index = row.json_output.find("utc_offset", 0, len(row.json_output))
					second_value_start_index = row.json_output.find(" ", offset_index + 1, len(row.json_output)) + 1
					second_value_end_index = row.json_output.find(",", offset_index + 1, len(row.json_output)) 
					count_in_second += 1

					# found it the second time: update the row in sqlite
					new_attempted_offset = row.json_output[second_value_start_index:second_value_end_index]
					if new_attempted_offset == 'None': 
						cannot_update += 1

					else: 
						row.utc_offset = int(new_attempted_offset)

						self.session.add(row)
		      			
						try:
							self.session.commit()
							updated_count += 1

						except:
							self.session.rollback()
							collisions += 1

				else: 
					cannot_update += 1


			else:
				row.utc_offset = int(row.json_output[value_start_index:value_end_index])
				self.session.add(row)

				try:
					self.session.commit()
					updated_count += 1

				except:
					self.session.rollback()
					collisions += 1

				# worked first time: update the row in the sqlite 



		print "missing utc_offset first: " + str(count)
		print "found in second: " + str(count_in_second)
		print "total: " + str(count_all)
		print "updated: " + str(updated_count)
		print "collisions: " + str(collisions)
		print "cannot_update: " + str(cannot_update)

if __name__ == '__main__':
	f = Fix()
	f.main()