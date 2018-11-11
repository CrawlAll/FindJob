# -*- coding: utf-8 -*-
import json
import scrapy
from FindJob.items import FindJobItem


class LagouSpider(scrapy.Spider):
	name = 'lagou'
	allowed_domains = ['lagou.com']
	url = 'https://www.lagou.com/jobs/positionAjax.json'

	headers = {'Referer': 'https://www.lagou.com/jobs/list_python?px=default&gx=&isSchoolJob=1&city=%E5%8C%97%E4%BA%AC'}

	def start_requests(self):
		for page in range(1, 31):
			formdata = {'needAddtionalResult': 'false',
						'city': '北京',
						'first': 'true',
						'pn': str(page),
						'kd': 'python'
						}
			yield scrapy.FormRequest(self.url, headers=self.headers, formdata=formdata, callback=self.parse,
									 dont_filter=True)

	def parse(self, response):
		item = FindJobItem()
		text = response.text
		details = json.loads(text)
		result = details.get('content').get('positionResult').get('result')
		for info in result:
			unique_id = int("{}{}".format(info.get('companyId', 1), info.get('positionId', 2)))
			company_name = info.get('companyFullName')
			work_year = info.get('workYear')
			salary = info.get('salary')
			city = info.get('city')
			create_time = info.get('createTime')
			position_name = info.get('positionName')

			for field in item.fields:
				item[field] = eval(field)
			yield item
