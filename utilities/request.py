import requests
from random import choice

_user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

class Request:
	def __init__(self, user_agents=None, proxy=None):
		self.user_agents = _user_agents
		self.proxy       = proxy

	def __random_agent(self):
		if self.user_agents and isinstance(self.user_agents, list):
			return choice(self.user_agents)
		return choice(_user_agents)

	def url(self, url):
		try:
			response = requests.get(url, headers={'User-Agent': self.__random_agent()}, proxies={'http': self.proxy, 'https': self.proxy})
			response.raise_for_status()
		except requests.HTTPError:
			raise requests.HTTPError('Received non 200 status code from Instagram')
		except requests.RequestException:
			raise requests.RequestException
		return response.text
