# -*- coding: utf-8 -*-
import pymysql


class FindJobPipeline(object):
	def __init__(self, host, dbname, user, pwd, port):
		self.host = host
		self.dbname = dbname
		self.user = user
		self.pwd = pwd
		self.port = port

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			host=crawler.settings.get('MYSQL_HOST'),
			dbname=crawler.settings.get('MYSQL_DBNAME'),
			user=crawler.settings.get('MYSQL_USER'),
			pwd=crawler.settings.get('MYSQL_PASSWD'),
			port=crawler.settings.get('MYSQL_PORT')
		)

	def open_spider(self, spider):
		self.connect = pymysql.connect(host=self.host, db=self.dbname, user=self.user, passwd=self.pwd, port=self.port,
									   charset='utf8', use_unicode=True)
		# 通过cursor执行增删查改
		self.cursor = self.connect.cursor()

	def process_item(self, item, spider):
		try:
			sql = """INSERT INTO find_job(unique_id, position_name, work_year, salary, company_name, city, create_time) VALUES \
(%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE position_name=%s, work_year=%s, salary=%s, company_name=%s, city=%s, create_time=%s"""
			params = (item['unique_id'], item['position_name'], item['work_year'], item['salary'], item['company_name'],
					  item['city'], item['create_time'],
					  item['position_name'], item['work_year'], item['salary'], item['company_name'], item['city'],
					  item['create_time'])
			self.cursor.execute(sql, params)
			self.connect.commit()

		except Exception as ex:
			spider.logger.error(ex)

		return item

	def close_spider(self, spider):
		self.connect.close()
