
# get the tweets 
echo "Downloading tweets"
python2 twython_sqlite.py
echo "Done getting tweets"

# show updated count 
echo "Updated total count:"
sqlite3 en_lupus.sqlite "select count(*) from hashtags"

# show updated count original tweets only 
echo "Updated total count (original tweets only):"
sqlite3 en_lupus.sqlite "select count(*) from hashtags where hashtags.retweeted_status like ''"

echo "updating analysis CSVs"

echo "updating count for each day of week"
sqlite3 en_lupus.sqlite < ../../sql-analysis/tweet_count_day_per_week.sql 

echo "updating count for each hour of day"
sqlite3 en_lupus.sqlite < ../../sql-analysis/tweet_count_hour_of_day.sql

echo "done"