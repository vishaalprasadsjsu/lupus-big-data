Lupus Big Data Project 
======================

The purpose of this project is to analyze data from Twitter using Big Data tools to see what [Lupus](http://www.mayoclinic.org/diseases-conditions/lupus/basics/definition/con-20019676) patients, and others affected by Lupus, are saying.  This information can be used to help direct Lupus research. 

Gathering Data 
--------------

Twitter has a an [array of APIs](https://developer.twitter.com/en/docs/api-reference-index) available to us developers, but we mostly use the [search APIs](https://developer.twitter.com/en/docs/tweets/search/overview).

To run our code and use these APIs to gather data, you'll need to get your own API access tokens from the [Twitter developer's page](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens).  (We keep our private access tokens off this public repo).


Analyzing Data 
--------------

The two languages we use mostly are [R](https://www.r-project.org/) and [Python 3.x](https://www.python.org/) as they're friendly with data analysis, and easy languages to get started in for a project like this. 

To make gathering data easier, we use packages such as [rtweet](https://cran.r-project.org/web/packages/rtweet/vignettes/intro.html) and [Twython](https://twython.readthedocs.io/en/latest/).

Findings & Notebooks
--------------------
Here are notebooks with our findings: 
* [Classification using ML](./ml/tweet_classification.ipynb) 
* [Misc Tweet Analysis](./twitter_python/lupus-graphs.ipynb)
* [NLP Analysis](./twitter_python/clean_word_count_nb.ipynb)
