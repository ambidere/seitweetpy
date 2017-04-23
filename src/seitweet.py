import tweepy
import exceptions

from auth import TwitterAuthWrapper
from post_actions import get_post_action_class

class SeiTweetFetcherApp(object):
	"""Application that fetches Tweets of a specific user"""
	def __init__(self, options):
		super(SeiTweetFetcherApp, self).__init__()
		self.auth_wrapper = TwitterAuthWrapper(options)
		self.api = tweepy.API(self.auth_wrapper.get_twitter_auth(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		self.alltweets = []
		if not hasattr(options, 'user'):
			raise exceptions.InvalidArgumentsError('User was not passed')
		self.user = options.user
		self.options = options

	def _get_all_tweets(self, user):
		alltweets = []
		new_tweets = self.api.user_timeline(screen_name=user, count=200)
		alltweets.extend(new_tweets)
		oldest = alltweets[-1].id - 1

		print '%s tweets fetched so far...' % (len(alltweets))
		while len(new_tweets) > 0:
			new_tweets = self.api.user_timeline(screen_name=user, count=200, max_id=oldest)
			alltweets.extend(new_tweets)
			oldest = alltweets[-1].id - 1
			print '%s tweets fetched so far...' % (len(alltweets))
		self.alltweets = alltweets
		return self

	def do_action(self):
		self._get_all_tweets(self.user)
		return self

	def then(self, post_actions):
		for post_action_class in get_post_action_class(post_actions):
			post_action_class(self.alltweets, self.options).perform_action()