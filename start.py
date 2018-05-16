#!/usr/bin/env python
# encoding: utf-8

import tweepy
import csv

from optparse import OptionParser

from src.seitweet import SeiTweetFetcherApp

opt_parse = OptionParser()
opt_parse.add_option("-c", "--credentials", dest="credentials_file",
                  help="File containing credentials for Twitter API", metavar="FILE", default="credentials.txt")
opt_parse.add_option("-a", "--action", dest="action",
                  help="Fetching action the system will perform", metavar="ACTION", default="all_tweets")
opt_parse.add_option("-p", "--post_action", dest="post_actions",
                  help="Action performed after tweets have been fetched", metavar="ACTION", default="csv")
opt_parse.add_option("-u", "--user", dest="user",
                  help="User", metavar="TWITTER_USER")
opt_parse.add_option("-o", "--output", dest="output",
                  help="User", metavar="FILE")
opt_parse.add_option("-k", "--consumer_key", dest="consumer_key",
                  help="Twitter App Consumer Key", metavar="CONSUMER_KEY")
opt_parse.add_option("-s", "--consumer_secret", dest="consumer_secret",
                  help="Twitter App Consumer Secret", metavar="CONSUMER_SECRET")

(options, args) = opt_parse.parse_args()

if __name__ == '__main__':
    app = SeiTweetFetcherApp(options)
    app.do_action().then(options.post_actions)
