import json
from .otypes.user       import User
from .otypes.post       import Post
from .otypes.hashtag    import Hashtag
from .utilities.request import request
from .utilities.extras  import create_url_user, create_url_single_post, create_url_hashtag
from .exceptions.common import IgRequestException

class InstagramScraper:
	def __init__(self, profile_url=''):
		self.profile_url = profile_url
		self.user        = {}
		self.hashtag     = {}

	def get_user_profile_request(self, profile_url='', reset_posts=True):
		try:
			response  = request.get(create_url_user(profile_url if profile_url else self.profile_url))
			data      = json.loads(response.text)
			# Set to True, just to delete the current saved posts and request them again with more data :(
			self.user = User(data['graphql']['user'], reset_posts)
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True)
				self.get_user_profile_request(profile_url, reset_posts)
			else:
				raise r
		except Exception as e:
			raise e
		return self.user

	def get_single_post_request(self, post_url):
		try:
			post = {}
			response  = request.get(create_url_single_post(post_url))
			data      = json.loads(response.text)
			post      = Post(data['data']['shortcode_media'])
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True)
				self.get_single_post_request(post_url)
			else:
				raise r
		except Exception as e:
			raise e
		return post

	def get_hashtag_request(self, hashtag_url, first=''):
		try:
			response     = request.get(create_url_hashtag(hashtag_url, first))
			data         = json.loads(response.text)
			self.hashtag = Hashtag(data['data']['hashtag'])
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True)
				self.get_hashtag_request(hashtag_url, first)
			else:
				raise r
		except Exception as e:
			raise e
		return self.hashtag

	def renew_proxy_list(self, option):
		print("[%s] Refreshing free proxy list" % (time.strftime('%x %X')))
		return request.get_proxy_list(option)
