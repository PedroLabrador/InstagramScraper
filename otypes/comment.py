class Comment:
	def __init__(self, comment):
		self.id                     = comment['id']
		self.text                   = comment['text']
		self.created_at             = comment['created_at']
		self.owner_id               = comment['owner']['id']
		self.owner_username         = comment['owner']['username']
		self.profile_url            = "https://instagram.com/%s/" % comment['owner']['username']
		self.owner_is_verified      = comment['owner']['is_verified']
		self.owner_profile_pic_url  = comment['owner']['profile_pic_url']
		self.edge_liked_by          = comment['edge_liked_by']
		self.did_report_as_spam     = comment['did_report_as_spam']
		self.edge_threaded_comments = comment['edge_threaded_comments']

	def __repr__(self):
		return self.owner_username + ' - ' + self.text

	def __str__(self):
		return self.owner_username + ' - ' + self.text
	
	def toJSON(self):
		return {
			'id':                     self.id,
			'text':                   self.text,
			'created_at':             self.created_at,
			'owner_id':               self.owner_id,
			'owner_username':         self.owner_username,
			'profile_url':            self.profile_url,
			'owner_is_verified':      self.owner_is_verified,
			'owner_profile_pic_url':  self.owner_profile_pic_url,
			'edge_liked_by':          self.edge_liked_by,
			'did_report_as_spam':     self.did_report_as_spam,
			'edge_threaded_comments': self.edge_threaded_comments,
		}