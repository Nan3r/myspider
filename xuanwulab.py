#coding:utf-8
#__author__='Nan3r'


import calendar,datetime,MySQLdb
from bs4 import BeautifulSoup
import sys,requests,re,json
reload(sys)
sys.setdefaultencoding('utf-8')

mysqlconfig = {
	'host': '127.0.0.1',
	'username': 'root',
	'userpwd': 'root',
	'dbname': 'lab'
}

'''
返回到当前日期的URL列表
'''
def get_url_list(start_year=2016, start_month=1, start_day=1):
	urls = []
	url_head = 'https://xuanwulab.github.io/cn/secnews/'
	nowtime = datetime.datetime.now()
	listtime = nowtime.strftime("%Y-%m-%d").split('-')
	for year in range(start_year, int(listtime[0])+1):
		for month in range(start_month, 13):
			day = calendar.monthrange(year,month)
			for day in range(start_day,int(day[1])+1):
				urls.append("{head}{year}/{month:0>2}/{day:0>2}/index.html".format(
					head=url_head,year=str(year),month=str(month),day=str(day)))
	return urls

def html2soup(url):
	headers = {
		'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
	}
	html = requests.get(url, headers=headers).text
	if html.find('http://example.com/') == -1:
		return BeautifulSoup(html,'lxml')
	return False

def mysql_insert(result):
	db = MySQLdb.connect(mysqlconfig['host'],mysqlconfig['username'],mysqlconfig['userpwd'],mysqlconfig['dbname'])
	cursor = db.cursor()

	# SQL 插入语句
	sql = "INSERT INTO info(type,content) VALUES"
	#print result
	for r in result:
		sql += ' (\''+r['typet']+'\', \''+r['content']+'\'),'
	sql = sql[:-1]
	print sql
	try:
	   cursor.execute(sql)
	   db.commit()
	except:
	   db.rollback()

	db.close()

def savetxt(result, count=0):
	with open('xuanwulab'+str(count)+'.txt','a+') as f:
		f.write(json.dumps(result)+'\n')

def main(save='txt'):
	urllist = get_url_list()
	typet = ''
	result = []
	tmp = {}

	for count,url in enumerate(urllist):
		soup = html2soup(url)
		print 'Crawl: {:.2f}%'.format(100*count/float(len(urllist)))
		if soup:
			p_tags = soup.find_all('p')
			for tag in p_tags:
				content = tag.get_text()
				try:
					typet = re.findall(r'\[(.*?)\]', content)[0].strip()
				except Exception as e:
					pass
				if typet:
					tmp['typet'] = typet.replace('\'', ' ').strip()
					tmp['content'] = content.replace('\'', ' ').strip()
					if save == 'mysql':
						result.append(tmp)
					if save == 'txt':
						savetxt(tmp, count/10)
						#print count
					tmp = {}
			if save == 'mysql':
				mysql_insert(result)
				result = []

	print 'crawl done,result svae in mysql!'

if __name__ == '__main__':
	'''
	type:
	1.txt(json形式)
	2.mysql

	本程序：单线程
	爬取一次，在运行脚本不能起更新作用，可以建一个文件记录上次爬取的日期来进行更新爬取
	mysql功能可能还有问题,每10天为一个TXT
	'''
	saveType = 'txt'
	main(saveType)