# Lupus Big Data Project 
The purpose of this project is to analyze data from Twitter using Big Data tools to see what [Lupus](http://www.mayoclinic.org/diseases-conditions/lupus/basics/definition/con-20019676) patients, and others affected by Lupus, are saying.  If successful, this information can be used to help direct Lupus research. 

## Gathering Data 
Twitter has a an [array of APIs](https://developer.twitter.com/en/docs/api-reference-index) available to us developers, but we mostly use the [search APIs](https://developer.twitter.com/en/docs/tweets/search/overview).

To run our code and use these APIs to gather data, you'll need to get your own API access tokens from the [Twitter developer's page](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens).  (We keep our access tokens off this public repo since they're supposed to be private keys).

To make gathering data easier, we use packages such as [rtweet](https://cran.r-project.org/web/packages/rtweet/vignettes/intro.html) and [Twython](https://twython.readthedocs.io/en/latest/).

## Analyzing Data 
The two languages we use mostly are [R](https://www.r-project.org/) and [Python 3.x](https://www.python.org/) as they're friendly with data analysis, and easy languages to get started in for a project like this. 

## Repo Organization 
This repo is organized in a few levels.  The first level contains folders for a given **purpose** (for example, the folder named `twitter_python` is contains work relevant to gathering Twitter Data using Python).  The next level separates each person's work if people have a different approach to making progress in the given **purpose**. 
