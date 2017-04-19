import tweepy

from auth import TwitterAuthWrapper

class SeiTweetApp(object):
	"""Application that fetches Tweets of a specific user"""
	def __init__(self, options):
		super(SeiTweetApp, self).__init__()
		self.auth_wrapper = TwitterAuthWrapper(options)
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
		return alltweets
