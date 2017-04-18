#!/usr/bin/env python
# encoding: utf-8

import tweepy
import csv

from optparse import OptionParser

from src.seitweet import SeiyuuTweetApp

opt_parse = OptionParser()
opt_parse.add_option("-c", "--credentials", dest="credentials_file",
                  help="File containing credentials for Twitter API", metavar="FILE")
opt_parse.add_option("-a", "--action", dest="action",
                  help="Action", metavar="ACTION")
opt_parse.add_option("-u", "--user", dest="user",
                  help="User", metavar="TWITTER_USER")
opt_parse.add_option("-o", "--output", dest="output_file",
                  help="User", metavar="FILE")
(options, args) = opt_parse.parse_args()

if __name__ == '__main__':
	app = SeiyuuTweetApp(options.credentials_file)
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in app.get_all_tweets(options.user)]
	
	with open(options.output_file, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)