import tweepy

class TwitterAuthWrapper(object):
	"""wrapper for twitter authorization"""
	def __init__(self, credentials_file):
		super(TwitterAuthWrapper, self).__init__()
		self.credentials_file = credentials_file
		self.get_credentials_from_file()

	def get_credentials_from_file(self):
		with open(self.credentials_file, 'rt') as c_file:
			for line in c_file.read().splitlines():
				c_split = line.split("=")
				setattr(self, c_split[0], c_split[1])

	def get_twitter_auth(self):
		auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
		auth.set_access_token(self.access_key, self.access_secret)
		return auth