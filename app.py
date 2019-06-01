import json, requests
from  pprint            import pprint
from .otypes.user       import User
from .otypes.post       import Post
from .otypes.hashtag    import Hashtag
from .utilities.request import request
from .utilities.extras  import create_url_user, create_url_single_post, create_url_hashtag

class InstagramScraper:
	def __init__(self, profile_url=''):
		self.profile_url = profile_url
		self.user        = {}
		self.hashtags    = []

	def get_user_profile_request(self, profile_url='', reset_posts=True):
		try:
			response  = request.get(create_url_user(profile_url if profile_url else self.profile_url))
			data      = json.loads(response)
			# Set to True, just to delete the current saved posts and request them again with more data :(
			self.user = User(data['graphql']['user'], reset_posts)
		except Exception as e:
			raise e
		return self.user

	def get_single_post_request(self, post_url):
		post = {}
		try:
			response  = request.get(create_url_single_post(post_url))
			data      = json.loads(response)
			post      = Post(data['data']['shortcode_media'])
		except Exception as e:
			raise e
		return post

	def get_hashtag_request(self, hashtag_url, first=''):
		hashtag = {}
		try:
			response  = request.get(create_url_hashtag(hashtag_url, first))
			data      = json.loads(response)
			hashtag   = Hashtag(data['data']['hashtag'])
			self.hashtags.append(hashtag)
		except Exception as e:
			raise e
		return hashtag
