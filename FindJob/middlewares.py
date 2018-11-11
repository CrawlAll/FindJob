# -*- coding: utf-8 -*
import json
import logging
import requests
import fake_useragent

logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):

	def process_request(self, request, spider):
		ua = fake_useragent.UserAgent()
		request.headers.setdefault("User-Agent", ua.random)


class RandomProxyMiddleware(object):
	def __init__(self, proxy_url):
		self.proxy_url = proxy_url

	@classmethod
	def from_crawler(cls, crawler):
		settings = crawler.settings
		print(settings)
		return cls(proxy_url=settings.get('PROXY_URL'))

	def get_random_proxy(self):
		try:
			response = requests.get(self.proxy_url)
			if response.status_code == 200:
				proxy = response.text
				return proxy
		except requests.ConnectionError:
			return False

	def process_request(self, request, spider):
		if request.meta.get('keyword') or request.meta.get('retry_times'):
			request.meta['keyword'] = None
			proxy = self.get_random_proxy()
			if proxy:
				uri = 'https://{proxy}'.format(proxy=proxy)
				logger.info('使用代理%s' % proxy)
				request.meta['proxy'] = uri


class CheckResponseMiddleware(object):
	def process_response(self, request, response, spider):
		details = json.loads(response.text)
		# 返回的内容中 判断是否出现 ip被封情况
		if details.get('success'):
			return response
		else:
			logger.error('CheckResponseMiddleware')
			request.meta['keyword'] = '请重试'
			return request
