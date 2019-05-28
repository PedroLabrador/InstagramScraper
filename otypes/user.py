from .post import Post

class User:
	def __init__(self, user):
		self.id                        = user['id']
		self.username                  = user['username']
		self.biography                 = user['biography']
		self.full_name                 = user['full_name']
		self.profile_url               = 'https://instagram.com/%s' % (user['username'])
		self.has_channel               = user['has_channel']
		self.external_url              = user['external_url']
		self.external_url_linkshimmed  = user['external_url_linkshimmed']
		self.country_block             = user['country_block']
		self.profile_pic_url           = user['profile_pic_url']
		self.profile_pic_url_hd        = user['profile_pic_url_hd']
		self.is_private                = user['is_private']
		self.is_verified               = user['is_verified']
		self.is_joined_recently        = user['is_joined_recently']
		self.is_business_account       = user['is_business_account']
		self.business_category_name    = user['business_category_name']
		self.blocked_by_viewer         = user['blocked_by_viewer']
		self.connected_fb_page         = user['connected_fb_page']
		self.followed_by_viewer        = user['followed_by_viewer']
		self.has_blocked_viewer        = user['has_blocked_viewer']
		self.requested_by_viewer       = user['requested_by_viewer']
		self.has_requested_viewer      = user['has_requested_viewer']
		self.highlight_reel_count      = user['highlight_reel_count']
		self.edge_follow               = user['edge_follow']['count']
		self.edge_followed_by          = user['edge_followed_by']['count']
		self.edge_saved_media          = user['edge_saved_media']
		self.edge_media_collections    = user['edge_media_collections']
		self.edge_mutual_followed_by   = user['edge_mutual_followed_by']
		self.edge_felix_video_timeline = user['edge_felix_video_timeline']
		self.post_count                = user['edge_owner_to_timeline_media']['count']
		self.has_next_page             = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
		self.end_cursor                = user['edge_owner_to_timeline_media']['page_info']['end_cursor']
		self.posts                     = [
			Post(post['node']) for post in user['edge_owner_to_timeline_media']['edges']
		]

	def add_posts(self, user):
		self.has_next_page = user['edge_owner_to_timeline_media']['page_info']['has_next_page']
		self.end_cursor    = user['edge_owner_to_timeline_media']['page_info']['end_cursor']
		for post in user['edge_owner_to_timeline_media']['edges']
			self.posts.append(Post(post['node']))
