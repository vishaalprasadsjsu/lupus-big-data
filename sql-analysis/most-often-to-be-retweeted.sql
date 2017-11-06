/* select users with most retweets, sort by retweet count */

SELECT from_user_screen_name, SUM(retweet_count) FROM hashtags GROUP BY from_user_id ORDER BY SUM(retweet_count) DESC LIMIT 15; 