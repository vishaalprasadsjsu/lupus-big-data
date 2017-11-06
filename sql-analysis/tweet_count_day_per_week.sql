/* Count of tweets for each day of the week */
/*  */ 
.mode csv
.output day_of_week_count.csv
SELECT strftime('%w', created_at),  COUNT(*) FROM hashtags GROUP BY strftime('%w', created_at);