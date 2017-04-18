import tweepy

class TwitterAuthWrapper(object):
	"""docstring for TwitterAuthWrapper"""
	def __init__(self, credentials_file):
		super(TwitterAuthWrapper, self).__init__()
		self.credentials_file = credentials_file
		self.get_credentials_from_file()

	def get_credentials_from_file(self):
		self.credentials = CredentialsContainer()
		with open(self.credentials_file, 'rt') as c_file:
			for line in c_file.read().splitlines():
				c_split = line.split("=")
				setattr(self.credentials, c_split[0], c_split[1])

	def get_twitter_auth(self):
		creds = self.credentials
		auth = tweepy.OAuthHandler(creds.consumer_key, creds.consumer_secret)
		auth.set_access_token(creds.access_key, creds.access_secret)
		return auth

class CredentialsContainer(object):
	"""docstring for CredentialsContainer"""
	def __init__(self):
		super(CredentialsContainer, self).__init__()