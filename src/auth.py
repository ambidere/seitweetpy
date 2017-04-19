import os, webbrowser, signal
import tweepy
import exceptions

class TwitterAuthWrapper(object):
	"""wrapper for twitter authorization"""
	def __init__(self, options):
		super(TwitterAuthWrapper, self).__init__()
		self.options = options
		self.process_credentials_from_file()

	def process_credentials_from_file(self):
		credentials_file = self.options.credentials_file
		if credentials_file is not None:
			self.take_tokens_from_file(credentials_file)
			self.process_tokens(self.consumer_key, self.consumer_secret)
		else:
			self.process_tokens(self.options.consumer_key, self.options.consumer_secret)

	def take_tokens_from_file(self, credentials_file):
		if os.path.isfile(credentials_file) and os.stat(credentials_file).st_size > 0:
			with open(credentials_file, 'rt') as c_file:
				for line in c_file.read().splitlines():
					self.process_line_in_file(line)
		else:
			raise exceptions.CredentialsFileFormatError('Credentials file is empty and none existing. Please create a credentials file with your Twitter app\'s consumer token.')
		self.credentials_file = credentials_file

	def process_line_in_file(self, line):
		delimit_position = line.find('=')
		if line.count('=') == 1 and delimit_position > 0 and delimit_position < len(line):
			c_split = line.split("=")
			setattr(self, c_split[0], c_split[1])
		else:
			raise exceptions.CredentialsFileFormatError('Format of credentials file passed incorrect')

	def timeout_for_verify(self, signum, frame):
		raise exceptions.InvalidCredentialsError('Verification timed out. Try again.')

	def process_tokens(self, consumer_key, consumer_secret):
		if consumer_key is not None and consumer_secret is not None:
			self.consumer_key = consumer_key
			self.consumer_secret = consumer_secret
			self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
			self.process_access_token()
		else:
			raise exceptions.InvalidCredentialsError('No credentials entered')

		self.save_tokens()

	def process_access_token(self):
		access_key = getattr(self, 'access_key', None)
		access_secret = getattr(self, 'access_key', None)

		if access_key is None or access_secret is None:
			try:
				redirect_url = self.auth.get_authorization_url()
				webbrowser.open_new_tab(redirect_url)
				self.retrieve_verification_code()
				self.access_key = self.auth.access_token
				self.access_secret = self.auth.access_token_secret

			except tweepy.TweepError:
				print "Failed to get request token."
		return (access_key, access_secret)

	def retrieve_verification_code(self):
		signal.signal(signal.SIGALRM, self.timeout_for_verify)
		signal.alarm(15)
		verify_code = raw_input('Enter verification code here: ')
		signal.alarm(0)
		self.auth.get_access_token(verify_code)

	def save_tokens(self):
		with open(getattr(self, 'credentials_file', 'credentials.txt'), 'w') as creds:
			creds.write('%s=%s\n' % ('consumer_key' , self.consumer_key))
			creds.write('%s=%s\n' % ('consumer_secret' , self.consumer_secret))
			creds.write('%s=%s\n' % ('access_key' , self.access_key))
			creds.write('%s=%s\n' % ('access_secret' , self.access_secret))

	def get_twitter_auth(self):
		return self.auth