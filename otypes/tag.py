import json, time
from ..utilities.request import request
from ..utilities.extras  import create_url_user
from ..exceptions.common import IgRequestException

class TaggedUser:
	def __init__(self, user):
		self.id                        = user['id']
		self.username                  = user['username']
		self.biography                 = user['biography']
		self.full_name                 = user['full_name']
		self.profile_url               = 'https://instagram.com/%s/' % (user['username'])
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
		self.edge_mutual_followed_by   = user['edge_mutual_followed_by']
		self.post_count                = user['edge_owner_to_timeline_media']['count']

class Tag:
	def __init__(self, tag, shortcode=''):
		self.full_name       = tag['full_name']
		self.id              = tag['id']
		self.is_verified     = tag['is_verified']
		self.profile_pic_url = tag['profile_pic_url']
		self.username        = tag['username']
		self.profile_url     = "https://instagram.com/%s/" % tag['username']
		self.tagged_in       = shortcode
		self.user            = {}

	def __repr__(self):
		return self.username

	def __str__(self):
		return self.username

	def toJSON(self):
		return {
			'full_name':       self.full_name,
			'id':              self.id,
			'is_verified':     self.is_verified,
			'profile_pic_url': self.profile_pic_url,
			'username':        self.username,
			'profile_url':     self.profile_url
		}

	def check_profile(self, current):
		try:
			print("[%s] [%s] Checking %s profile %s" % (time.strftime('%X'), current, self.username, ' ' * 10), end="\r", flush=True)
			response     = request.get(create_url_user(self.profile_url))
			data         = json.loads(response.text)
			self.user    = TaggedUser(data['graphql']['user'])
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True, error=r)
				self.check_profile(current)
			else:
				raise r
		except Exception as e:
			raise e
