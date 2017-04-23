import sys, inspect, csv
import exceptions
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def get_post_action_class(post_actions):
	if len(post_actions) <= 0:
		raise exceptions.InvalidArgumentsError('No post actions are passed')
	new_actions = post_actions.split(',')
	for name, class_name in inspect.getmembers(sys.modules[__name__]):
		for post_action in new_actions:
			if inspect.isclass(class_name) and issubclass(class_name, TweetActions) and class_name.name == post_action:
				yield class_name
			elif inspect.isclass(class_name):
				yield TweetActions

class TweetActions(object):
	"""actions for receiving one tweet"""
	name = "default"
	def __init__(self, tweets, options, **kwargs):
		super(TweetActions, self).__init__()
		self.tweets = tweets
		for key, value in kwargs.iteritems():
			setattr(self, key, value)
		self.assert_arguments_valid(options)

	def assert_arguments_valid(self, options):
		pass

	def perform_action(self):
		pass

class JSONAction(TweetActions):
	"""prints tweets fetched to json"""
	name = "json"
	def __init__(self, tweets, options, **kwargs):
		super(JSONAction, self).__init__(tweets, options, **kwargs)
		self.output = options.output

	def assert_arguments_valid(self, options):
		if not hasattr(options, 'output'):
			raise exceptions.InvalidArgumentsError('Output arguments not passed.')
		if not options.output.lower().endswith('.json'):
			raise exceptions.InvalidArgumentsError('Output arguments must end with .json.')

	def perform_action(self):
		with open(self.output, 'wb') as json_file:
			for tweet in self.tweets:
				json.dump(tweet._json, json_file, sort_keys = True, indent = 4)

class PrintCSVAction(TweetActions):
	"""prints tweets fetched to csv"""
	name = "csv"
	def __init__(self, tweets, options, **kwargs):
		super(PrintCSVAction, self).__init__(tweets, options, **kwargs)
		self.fields = ["id","created_at","text"]
		self.output = options.output
		
	def perform_action(self):
		with open(self.output, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(self.fields)
			writer.writerows(self._build_csv_rows())

	def assert_arguments_valid(self, options):
		if not hasattr(options, 'output'):
			raise exceptions.InvalidArgumentsError('Output arguments not passed.')
		if not options.output.lower().endswith('.csv'):
			raise exceptions.InvalidArgumentsError('Output arguments must end with .csv.')

	def _build_csv_rows(self):
		rows = []
		for tweet in self.tweets:
			row = []
			for field in self.fields:
				try:
					value = getattr(tweet, field, '')
					if field == 'text':
						value = value.encode('utf-8')
					row.append(value)
				except ValueError, e:
					print "field not found"
			rows.append(row)
		return rows

class TopMentionsAction(TweetActions):
	"""retrieves top mentions"""
	name = "top_mentions"
	def __init__(self, tweets, options, **kwargs):
		super(TopMentionsAction, self).__init__(tweets, options, **kwargs)
		self.fontProp = fm.FontProperties(fname='./resources/default.ttf')

	def assert_arguments_valid(self, options):
		pass

	def perform_action(self):
		tweets_data = pd.DataFrame(self.tweets)
		tweets_data['text'] = map(lambda tweet: tweet.text.encode('utf-8'), self.tweets)
		user_mentions = map(lambda tweet: tweet.entities['user_mentions'], self.tweets)
		tweets_data['mentions'] = map(lambda mention: mention.screen_name, user_mentions)

		print 'Analyzing tweets by mentions\n'
		tweets_by_mentions = tweets_data['mentions'].value_counts()
		fig, ax = plt.subplots()
		ax.tick_params(axis='x', labelsize=10)
		ax.tick_params(axis='y', labelsize=10)
		ax.set_xlabel('Mentions', fontsize=10)
		ax.set_ylabel('Number of tweets' , fontsize=10)
		ax.set_title('Top 10 mentions', fontsize=10, fontweight='bold')
		tweets_by_mentions[:10].plot(ax=ax, kind='bar', color='red')
		plt.savefig('tweets_by_mentions', format='png')