
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
