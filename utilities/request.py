import requests, random
from  bs4            import BeautifulSoup
from  random         import choice
from  fake_useragent import UserAgent
from .parameters     import proxy_list, enable_proxy, _user_agents

class Request:
	def __init__(self):
		self.user_agents   = _user_agents
		self.proxy         = None
		self.proxies       = proxy_list
		self.proxy_index   = -1
		self.enable_proxy  = enable_proxy

		if enable_proxy:
			print("Proxies enabled")
			self.select_proxy()

	# scrapes a list of free proxies from https://www.sslproxies.org/
	def get_proxy_list(self):
		response       = requests.get('https://www.sslproxies.org/', headers={'User-Agent': UserAgent().random})
		soup           = BeautifulSoup(response.content, 'html.parser')
		proxylisttable = soup.find(id='proxylisttable')
		for row in proxylisttable.tbody.find_all('tr'):
			self.proxies.append({
				'ip':      row.find_all('td')[0].string,
				'port':    row.find_all('td')[1].string,
				'https':   row.find_all('td')[6].string,
				'country': row.find_all('td')[3].string
			})
		self.select_proxy()

	def __random_agent(self):
		if self.user_agents and isinstance(self.user_agents, list):
			return choice(self.user_agents)
		return choice(_user_agents)

	def select_proxy(self, status=False):
		self.proxy_index = random.randint(0, len(self.proxies) - 1)
		self.proxy       = self.proxies[self.proxy_index]
		print("%sCurrent proxy: %s:%s Https: %s Country: %s %s" % (
			'' if not (status) else '[Changing proxy] -> ',
			self.proxy['ip'],
			self.proxy['port'],
			self.proxy['https'],
			self.proxy['country'],
			' ' * 30)
		)

	def __get_proxy(self):
		return self.proxy['ip'] + ':' + self.proxy['port']

	def is_enabled_proxy(self):
		return self.enable_proxy

	def get(self, url, stream=False):
		try:
			if self.enable_proxy:
				headers  = {'User-Agent': self.__random_agent()}
				proxies  = {'http':  self.__get_proxy(), 'https': self.__get_proxy()}
				response = requests.get(url, stream=stream, headers=headers, proxies=proxies)
			else:
				response = requests.get(url, headers={'User-Agent': self.__random_agent()})
			response.raise_for_status()
		except requests.HTTPError as e:
			raise requests.HTTPError('Received non 200 status code from Instagram')
		except requests.RequestException as r:
			raise requests.RequestException
		return response


request = Request()
