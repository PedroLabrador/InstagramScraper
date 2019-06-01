import json
from  .post              import Post
from ..utilities.extras  import create_url_hashtag
from ..utilities.request import request

class Hashtag:
	def __init__(self, hashtag):
		self.id                                     = hashtag['id']
		self.name                                   = hashtag['name']
		self.hashtag_url                            = 'https://instagram.com/explore/tags/%s/' % (hashtag['name'])
		self.allow_following                        = hashtag['allow_following']
		self.is_following                           = hashtag['is_following']
		self.is_top_media_only                      = hashtag['is_top_media_only']
		self.profile_pic_url                        = hashtag['profile_pic_url']
		self.has_next_page                          = hashtag['edge_hashtag_to_media']['page_info']['has_next_page']
		self.end_cursor                             = hashtag['edge_hashtag_to_media']['page_info']['end_cursor']
		self.edge_hashtag_to_media_count            = hashtag['edge_hashtag_to_media']['count']
		self.edge_hashtag_to_media	                = [
			Post(post['node']) for post in hashtag['edge_hashtag_to_media']['edges']
		]
		self.edge_hashtag_to_top_posts	            = hashtag['edge_hashtag_to_top_posts']
		self.edge_hashtag_to_content_advisory_count = hashtag['edge_hashtag_to_content_advisory']['count']
		self.edge_hashtag_to_content_advisory       = [
			Post(post['node']) for post in hashtag['edge_hashtag_to_content_advisory']['edges']
		]

	def __repr__(self):
		return self.name

	def __str__(self):
		return self.name

	def status(self):
		return ({
			'post_count':    self.edge_hashtag_to_media_count,
			'scraped_posts': len(self.edge_hashtag_to_media),
			'has_next_page': self.has_next_page
		})

	def get_posts_request(self, max_requests=2, first='', aggresive=False):
		try:
			iteration = 0
			while True:
				print("[Request #%s] %s" % (iteration, self.status()), end="\r", flush=True)
				if not self.has_next_page or (iteration is max_requests and not aggresive):
					break
				else:
					iteration += 1
					response  = request.get(create_url_hashtag(self.hashtag_url, first, self.end_cursor))
					data      = json.loads(response)['data']['hashtag']['edge_hashtag_to_media']

					self.has_next_page = data['page_info']['has_next_page']
					self.end_cursor    = data['page_info']['end_cursor']

					for current in data['edges']:
						self.edge_hashtag_to_media.append(Post(current['node']))
		except Exception as e:
			raise e
	
	def refresh_post_tags(self):
		print("Refreshing %s posts from %s" % (len(self.edge_hashtag_to_media), self.hashtag_url))
		for post in self.edge_hashtag_to_media:
			print("Updating Post %s" % (post.shortcode), end="\r", flush=True)
			post.update_tags_request()
		print("Updating task done successfully")

	def retrieve_tagged_users(self):
		tags = []
		usernames = []
		for post in self.edge_hashtag_to_media:
			for tag in post.edge_media_to_tagged_user:
				if not tag.username in usernames:
					usernames.append(tag.username)
					tags.append(tag)
		return tags

	def toJSON(self):
		return {
			'id': self.id,
			'hashtag_url': self.hashtag_url,
			'profile_pic_url': self.profile_pic_url,
			'edge_hashtag_to_media': [post.toJSON() for post in self.edge_hashtag_to_media]
		}
