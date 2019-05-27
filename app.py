import requests, json
from bs4 import BeautifulSoup
from pprint import pprint
from random import choice

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

class InstagramScraper:

	def __init__(self, user_agents=None, proxy=None):
		self.user_agents = user_agents
		self.proxy = proxy

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

	def profile_page_metrics(self, profile_url):
		results = {}
		try:
			response = self.__request_url(profile_url)
			json_data = self.extract_json_data(response)
			metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']
		except Exception as e:
			raise e

		for key, value in metrics.items():
			if key != 'edge_owner_to_timeline_media':
				if value and isinstance(value, dict):
					value = value['count']
					results[key] = value
				elif value:
					results[key] = value
		return results

	def profile_page_recent_posts(self, profile_url):
		results = []
		try:
			response = self.__request_url(profile_url)
			json_data = self.extract_json_data(response)
			metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']["edges"]
		except Exception as e:
			raise e

		for key, node in enumerate(metrics):
			# if key > 1:
			# 	break
			node = node.get('node')
			if node and isinstance(node, dict):
				results.append(node)
		return results


k = InstagramScraper()
results = k.profile_page_recent_posts("https://www.instagram.com/selenagomez/")
pprint(results)

# page = requests.get("""
# 	https://www.instagram.com/graphql/query/?query_hash=477b65a610463740ccdb83135b2014db&variables={
# 		"shortcode":"BrwNjmlFYum",
# 		"child_comment_count":3,
# 		"fetch_comment_count":40,
# 		"parent_comment_count":24,
# 		"has_threaded_comments":true
# 	}""", headers={'User-Agent': _user_agents[0]}, proxies={'http': None, 'https': None})
# pprint(json.loads(page.content))