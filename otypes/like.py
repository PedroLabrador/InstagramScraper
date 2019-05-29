class Like:
	def __init__(self, like):
		self.id                  = like['id']
		self.username            = like['username']
		self.full_name           = like['full_name']
		self.is_private          = like['is_private']
		self.is_verified         = like['is_verified']
		self.profile_pic_url     = like['profile_pic_url']
		self.followed_by_viewer  = like['followed_by_viewer']
		self.requested_by_viewer = like['requested_by_viewer']
		self.reel                = like['reel']

	def __repr__(self):
		return self.username

	def __str__(self):
		return self.username
		