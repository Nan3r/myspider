#coding:utf-8

#get xuanwulab info to search
#author: Nan3r

from requests_html import HTMLSession
import re,datetime 

def writeHtml(filename, text):
	with open(filename, 'a+') as f:
		f.write(text+"\n")

def main(url, session):
	#url = 'http://xuanwulab.github.io/cn/secnews/2018/01/09/index.html'
	sel1 = 'div.singleweibotext'
	sel2 = 'div.singlefeedtext'

	htmlse = session.get(url)
	res1 = htmlse.html.find(sel1)
	res2 = htmlse.html.find(sel2)
	res = res1 + res2
	if len(res) > 0:
		for i in res:
			try:
				classname = re.match(r'\[(.*?)\]', i.text).group(1)
				writeHtml(classname.strip()+'.txt', i.text)
			except Exception as e:
				writeHtml('write.log', i.text)

if __name__ == '__main__':
	'''
	main
	'''
	session = HTMLSession()
	url = 'http://xuanwulab.github.io/cn/secnews/'

	'''
	#first spider
	start='2016-01-01'  
	end=str(datetime.date.today())
	datestart=datetime.datetime.strptime(start,'%Y-%m-%d')  
	dateend=datetime.datetime.strptime(end,'%Y-%m-%d')  
	while datestart<dateend:
		datestart+=datetime.timedelta(days=1)
		main(url+datestart.strftime('%Y/%m/%d/'), session)
	'''

	'''
	cron spider
	'''
	today = str(datetime.date.today()).replace('-', '/') + '/'
	main(url+today, session)
