
.mode csv
.output user_name_orig_tweet_freq.csv
SELECT hashtags.from_user_screen_name, count(*) AS freq FROM hashtags WHERE hashtags.retweeted_status  LIKE '' GROUP BY hashtags.from_user_screen_name ORDER BY count(*) ASC;