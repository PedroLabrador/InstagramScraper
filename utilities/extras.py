import validators
from  .parameters        import parameters
from ..exceptions.common import ShortCodeException, UsernameException, TagnameException

base_url = "https://www.instagram.com/graphql/query/?query_hash=%s&variables=%s"

# Improve this method
def parse_url_or_username(url):
	if not validators.url(url):
		raise UsernameException ("Username error - Invalid URL")
	return "%s/?__a=1" % url if not url.endswith("/") else "%s?__a=1" % url

# Improve this method
def parse_url_or_shortcode(url):
	if not validators.url(url):
		raise ShortCodeException ("ShortCode error - Invalid URL")
	return url.split('/')[4]

#improve this method
def parse_url_or_tagname(url):
	if not validators.url(url):
		raise TagnameException ("Tagname error - Invalid URL")
	return url.split('/')[5]

def get_variables(params):
	return str({pmt:params[pmt] for pmt in params if params[pmt] != ''}).strip().replace(" ", "").replace("'", '"').replace("True", "true").replace("False", "false")

def create_url_user(profile_url, id='', after=''):
	params = parameters['user']

	if id:
		params['variables']['id']    = id
		params['variables']['after'] = after

		variables = get_variables(params['variables'])
		query_url = base_url % (params['query_hash'], variables)

		return query_url
	else:
		return parse_url_or_username(profile_url)

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
	