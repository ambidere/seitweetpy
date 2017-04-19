import tweepy

from auth import TwitterAuthWrapper

class SeiyuuTweetApp(object):
	"""Application that fetches Tweets of a specific user"""
	def __init__(self, credentials_file):
		super(SeiyuuTweetApp, self).__init__()
		self.auth_wrapper = TwitterAuthWrapper(credentials_file)
		self.api = tweepy.API(self.auth_wrapper.get_twitter_auth())

	def get_all_tweets(self, user, *args, **kwargs):
		alltweets = []
		new_tweets = self.api.user_timeline(screen_name=user, count=200)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

		while len(new_tweets) > 0:
			new_tweets = self.api.user_timeline(screen_name=user, count=200, max_id=oldest)
			alltweets.extend(new_tweets)
			oldest = alltweets[-1].id - 1
			
			print "...%s tweets downloaded so far" % (len(alltweets))
		return alltweets
