
# get the tweets 
echo "Downloading tweets"
python2 ./twython_sqlite.py
echo "Done getting tweets"

# show updated count 
echo "Updated total count:"
sqlite3 ./en_lupus.sqlite "select count(*) from hashtags"

# show updated count original tweets only 
echo "Updated total count (original tweets only):"
sqlite3 ./en_lupus.sqlite "select count(*) from hashtags where hashtags.retweeted_status = 0"

echo "updating analysis CSVs"

echo "updating count for each day of week"
sqlite3 en_lupus.sqlite < ../sql-analysis/tweet_count_day_per_week.sql 

echo "updating count for each hour of day"
sqlite3 en_lupus.sqlite < ../sql-analysis/tweet_count_hour_of_day.sql

echo "saving original tweet content to tweet_content"
sqlite3 en_lupus.sqlite "select content from hashtags where retweeted_status = 0 " > tweet_content.txt

echo "done"

