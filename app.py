import json
from otypes.user       import User
from otypes.post       import Post
from otypes.hashtag    import Hashtag
from utilities.request import Request
from utilities.extras  import create_url_user, create_url_single_post, create_url_hashtag
from pprint            import pprint

class InstagramScraper:
	def __init__(self, profile_url=''):
		self.profile_url = profile_url
		self.user        = {}
		self.hashtags    = []

	def get_user_profile_request(self, profile_url='', reset_posts=True):
		try:
			response  = Request().url(create_url_user(profile_url if profile_url else self.profile_url))
			data      = json.loads(response)
			# Set to True, just to delete the current saved posts and request them again with more data :(
			self.user = User(data['graphql']['user'], reset_posts)
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

	def get_hashtag_request(self, hashtag_url, first=''):
		hashtag = {}
		try:
			response  = Request().url(create_url_hashtag(hashtag_url, first))
			data      = json.loads(response)
			hashtag   = Hashtag(data['data']['hashtag'])
			self.hashtags.append(hashtag)
		except Exception as e:
			raise e
		return hashtag

# tests & examples

i = InstagramScraper()
user = i.get_user_profile_request("https://www.instagram.com/paolapernia_/")
user.get_posts_request(max_requests=2)
tags = user.retrieve_tagged_users()

users_with_external_url = []

for tag in tags:
	tag.check_profile()
	if tag.user.external_url:
		users_with_external_url.append({
			'username': tag.user.username,
			'full_name': tag.user.full_name,
			'external_url': tag.user.external_url
		})

print("Profiles checked successfully             ")
pprint(users_with_external_url)

# for post in user.posts:
# 	pprint(post.toJSON())

# hashtag = i.get_hashtag_request("https://www.instagram.com/explore/tags/stackoverflow/")
# # hashtag.get_posts_request(max_requests=1, first=12)
# hashtag.refresh_post_tags()
# tags = hashtag.retrieve_tagged_users()

# users_with_external_url = []

# for tag in tags:
# 	tag.check_profile()
# 	if tag.user.external_url:
# 		users_with_external_url.append({
# 			'username': tag.user.username,
# 			'full_name': tag.user.full_name,
# 			'external_url': tag.user.external_url
# 		})

# print("Profiles checked successfully             ")
# pprint(users_with_external_url)

# pprint(hashtag.toJSON())

# user.get_likes_and_comments_request(aggresive=True)
# user.save_posts_to_json()

# post = user.find_post("Bx2p0gsA-dT")
# post.get_likes_request(aggresive=True)
# post.get_comments_request(aggresive=True)

# i = InstagramScraper()
# user = i.get_user_profile_request("https://instagram.com/par_anoia/")

# print(user.get_info())
# user.get_posts_request(aggresive=True)
# print(user.posts)

# post = i.get_single_post_request("http://www.instagram.com/p/BwC3-fwH2dZ/")
# post.get_likes_request(aggresive=True)
# print("--------------------")
# print(post.edge_liked_by)
# print("--------------------")
# post.get_comments_request(aggresive=True)
# print("--------------------")
# print(post.edge_comment_by)
# print("--------------------")
# post.check_users_liked(['crovaz', 'andresraul7', 'roxanadpc', 'pedroool'])


