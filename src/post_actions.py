import os, sys, inspect, csv, time
import exceptions
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.transforms as mtransforms

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
		self.user = options.user
		self.top_entries_shown = 8
		self.output = '%s_tweets_by_mentions.png' % (self.user)
		self.fontProp = fm.FontProperties(fname=os.path.abspath('./resources/default.otf'))

	def assert_arguments_valid(self, options):
		pass

	def get_mentioned_screen_names(self):
		all_screen_names = []
		for tweet in self.tweets:
			screen_names = []
			for user_mentions in tweet.entities['user_mentions']:
				if self.filter_mentions(user_mentions['screen_name']):
					screen_names.append(user_mentions['screen_name'])
			all_screen_names.extend(screen_names)
		return all_screen_names

	def filter_mentions(self, screen_name):
		return not screen_name == self.user

	def get_title(self):
		return 'Top %s mentions by user: %s\n as of %s' % (self.top_entries_shown, self.user, time.strftime("%m/%d/%Y %H:%M"))

	def perform_action(self):
		tweets_data = pd.DataFrame()
		tweets_data['mentions'] = self.get_mentioned_screen_names()
		
		tweets_by_mentions = tweets_data['mentions'].value_counts()
		print tweets_by_mentions
		fig, ax = plt.subplots()
		ax.tick_params(axis='x', labelsize=10)
		ax.tick_params(axis='y', labelsize=10)
		ax.set_xlabel('Created by seitweetpy. Written by @ambidere', fontsize=10, fontproperties=self.fontProp)
		ax.set_ylabel('Number of tweets' , fontsize=10, fontproperties=self.fontProp)
		ax.set_title(self.get_title(), fontsize=10, fontweight='bold', fontproperties=self.fontProp)
		tweets_by_mentions[:self.top_entries_shown].plot(ax=ax, kind='bar', color='#3498db')

		for i, label in enumerate(list(tweets_by_mentions.index)):
			total = tweets_by_mentions.ix[i]
			ax.annotate(str(total), (i - 0.2, total + 0.2))

		plt.tight_layout()
		plt.savefig(self.output, format='png')

class TopMentionsToAqoursAction(TopMentionsAction):
	"""retrieves top mentions to aqours twitters"""
	name = "top_mentions_to_aqours"
	AQOURS_TWITTERS = ['anju_inami', 'Rikako_Aida', 'suwananaka', 'box_komiyaarisa', 'Saito_Shuka', 'Aikyan_', 'Kanako_tktk', 'aina_suzuki723', 'furihata_ai']
	def __init__(self, tweets, options, **kwargs):
		super(TopMentionsToAqoursAction, self).__init__(tweets, options, **kwargs)
		self.output = '%s_tweets_by_mentions_to_aqours.png' % (self.user)

	def filter_mentions(self, screen_name):
		return not screen_name == self.user and screen_name in self.AQOURS_TWITTERS

	def get_title(self):
		return 'Top Aqours mentions by user: %s\n as of %s' % (self.user, time.strftime("%m/%d/%Y %H:%M"))