# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import MySQLdb
#from joke.myconfig import Dbconfig

import redis
from joke.myconfig import redisConfig

class JokePipeline(object):
    #def __init__(self):
    #   self.conn = MySQLdb.connect(user=Dbconfig['user'], passwd=Dbconfig['pwd'], db=Dbconfig['dbname'],
    #                              host=Dbconfig['host'], charset='utf8', use_unicode=True)
    # self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        #try:
        #   self.cursor.execute("INSERT into joke(content) values(%s)", item['content'])
        #   self.conn.commit()
        #except MySQLdb.Error,e:
        #   print 'Error'

        r = redis.Redis(host=redisConfig['host'], port=6379, password=redisConfig['pwd'])
        r.incr('num1')
        r.set(r.get('num1'), item['content'])  # 添加

        return item

