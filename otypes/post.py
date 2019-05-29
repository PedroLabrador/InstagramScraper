import json
from .comment import Comment
from .like    import Like
from utilities.parameters import parameters
from utilities.request    import Request
from utilities.extras     import create_url_likes, create_url_comments

class Post:
	def __init__(self, post):
		self.id                      = post['id']
		self.owner_id                = post['owner']['id']
		self.owner_username          = post['owner']['username']
		self.shortcode               = post['shortcode']
		self.post_url                = "https://instagram.com/p/%s/" % (post['shortcode'])
		self.display_url             = post['display_url']
		self.location                = post['location']
		self.is_video                = post['is_video']
		self.dimensions_width        = post['dimensions']['width']
		self.dimensions_height       = post['dimensions']['height']
		self.gating_info             = post['gating_info']
		self.media_preview           = post['media_preview']
		self.edge_liked_by_count     = post['edge_liked_by']['count'] if 'edge_liked_by' in post else None
		self.edge_media_preview_like = post['edge_media_preview_like']['count'] if 'edge_media_preview_like' in post else None
		self.edge_media_to_caption   = post['edge_media_to_caption']
		self.edge_comment_by_count   = post['edge_media_to_comment']['count'] if 'edge_media_to_comment' in post else None
		self.thumbnail_src           = post['thumbnail_src'] if 'thumbnail_src' in post else None
		self.thumbnail_resources     = post['thumbnail_resources'] if 'thumbnail_resources' in post else None
		self.comments_disabled       = post['comments_disabled']
		self.taken_at_timestamp      = post['taken_at_timestamp']
		self.accessibility_caption   = post['accessibility_caption'] if 'accessibility_caption' in post else ''
		self.__typename              = post['__typename']

		self.has_next_page_likes     = ''
		self.end_cursor_likes        = ''
		self.edge_liked_by           = []

		self.has_next_page_comments  = ''
		self.end_cursor_comments     = ''
		self.edge_commented_by       = []

	def __repr__(self):
		return self.shortcode

	def __str__(self):
		return self.shortcode

	def get_post_likes_request(self, max_requests=5):
		try:
			iteration = 0
			while True:
				response   = Request().url(create_url_likes(self.post_url, self.end_cursor_likes))
				data       = json.loads(response)['data']['shortcode_media']['edge_liked_by']
				iteration += 1

				self.has_next_page_likes = data['page_info']['has_next_page']
				self.end_cursor_likes    = data['page_info']['end_cursor']

				for edge in data['edges']:
					self.edge_liked_by.append(Like(edge['node']))

				if not self.has_next_page_likes or iteration is max_requests:
					break
		except Exception as e:
			raise e

	def check_users_liked(self, users):
		if isinstance(users, list):
			if len(self.edge_liked_by) is 0:
				self.get_post_likes_request()
			for user in users:
				liked = False
				for like in self.edge_liked_by:
					if user == like.username:
						liked = True
						break
				if not liked:
					print("User: %s did not like the photo" % user)
				else:
					print("User: %s did like the photo" % user)
		else:
			print("please use an array of users")

	def get_post_comments_request(self, max_requests=5):
		try:
			iteration = 0
			while True:
				response   = Request().url(create_url_comments(self.post_url, self.end_cursor_comments))
				data       = json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']
				iteration += 1

				self.has_next_page_comments = data['page_info']['has_next_page']
				self.end_cursor_comments    = data['page_info']['end_cursor']

				for edge in data['edges']:
					self.edge_commented_byppend(Comment(edge['node']))

				if not self.has_next_page_comments or iteration is max_requests:
					break
		except Exception as e:
			raise e
