import requests, json, validators
from pprint import pprint
from random import choice
from otypes.user import User
from exceptions.common import ShortCodeException, UsernameException
from utilities.parameters import parameters

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

class InstagramScraper:
	def __init__(self, user_agents=None, proxy=None):
		self.user_agents = user_agents
		self.proxy       = proxy
		self.base_url    = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s"

	def __random_agent(self):
		if self.user_agents and isinstance(self.user_agents, list):
			return choice(self.user_agents)
		return choice(_user_agents)

	def __request_url(self, url):
		try:
			response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy, 'https': self.proxy})
			response.raise_for_status()
		except requests.HTTPError:
			raise requests.HTTPError('Received non 200 status code from Instagram')
		except requests.RequestException:
			raise requests.RequestException
		return response.text

	def get_variables(self, params):
		return str({pmt:params[pmt] for pmt in params if params[pmt] != ''}).strip().replace(" ", "").replace("'", '"').replace("True", "true").replace("False", "false")

	def parse_url_or_username(self, url):
		if not validators.url(url):
			raise UsernameException ("Username error - Invalid URL")
		return "%s/?__a=1" % url if not url.endswith("/") else "%s?__a=1" % url

	def parse_url_or_shortcode(self, url):
		if not validators.url(url):
			raise ShortCodeException("ShortCode error - Invalid URL")
		return url.split('/')[4]

	def create_url_user(self, url, id='', after=''):
		params = parameters['user']

		if not id:
			return self.parse_url_or_username(url)
		else:
			params['variables']['id']    = id
			params['variables']['after'] = after

			variables = self.get_variables(params['variables'])
			query_url = self.base_url % (params['query_hash'], variables)

			return query_url

	def create_url_single_post(self, url):
		params = parameters['single_post']
		params['variables']['shortcode'] = self.parse_url_or_shortcode(url)

		variables = self.get_variables(params['variables'])
		query_url = self.base_url % (params['query_hash'], variables)

		return query_url

	def create_url_likes(self, url, after=''):
		params = parameters['likes']
		params['variables']['shortcode'] = self.parse_url_or_shortcode(url)
		params['variables']['after'] = after

		variables = self.get_variables(params['variables'])
		query_url = self.base_url % (params['query_hash'], variables)
		
		return query_url

	def get_user(self, profile_url):
		user = {}
		try:
			response  = self.__request_url(self.create_url_user(profile_url))
			data      = json.loads(response)
			user      = User(data['graphql']['user'])
		except Exception as e:
			raise e
		return user

	def get_user_posts(self, profile_url, user={}, max_requests=5):
		try:
			if not user:
				response  = self.__request_url(self.create_url_user(profile_url))
				data      = json.loads(response)
				user      = User(data['graphql']['user'])
			
			if user.is_private:
				print("Private profile :(")
			else:
				iteration = 0
				while True:
					iteration += 1

					if not user.has_next_page or iteration is max_requests:
						print("this user ran out of posts")
						break
					else:
						response  = self.__request_url(self.create_url_user(profile_url, user.id, user.end_cursor))
						data      = json.loads(response)
						user.add_posts(data['data']['user'])

		except Exception as e:
			raise e

		return user.posts

	def get_single_post(self, post_url):
		post = {}
		try:
			response  = self.__request_url(self.create_url_single_post(post_url))
			data = json.loads(response)
			post = Post(data['data']['shortcode_media'])
		except Exception as e:
			raise e

		return post

	def get_post_likes(self, post_url, max_requests=5):
		nodes = []
		after = ''

		try:
			iteration = 0
			while True:
				response   = self.__request_url(self.create_url_likes(post_url, after))
				data       = json.loads(response)['data']['shortcode_media']['edge_liked_by']
				iteration += 1

				for edge in data['edges']:
					nodes.append(edge['node'])

				if not data['page_info']['has_next_page'] or iteration is max_requests:
					break
				else:
					after = data['page_info']['end_cursor']

		except Exception as e:
			raise e

		return nodes

	def check_users_liked(self, post_url, users):
		nodes = self.get_post_likes(post_url)
		for user in users:
			liked = False
			for node in nodes:
				if user == node['username']:
					liked = True
					break
			if not liked:
				print("User: %s did not like the photo" % user)
			else:
				print("User: %s did like the photo" % user)


i = InstagramScraper()
i.get_user_posts("https://www.instagram.com/pedroool/")
# i.get_single_post("http://www.instagram.com/p/BwC3-fwH2dZ/")
# i.check_users_liked("http://www.instagram.com/p/BwC3-fwH2dZ/", ['crovaz', 'andresraul7', 'roxanadpc', 'pedroool'])
