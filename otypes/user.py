import json, time
from  .post              import Post
from ..utilities.extras  import create_url_user, create_url_single_post
from ..utilities.request import request
from ..exceptions.common import IgRequestException

class User:
	def __init__(self, user, reset_posts=False):
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
		self.reset_posts = reset_posts

		# Deletes the already saved posts
		if self.reset_posts:
			self.posts.clear()
			self.end_cursor    = ''
			self.reset_posts   = False
			self.has_next_page = True

	def __repr__(self):
		return self.username

	def __str__(self):
		return self.username

	def find_post(self, shortcode):
		for post in self.posts:
			if shortcode == post.shortcode:
				return post

	def get_info(self):
		info = (
			"Username:    @%s\n"
			"Biography:   %s\n"
			"Full Name:   %s\n"
			"Profile url: %s\n"
			"Followers:   %s\n"
			"Following:   %s\n"
		) % (
			self.username,
			self.biography,
			self.full_name,
			self.profile_url,
			self.edge_followed_by,
			self.edge_follow
		)
		return info

	def status(self):
		return ({
			'post_count':    self.post_count,
			'scraped_posts': len(self.posts),
			'has_next_page': self.has_next_page
		})

	def get_posts_request(self, max_requests=5, aggresive=False, it=0):
		try:
			if self.is_private:
				print("[%s] Private profile :(\nCannot retrieve posts" % (time.strftime('%X')))
			else:
				iteration = it
				while True:
					print("[%s] [Request #%s] %s" % (time.strftime('%X'), iteration, self.status()), end="\r", flush=True)
					if not self.has_next_page or (iteration is max_requests and not aggresive):
						break
					else:
						response  = request.get(create_url_user(self.profile_url, self.id, self.end_cursor))
						data      = json.loads(response.text)['data']['user']['edge_owner_to_timeline_media']
						iteration += 1

						self.has_next_page = data['page_info']['has_next_page']
						self.end_cursor    = data['page_info']['end_cursor']

						for edge in data['edges']:
							self.posts.append(Post(edge['node']))
				print("[%s] status posts: %s" % (time.strftime('%X'), self.status()))
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True, error=r)
				self.get_posts_request(max_requests, aggresive, iteration)
			else:
				raise r
		except Exception as e:
			raise e

		return self.posts

	def get_posts_videos_request(self, videos=[]):
		try:
			for post in self.posts:
				if post.is_video and post.shortcode not in videos:
					print("[%s] [Requesting Video Post %s]" % (time.strftime('%X'), post.shortcode), end="\r", flush=True)
					response = request.get(create_url_single_post(post.post_url))
					data     = json.loads(response.text)
					post.update_video_data(data['data']['shortcode_media'])
					videos.append(post.shortcode)
		except IgRequestException as r:
			if request.is_enabled_proxy():
				request.select_proxy(status=True, error=r)
				self.get_posts_videos_request(videos)
			else:
				raise r
		except Exception as e:
			raise e
		return [post for post in self.posts if post.is_video]

	def retrieve_tagged_users(self):
		tags      = []
		usernames = []
		for post in self.posts:
			for tag in post.edge_media_to_tagged_user:
				if not tag.username in usernames:
					usernames.append(tag.username)
					tags.append(tag)
		return tags

	def get_likes_and_comments_request(self, max_requests=5, aggresive=False):
		for post in self.posts:
			if not post.edge_liked_by:
				post.get_likes_request(max_requests, aggresive)
			if not post.edge_comment_by:
				post.get_comments_request(max_requests, aggresive)

	def save_posts_to_json(self, all=False):
		if self.posts:
			with open(self.username + '_posts.json', 'w') as f:
				json.dump([post.toJSON() for post in self.posts], f)
			print("[%s] %s saved into the current directory" % (time.strftime('%X'), self.username + '_posts.json'))
