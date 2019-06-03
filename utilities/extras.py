import validators
from  .parameters        import parameters
from ..exceptions.common import ShortCodeException, UsernameException, TagnameException

instagram_url = "https://www.instagram.com/%s/?__a=1"
base_url      = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s"

def parse_url_or_username(string):
	if validators.url(string):
		return ("%s/?__a=1" if not string.endswith("/") else "%s?__a=1") % string
	if '@' in string:
		string = string.replace('@', '').strip()
	if '/' in string:
		string = string.strip('/')
	for char in string:
		if not char.isalnum() and char not in ('_', '.'):
			raise UsernameException ("Username error")
	return instagram_url % string

def parse_url_or_shortcode(string):
	if validators.url(string):
		if not '/p/' in string or len(string.split('/')[4]) < 8:
			raise ShortCodeException ("ShortCode error")
		return string.split('/')[4]
	string = string.strip('/')
	for char in string:
		if not char.isalnum() and char not in ('-', '_'):
			raise ShortCodeException ("ShortCode error")
	return string

def parse_url_or_tagname(string):
	if validators.url(string):
		if not '/explore/' in string and not '/tags/' in string:
			raise TagnameException ("Tagname error")
		return string.split('/')[5]
	string = string.strip('/')
	for char in string:
		if not char.isalnum() and char not in ('-', '_'):
			raise TagnameException ("Tagname error")
	return string

def get_variables(params):
	return str({pmt:params[pmt] for pmt in params if params[pmt] != ''}).strip().replace(" ", "").replace("'", '"').replace("True", "true").replace("False", "false")

def create_url_user(profile, id='', after=''):
	params = parameters['user']

	if id:
		params['variables']['id']    = id
		params['variables']['after'] = after

		variables = get_variables(params['variables'])
		query_url = base_url % (params['query_hash'], variables)

		return query_url
	else:
		return parse_url_or_username(profile)

def create_url_single_post(post_url):
	params = parameters['single_post']
	params['variables']['shortcode'] = parse_url_or_shortcode(post_url)

	variables = get_variables(params['variables'])
	query_url = base_url % (params['query_hash'], variables)

	return query_url

def create_url_likes(post_url, after=''):
	params = parameters['likes']
	params['variables']['shortcode'] = parse_url_or_shortcode(post_url)
	params['variables']['after'] = after

	variables = get_variables(params['variables'])
	query_url = base_url % (params['query_hash'], variables)
	
	return query_url

def create_url_comments(post_url, after=''):
	params = parameters['comments']
	params['variables']['shortcode'] = parse_url_or_shortcode(post_url)
	params['variables']['after'] = after

	variables = get_variables(params['variables'])
	query_url = base_url % (params['query_hash'], variables)
	
	return query_url

def create_url_hashtag(hashtag_url, first='', after=''):
	params = parameters['hashtag']
	params['variables']['tag_name'] = parse_url_or_tagname(hashtag_url)
	if first:
		params['variables']['first'] = first
	params['variables']['after']    = after

	variables = get_variables(params['variables'])
	query_url = base_url % (params['query_hash'], variables)
	return query_url
	