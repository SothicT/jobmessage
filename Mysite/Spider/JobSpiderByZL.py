import requests
import pymysql
from bs4 import BeautifulSoup
from Spider.MyLog import MyLog as mylog


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

class GetJobMessagebyzl(object):
    startpage = None
    endpage = None
    jobname = None
    table_name = None
    def __init__(self, jobname, startpage, endpage, table_name):
        self.urls = []
        self.log = mylog()
        self.set_jobname(jobname)
        self.set_startnum(startpage)
        self.set_endpage(endpage)
        self.set_table_name(table_name)
        self.geturls()
        self.items = self.spider(self.urls)
        self.Print_JobMessage(self.items)
        self.Save_Into_MysqlDB(self.items)

    def set_jobname(self, jobname):
        self.jobname = jobname

    def get_jobname(self):
        return self.jobname

    def set_startnum(self, startpage):
        self.startpage = startpage

    def get_startpage(self):
        return self.startpage

    def set_endpage(self, endpage):
        self.endpage = endpage

    def get_endpage(self):
        return self.endpage

    def set_table_name(self, table_name):
        self.table_name = table_name

    def get_table_name(self):
        return self.table_name

    def geturls(self):            #获取爬取网页的URL
        jobname = self.jobname
        startpage = self.get_startpage()
        endpage = self.get_endpage()
        for i in range(startpage, endpage + 1):
            Pageurl = r'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=' + str(jobname) + '&sm=0&p=' + str(
                i)+'&isfilter=0&fl=489&isadv=0&sb=1'
            htmlContent = self.getResponseContent(Pageurl)
            soup = BeautifulSoup(htmlContent, 'lxml')
            # print('测试表头：\n' + soup.find_all('table', attrs={'class': 'newlist'})[0])   # This is a test line
            tags = soup.find_all('table', attrs={'class': 'newlist'})
            test = 1
            for tag in tags:
                if tag.find('td', attrs={'class': 'zwmc'}):
                    url = tag.find('td', attrs = {'class' : 'zwmc'}).find('a').get('href')
                    print(str(test)+'测试url:\t%s' %url+'\t插入成功！')
                    self.urls.append(url)
                    test = test + 1
        # self.log.info(u'添加URL到：%s到URLS中' % Pageurl)

    def getResponseContent(self, url):      #通过requests获取url中的信息
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            self.log.info(u'python返回URL：%s数据成功' % url)
            return r.text
        except:
            self.log.info(u'python返回URL：%s 数据失败' % url)
            return "error"

    def spider(self, urls):         #爬取具体的URL中的相关信息
        JobMessageItems = []
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent, 'lxml')
            try:
                Tagli = soup.find('ul', attrs={'class': 'terminal-ul clearfix'}).find_all('li')
                item = JobMessageItem()
                item.GSname = soup.find('p', attrs={'class': 'company-name-t'}).find('a').get_text()
                item.GSlink = soup.find('p', attrs={'class': 'company-name-t'}).find('a').get('href')
                item.ZWname = Tagli[7].find('strong').find('a').get_text()
                item.ZWsalary = Tagli[0].find('strong').get_text()
                item.ZWadd = Tagli[1].find('strong').get_text()
                item.date = Tagli[2].find('strong').get_text()
                item.ZWtype = Tagli[3].find('strong').get_text()
                item.ZWexp = Tagli[4].find('strong').get_text()
                item.ZDedu = Tagli[5].find('strong').get_text()
                item.ZWnum = Tagli[6].find('strong').get_text()
                tagli = soup.find('ul', attrs={'class': 'terminal-ul clearfix terminal-company mt20'}).find_all('li')
                item.ZWnature = tagli[2].find('strong').get_text()  # 2018-3-14  22:00
                item.ZWinfo = soup.find('div', attrs={'class': 'tab-inner-cont'}).get_text()
                JobMessageItems.append(item)
                self.log.info(u'获取数据成功')
            except AttributeError as e:
                print(e)
                continue
                print('测试保存数据：' + str(test) + '条成功！\t')
            '''
            tags = soup.find_all('table', attrs={'class': 'newlist'})
            for tag in tags:
                if (tag.find('td', attrs={'class': 'zwmc'})):
                    test = test + 1
                    item = JobMessageItem()
                    item.ZWname = tag.find('td', attrs={'class': 'zwmc'}).get_text()
                    item.GSname = tag.find('td', attrs={'class': 'gsmc'}).get_text()
                    item.GSlink = tag.find('td', attrs={'class': 'gsmc'}).find('a').get('href')
                    item.ZWsalary = tag.find('td', attrs={'class': 'zwyx'}).get_text()
                    item.date = tag.find('td', attrs={'class': 'gxsj'}).get_text()
                    Span = tag.find('li', attrs={'class': 'newlist_deatil_two'}).find_all('span')
                    item.ZWadd = tag.find('td', attrs={'class': 'gzdd'}).get_text()
                    item.ZWtype = Span[1].get_text()
                    item.ZWnature = Span[2].get_text()
                    item.ZWexp = Span[3].get_text()
                    item.ZDedu = Span[4].get_text()
                    item.ZWinfo = tag.find('li', attrs={'class': 'newlist_deatil_last'}).get_text()
                    JobMessageItems.append(item)
                    #self.log.info(u'获取数据成功')
                    print('测试保存数据：'+str(test)+'条成功！\t')
            '''
        return JobMessageItems

    def Print_JobMessage(self, items):
        num = 0
        for item in items:
            num = num + 1
            print(u'\n测试打印数据：%s' %str(num)+'\n'+item.GSname, item.GSlink, item.ZWadd, item.ZWname, item.ZWinfo,
               item.ZWnature, item.ZWexp, item.ZDedu, item.ZWtype, item.ZWsalary, item.date)

    def Save_Into_MysqlDB(self, items):             #将爬取的信息保存到本地数据库中
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
                sql = "INSERT INTO "+ table_name +"(GSname,GSlink,ZWname,ZWsalary,ZWtype,ZWexp,ZWadd,ZWnature,ZDedu,ZWnum,date,ZWinfo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"           #2018-3-13 17：36
                for item in items:
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
                    print(data)
                    cursor.execute(sql, data)
                    connect.commit()
                self.log.info(u'数据写入MySql数据库成功！')
        except AttributeError as e:
            return "import Error"
        finally:
            cursor.close()
            connect.close()

if __name__ == '__main__':
    Jobmessage = GetJobMessagebyzl('图像处理', 1, 2, 'jobsite_jobmessagebyzl')
    print(Jobmessage.get_jobname(), Jobmessage.get_table_name())
