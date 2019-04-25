import requests
import re
import pymysql
from bs4 import BeautifulSoup
from MyLog import MyLog as mylog

class JobMessageItem(object):
    GSname = None
    GSlink = None
    ZWname = None
    ZWsalary = None
    ZWtype = None
    ZWexp = None
    ZWadd = None
    ZWnature = None
    ZDedu = None
    date = None
    ZWinfo = None
    ZWnum = None

class GetJobMessageby51(object):
    jobname = None
    start_page = None
    end_page = None
    table_name = None

    def __init__(self, jobname, start_page, end_page, table_name):
        self.urls = []
        self.log = mylog()
        self.set_jobname(jobname)
        self.set_table_name(table_name)
        self.set_start_page(start_page)
        self.set_end_page(end_page)
        self.table_name = table_name
        self.geturls()
        self.items = self.spider(self.urls)
        # self.PrintJobMessage(self.items, 1)       #2018-3-15 21:20

    def set_start_page(self, strat_page):
        self.start_page = strat_page

    def get_start_page(self):
        return self.start_page

    def set_end_page(self, end_page):
        self.end_page = end_page

    def get_end_page(self):
        return self.end_page

    def set_jobname(self, jobname):
        self.jobname = jobname

    def get_jobname(self):
        return self.jobname

    def set_pagenum(self, pagenum):
        self.pagenum = pagenum

    def get_pagenum(self):
        return self.pagenum

    def set_table_name(self, table_name):
        self.table_name = table_name

    def get_table_name(self):
        return self.table_name

    def geturls(self):
        strat_page = self.get_start_page()
        end_page = self.get_end_page()
        jobname = self.get_jobname()
        # print(PageNum, jobname)
        for i in range(strat_page, end_page+1):
            Pageurl = r'https://search.51job.com/list/000000,000000,0000,00,9,99,'+str(jobname)+',2,'+str(i) + '.html'
            htmlContent = self.getResponseContent(Pageurl)
            soup = BeautifulSoup(htmlContent, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'el'})
            for div in divs:
                try:
                    if div.find('p', attrs={'class': 't1'}).find('a'):
                        url = div.find('p', attrs={'class': 't1'}).find('a').get('href')
                        self.urls.append(url)
                        # print(div)    # this is a test line
                except Exception as e:
                    continue
        self.log.info(u'添加url到：%s URLS中' % Pageurl)

    def getResponseContent(self, url):  # 通过requests获取url中的信息
        try:
            r = requests.get(url, timeout=8)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.log.info(u'python返回URL：%s数据成功' % url)
            return r.text
        except Exception as e:
            self.log.info(e)
            self.log.info(u'python返回URL：%s 数据失败' % url)
            return "error"

    def spider(self, urls):
        JobMessageItems = []
        # print(urls)
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent, 'lxml')
            try:
                item = JobMessageItem()
                spans = soup.find('div', attrs={'class': 'tCompany_main'}).find_all('span', attrs={'class': 'sp4'})
                item.GSname = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('p', attrs={'class': 'cname'}).get_text()
                item.GSlink = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('p', attrs={'class': 'cname'}).find('a').get('href')
                item.ZWname = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('h1').get_text()
                item.ZWadd = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('span').get_text()      # 2018-3-16 18:13
                item.ZWsalary = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('strong').get_text()
                item.ZWtype = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('p', attrs={'class': 'msg ltype'}).get_text().strip()
                item.ZWexp = spans[0].get_text()
                item.ZWnum = spans[2].get_text()
                item.ZWinfo = soup.find('div', attrs={'class': 'tmsg inbox'}).get_text()
                item.ZWnature = soup.find('div', attrs={'class': 'tHeader tHjob'}).find('p', attrs={'class': 'msg ltype'}).get_text().strip()
                item.date = spans[3].get_text()
                item.ZDedu = spans[1].get_text()                                              # 2018-4-9 21:02
                # print(item.ZWnum, item.ZDedu, item.ZWexp, item.date)   # this is a test line
                self.log.info(u'获取数据成功')
                self.Save_Into_MysqlDB(item)
            except Exception as e:
                print(e)
                continue


    def Save_Into_MysqlDB(self, item):
        table_name = self.table_name
        connect = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='19950815',
            db='jobmessage',
            charset='utf8')
        try:
            with connect.cursor() as cursor:
                sql = "INSERT INTO " + table_name + "(GSname,GSlink,ZWname,ZWsalary,ZWtype,ZWexp,ZWadd,ZWnature,ZDedu,ZWnum,date,ZWinfo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 2018-3-13 17：36
                GSname = item.GSname.encode('utf8')
                GSlink = item.GSlink.encode('utf8')
                ZWname = item.ZWname.encode('utf8')
                ZWsalary = item.ZWsalary.encode('utf8')
                ZWtype = item.ZWtype.encode('utf8')
                ZWexp = item.ZWexp.encode('utf8')
                ZWadd = item.ZWadd.encode('utf8')
                ZWnature = item.ZWnature.encode('utf8')
                ZDedu = item.ZDedu.encode('utf8')
                ZWnum = item.ZWnum.encode('utf8')
                date = item.date.encode('utf8')
                ZWinfo = item.ZWinfo.encode('utf8')
                data = (GSname, GSlink, ZWname, ZWsalary, ZWtype, ZWexp, ZWadd, ZWnature, ZDedu, ZWnum, date, ZWinfo)
                # print(data)
                cursor.execute(sql, data)
                connect.commit()
                self.log.info(u'数据写入MySql数据库成功！')
        except AttributeError as e:
            return "import Error"
        finally:
            cursor.close()
            connect.close()

if __name__ == '__main__':
    jobmessage1 = GetJobMessageby51('python', 1, 400, 'jobsite_jobmessageby51')                  # 2018-4-10 12:00


