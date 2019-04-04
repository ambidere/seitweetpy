import tweepy
import builtins as exceptions

from src.auth import TwitterAuthWrapper
from src.post_actions import get_post_action_class
from src.fetch_actions import get_fetch_action_class

class SeiTweetFetcherApp(object):
	"""Application that fetches Tweets of a specific user"""
	def __init__(self, options):
		super(SeiTweetFetcherApp, self).__init__()
		self.auth_wrapper = TwitterAuthWrapper(options)
		self.api = tweepy.API(self.auth_wrapper.get_twitter_auth(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
		if not hasattr(options, 'action'):
			raise exceptions.InvalidArgumentsError('Action was not passed')
		self.action = options.action
		self.options = options

	def do_action(self):
		fetch_action_class = get_fetch_action_class(self.action)
		fetch_action = fetch_action_class(self.api, self.options)
		self.alltweets = fetch_action.do_fetch()
		return self

	def then(self, post_actions):
		for post_action_class in get_post_action_class(post_actions):
			post_action_class(self.alltweets, self.options).perform_action()