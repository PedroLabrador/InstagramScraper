import json
from pprint import pprint
from otypes.user import User
from otypes.post import Post
from utilities.request    import Request
from utilities.extras     import create_url_user, create_url_single_post

class InstagramScraper:
	def __init__(self, profile_url):
		self.profile_url = profile_url
		self.user        = {}

	def get_user_profile_request(self):
		try:
			response  = Request().url(create_url_user(self.profile_url))
			data      = json.loads(response)
			self.user = User(data['graphql']['user'])
		except Exception as e:
			raise e
		return self.user

	def get_single_post_request(self, post_url):
		post = {}
		try:
			response  = Request().url(create_url_single_post(post_url))
			data      = json.loads(response)
			post      = Post(data['data']['shortcode_media'])
		except Exception as e:
			raise e

		return post


i = InstagramScraper("https://www.instagram.com/selenagomez/")

user = i.get_user_profile_request()
user.get_posts_request(max_requests=10)
print(user.posts)

# post = i.get_single_post_request("http://www.instagram.com/p/BwC3-fwH2dZ/")
# post.get_post_likes_request(max_requests=1)
# post.get_post_comments_request(max_requests=1)
# print(post.edge_liked_by)
# print(post.edge_commented_by)

# post.check_users_liked("http://www.instagram.com/p/BwC3-fwH2dZ/", ['crovaz', 'andresraul7', 'roxanadpc', 'pedroool'])


