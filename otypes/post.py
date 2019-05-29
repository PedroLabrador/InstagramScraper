import json
from otypes.comment       import Comment
from otypes.like          import Like
from utilities.parameters import parameters
from utilities.request    import Request
from utilities.extras     import create_url_likes, create_url_comments

class Post:
	def __init__(self, post):
		self.id                                 = post['id']
		self.owner_id                           = post['owner']['id']
		self.owner_username                     = post['owner']['username']
		self.shortcode                          = post['shortcode']
		self.post_url                           = "https://instagram.com/p/%s/" % (post['shortcode'])
		self.display_url                        = post['display_url']
		self.display_resources                  = post['display_resources'] if 'display_resources' in post else None
		self.location                           = post['location']
		self.is_video                           = post['is_video']
		self.dimensions_width                   = post['dimensions']['width']
		self.dimensions_height                  = post['dimensions']['height']
		self.gating_info                        = post['gating_info']
		self.media_preview                      = post['media_preview']
		self.edge_liked_by                      = []
		self.edge_liked_by_count                = post['edge_liked_by']['count'] if 'edge_liked_by' in post else None
		self.has_next_page_likes                = ''
		self.end_cursor_likes                   = ''
		self.edge_media_preview_like            = post['edge_media_preview_like']['count'] if 'edge_media_preview_like' in post else None
		self.edge_media_to_caption              = post['edge_media_to_caption']
		self.edge_media_to_tagged_user          = post['edge_media_to_tagged_user'] if 'edge_media_to_tagged_user' in post else []
		self.edge_media_preview_comment         = post['edge_media_preview_comment'] if 'edge_media_preview_comment' in 'post' else None
		self.edge_media_to_sponsor_user         = post['edge_media_to_sponsor_user'] if 'edge_media_to_sponsor_user' in 'post' else None
		self.edge_comment_by                    = []
		self.edge_comment_by_count              = post['edge_media_to_comment']['count'] if 'edge_media_to_comment' in post else None
		self.edge_media_to_parent_comment_count = post['edge_media_to_parent_comment']['count'] if 'edge_media_to_parent_comment' in post else None
		self.has_next_page_comments             = ''
		self.end_cursor_comments                = ''
		self.thumbnail_src                      = post['thumbnail_src'] if 'thumbnail_src' in post else None
		self.thumbnail_resources                = post['thumbnail_resources'] if 'thumbnail_resources' in post else None
		self.comments_disabled                  = post['comments_disabled']
		self.taken_at_timestamp                 = post['taken_at_timestamp']
		self.accessibility_caption              = post['accessibility_caption'] if 'accessibility_caption' in post else ''
		self.should_log_client_event            = post['should_log_client_event'] if 'should_log_client_event' in post else None
		self.tracking_token                     = post['tracking_token'] if 'tracking_token' in post else None
		self.caption_is_edited                  = post['caption_is_edited'] if 'caption_is_edited' in post else None
		self.has_ranked_comments                = post['has_ranked_comments'] if 'has_ranked_comments' in post else None
		self.viewer_has_liked                   = post['viewer_has_liked'] if 'viewer_has_liked' in post else None
		self.viewer_has_saved                   = post['viewer_has_saved'] if 'viewer_has_saved' in post else None
		self.viewer_has_saved_to_collection     = post['viewer_has_saved_to_collection'] if 'viewer_has_saved_to_collection' in post else None
		self.viewer_in_photo_of_you             = post['viewer_in_photo_of_you'] if 'viewer_in_photo_of_you' in post else None
		self.viewer_can_reshare                 = post['viewer_can_reshare'] if 'viewer_can_reshare' in post else None
		self.is_ad                              = post['is_ad'] if 'is_ad' in post else None
		self.edge_web_media_to_related_media    = post['edge_web_media_to_related_media'] if 'edge_web_media_to_related_media' in post else None
		self.__typename                         = post['__typename']

	def __repr__(self):
		return self.shortcode

	def __str__(self):
		return self.shortcode

	def get_status_likes(self):
		return ({
			'liked_by_count':      self.edge_liked_by_count if self.edge_liked_by_count is not None else self.edge_media_preview_like,
			'scraped_likes':       len(self.edge_liked_by),
			'has_next_page_likes': self.has_next_page_likes
		})

	def get_status_comments(self):
		return ({
			'comment_by_count':       self.edge_comment_by_count if self.edge_comment_by_count is not None else self.edge_media_to_parent_comment_count,
			'scraped_comments':       len(self.edge_comment_by),
			'has_next_page_comments': self.has_next_page_comments
		})

	def get_post_likes_request(self, max_requests=5, aggresive=False):
		try:
			iteration = 0
			while True:
				print("[Request #%s] %s" % (iteration, self.get_status_likes()), end="\r", flush=True)
				response   = Request().url(create_url_likes(self.post_url, self.end_cursor_likes))
				data       = json.loads(response)['data']['shortcode_media']['edge_liked_by']
				iteration += 1

				self.has_next_page_likes = data['page_info']['has_next_page']
				self.end_cursor_likes    = data['page_info']['end_cursor']

				for edge in data['edges']:
					self.edge_liked_by.append(Like(edge['node']))

				if not self.has_next_page_likes or (iteration is max_requests and not aggresive):
					break
			print("status likes: %s" % self.get_status_likes())
		except Exception as e:
			raise e

	def get_post_comments_request(self, max_requests=5, aggresive=False):
		try:
			if not self.comments_disabled:
				iteration = 0
				while True:
					print("[Request #%s] %s" % (iteration, self.get_status_comments()), end="\r", flush=True)
					response   = Request().url(create_url_comments(self.post_url, self.end_cursor_comments))
					data       = json.loads(response)['data']['shortcode_media']['edge_media_to_parent_comment']
					iteration += 1

					self.has_next_page_comments = data['page_info']['has_next_page']
					self.end_cursor_comments    = data['page_info']['end_cursor']

					for edge in data['edges']:
						self.edge_comment_by.append(Comment(edge['node']))

					if not self.has_next_page_comments or (iteration is max_requests and not aggresive):
						break
				print("status comments: %s" % self.get_status_comments())
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
					print("User: %s not like the photo" % user)
				else:
					print("User: %s liked the photo" % user)
		else:
			print("please use an array of users")