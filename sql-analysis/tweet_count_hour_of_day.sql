/* Count of tweets for each hour of the day */ 

.mode csv
.output hour_of_day_count.csv
SELECT strftime('%H', created_at),  COUNT(*) FROM hashtags GROUP BY strftime('%H', created_at);