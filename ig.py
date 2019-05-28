import requests, json, validators
# import parameters, helpers
from parameters import parameters
from bs4 import BeautifulSoup
from pprint import pprint
from random import choice
from exceptions import ShortCodeException

# p = helpers.Parameters(parameters.data)

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

class InstagramScraper:
	def __init__(self, user_agents=None, proxy=None):
		self.user_agents = user_agents
		self.proxy       = proxy
		self.base_url    = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s"
		# self.parameters = helpers.Parameters(parameters.data)

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

	def extract_json_data(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		body = soup.find('body')
		script_tag = body.find('script')
		raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
		return json.loads(raw_string)

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
		print(query_url)
		return query_url

	def get_user_posts(self, profile_url, max_requests=5):
		nodes = []
		after = ''
		current_iteration = 0
		
		try:
			response  = self.__request_url(self.create_url_user(profile_url))
			json_data = json.loads(response)
			user  = json_data['graphql']['user']
			id    = user['id']
			posts = user['edge_owner_to_timeline_media']
			has_next_page = posts['page_info']['has_next_page']
			
			if user['is_private']:
				print("Private profile :(")
			else:
				for current in posts['edges']:
					nodes.append(current['node'])
	
				while True:
					current_iteration += 1

					if not has_next_page or current_iteration is max_requests:
						break
					else:
						after     = posts['page_info']['end_cursor']
						response  = self.__request_url(self.create_url_user(profile_url, id, after))
						json_data = json.loads(response)['data']['user']
						posts     = json_data['edge_owner_to_timeline_media']
						has_next_page = posts['page_info']['has_next_page']

						for current in posts['edges']:
							nodes.append(current['node'])

		except Exception as e:
			raise e

		return nodes

	def get_single_post(self, post_url):
		results = {}
		try:
			response  = self.__request_url(self.create_url_single_post(post_url))
			json_data = json.loads(response)
		except Exception as e:
			raise e

		# for key, value in metrics.items():
		# 	if key != 'edge_owner_to_timeline_media':
		# 		if value and isinstance(value, dict):
		# 			value = value['count']
		# 			results[key] = value
		# 		elif value:
		# 			results[key] = value
		# return results

	def get_post_likes(self, post_url, max_requests=5):
		nodes = []
		after = ''
		current_iteration = 0

		try:
			while True:
				response   = self.__request_url(self.create_url_likes(post_url, after))
				json_data  = json.loads(response)['data']['shortcode_media']['edge_liked_by']
				current_iteration += 1

				for edge in json_data['edges']:
					nodes.append(edge['node'])

				if not json_data['page_info']['has_next_page'] or current_iteration is max_requests:
					break
				else:
					after = json_data['page_info']['end_cursor']

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
i.get_user_posts("https://www.instagram.com/selenagomez/")
# i.check_users_liked("http://www.instagram.com/p/BwC3-fwH2dZ/", ['crovaz', 'andresraul7', 'roxanadpc', 'pedroool'])
