import requests, random, json, time
from   bs4                 import BeautifulSoup
from   random              import choice
from   fake_useragent      import UserAgent
from   requests.exceptions import RequestException, ProxyError, HTTPError
from  .parameters          import parameters_proxy_list, default_option, enable_proxy, api_url_proxy_list, url_sslproxies, _user_agents
from ..exceptions.common   import IgRequestException

class Request:
	def __init__(self):
		self.user_agents   = _user_agents
		self.proxy         = None
		self.proxies       = parameters_proxy_list
		self.proxy_index   = -1
		self.enable_proxy  = enable_proxy

		if enable_proxy:
			print("[%s] Proxies enabled" % (time.strftime('%X')))
			self.get_proxy_list(default_option)

	def get_proxy_list(self, default=0):
		# scrapes a list of free proxies from https://www.sslproxies.org/
		if default is 1:
			print("[%s] Retrieving list of free proxies from https://www.sslproxies.org/" % (time.strftime('%X')))
			response       = requests.get(url_sslproxies, headers={'User-Agent': UserAgent().random})
			soup           = BeautifulSoup(response.content, 'html.parser')
			proxylisttable = soup.find(id='proxylisttable')
			self.proxies.clear()
			for row in proxylisttable.tbody.find_all('tr'):
				self.proxies.append({
					'ip':      row.find_all('td')[0].string,
					'port':    row.find_all('td')[1].string,
					'country': row.find_all('td')[3].string
				})
		# get a list of free proxies from https://www.proxy-list.download/api/v1/
		elif default is 2:
			print("[%s] Retrieving list of free proxies from https://www.proxy-list.download/ API" % (time.strftime('%X')))
			response     = requests.get(api_url_proxy_list, headers={'User-Agent': UserAgent().random})
			proxies_list = response.text.replace('\r', '').strip().split('\n')
			self.proxies.clear()
			for proxy in proxies_list:
				tokens = proxy.split(':')
				self.proxies.append({
					'ip':      tokens[0],
					'port':    tokens[1],
					'country': 'United States'
				})
		else:
			print("[%s] Using default proxy list from config" % (time.strftime('%X')))
			self.proxies = parameters_proxy_list

		self.select_proxy()
		return self.proxies

	def __random_agent(self):
		if self.user_agents and isinstance(self.user_agents, list):
			return choice(self.user_agents)
		return choice(_user_agents)

	def select_proxy(self, status=False, error=''):
		self.proxy_index = random.randint(0, len(self.proxies) - 1)
		self.proxy       = self.proxies[self.proxy_index]
		print("[%s]%s%sCurrent proxy: %s:%s Country: %s %s" % (
			time.strftime('%X'),
			' ' + str(error) + ' ' if error else ' ',
			'' if not (status) else '[Switching proxy] -> ',
			self.proxy['ip'],
			self.proxy['port'],
			self.proxy['country'],
			' ' * 30)
		)
		return self.proxy

	def __get_proxy(self):
		return self.proxy['ip'] + ':' + self.proxy['port']

	def is_enabled_proxy(self):
		return self.enable_proxy

	def get(self, url, stream=False):
		try:
			if self.enable_proxy:
				headers  = {'User-Agent': self.__random_agent()}
				proxies  = {'http':  self.__get_proxy(), 'https': self.__get_proxy()}
				response = requests.get(url, stream=stream, headers=headers, proxies=proxies, timeout=(3, 30))
			else:
				response = requests.get(url, headers={'User-Agent': self.__random_agent()}, timeout=(3, 30))
			response.raise_for_status()
		except HTTPError as e:
			raise IgRequestException('Received non 200 status code from Instagram')
		except ProxyError as p:
			raise IgRequestException('Proxy Error')
		except RequestException as r:
			raise IgRequestException('Request Error')
		except TimeoutError:
			raise IgRequestException('Timeout Error')
		except ConnectionRefusedError:
			raise IgRequestException('Connection Refused Error')
		except ConnectionResetError:
			raise IgRequestException('Connection Reset Error')
		except ConnectionError:
			raise IgRequestException('Connection Error')
		except Exception as e:
			print("*" * 100)
			raise e
		return response


request = Request()
