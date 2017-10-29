SELECT hashtags.from_user_screen_name, count(*) AS freq FROM hashtags GROUP BY hashtags.from_user_screen_name ORDER BY count(*) ASC;
