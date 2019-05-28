from pprint import pprint

class Post:
	def __init__(self, post):
		self.id = post['id']
		self.owner = post['owner']
		self.is_video = post['is_video']
		self.location = post['location']
		self.shortcode = post['shortcode']
		self.__typename = post['__typename']
		self.dimensions = post['dimensions']
		self.gating_info = post['gating_info']
		self.display_url = post['display_url']
		self.edge_liked_by = post['edge_liked_by']
		self.thumbnail_src = post['thumbnail_src']
		self.media_preview = post['media_preview']
		self.comments_disabled = post['comments_disabled']
		self.taken_at_timestamp = post['taken_at_timestamp']
		self.thumbnail_resources = post['thumbnail_resources']
		self.accessibility_caption = post['accessibility_caption'] if 'accessibility_caption' in post else ''
		self.edge_media_to_caption = post['edge_media_to_caption']
		self.edge_media_to_comment = post['edge_media_to_comment']
		self.edge_media_preview_like = post['edge_media_preview_like']
