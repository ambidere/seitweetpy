class TweetActions(object):
	name = "default"
	"""actions for receiving one tweet"""
	def __init__(self, tweets, **kwargs):
		super(TweetActions, self).__init__()
		self.tweets = tweets
		for key, value in kwargs.iteritems():
			setattr(self, key, value)

	def performAction(self):
		pass

class PrintCSVAction(TweetActions):
	name = "csv"
	"""prints tweets fetched to csv"""
	def __init__(self, tweets, output_file, **kwargs):
		super(PrintCSV, self).__init__(tweets)
		self.output_file = output_file
		
	def performAction(self):
		with open(self.output_file, 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(["id","created_at","text"])
			writer.writerows(self._build_csv_rows())

	def _build_csv_rows(self):
		rows = []
		for tweet in self.tweets:
			row = []
			for field in self.fields:
				try:
					value = getattr(tweet, field, '')
					row.append(value)
				except ValueError, e:
					print "field not found"
			rows.append(row)
		return rows

		