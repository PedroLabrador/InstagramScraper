import json

class Like:
	def __init__(self, like):
		self.id                  = like['id']
		self.username            = like['username']
		self.profile_url         = "https://instagram.com/%s/" % like['username']
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

	def toJSON(self):
		return {
			'id':                  self.id,                                    
			'username':            self.username,                        
			'profile_url':         self.profile_url,                        
			'full_name':           self.full_name,                      
			'is_private':          self.is_private,                    
			'is_verified':         self.is_verified,                  
			'profile_pic_url':     self.profile_pic_url,          
			'followed_by_viewer':  self.followed_by_viewer,    
			'requested_by_viewer': self.requested_by_viewer,  
		}
		