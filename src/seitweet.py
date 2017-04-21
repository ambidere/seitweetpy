import tweepy

from auth import TwitterAuthWrapper
from actions import get_action_class

class SeiTweetApp(object):
	"""Application that fetches Tweets of a specific user"""
	def __init__(self, options):
		super(SeiTweetApp, self).__init__()
		self.auth_wrapper = TwitterAuthWrapper(options)
		self.api = tweepy.API(self.auth_wrapper.get_twitter_auth())
		self.alltweets = []
		self.options = options

	def get_all_tweets(self, user, *args, **kwargs):
		alltweets = []
		new_tweets = self.api.user_timeline(screen_name=user, count=200)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

		while len(new_tweets) > 0:
			new_tweets = self.api.user_timeline(screen_name=user, count=200, max_id=oldest)
			alltweets.extend(new_tweets)
			oldest = alltweets[-1].id - 1
		self.alltweets = alltweets
		return self

	def do_action(self):
		action = self.options.action
		action_class = get_action_class(action)
		action_class(self.alltweets, options=self.options).perform_action()