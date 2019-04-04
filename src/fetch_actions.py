import sys, inspect
import builtins as exceptions

def get_fetch_action_class(action):
    for name, class_name in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(class_name) and issubclass(class_name, TweetFetchActions) and class_name.name == action:
            return class_name
    return TweetFetchActions

class TweetFetchActions(object):
    name = "default"
    def __init__(self, api, options):
        super(TweetFetchActions, self).__init__()
        self.assert_options(options)
        self.api = api
        self.options = options

    def assert_options(self, options):
        pass

    def do_fetch(self):
        return []

class AllTweetsFetchActions(TweetFetchActions):
    name = "all_tweets"
    def __init__(self, api, options):
        super(AllTweetsFetchActions, self).__init__(api, options)
        self.user = options.user

    def assert_options(self, options):
        if not hasattr(options, 'user'):
	        raise exceptions.InvalidArgumentsError('User was not passed')

    def do_fetch(self):
        user = self.user

        alltweets = []
        new_tweets = self.api.user_timeline(screen_name=user, count=200)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        
        print(f'{len(alltweets)} tweets fetched so far...')
        while (len(new_tweets) > 0):
	        new_tweets = self.api.user_timeline(screen_name=user, count=200, max_id=oldest)
	        alltweets.extend(new_tweets)
	        oldest = alltweets[-1].id - 1
	        print(f'{len(alltweets)} tweets fetched so far...')
        
        return alltweets