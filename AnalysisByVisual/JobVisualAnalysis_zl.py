import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from MyLog import MyLog as mylog


class JobAnalysisByZL(object):
    def __init__(self, filename, ResolveFileName):
        self.setfilename(filename)
        self.setResolvefilename(ResolveFileName)
        self.df = pd.read_json(self.filename)
        self.log = mylog()
        self.ResolveDataFrame()                   # 2018-3-20 已测试
        self.ShowJsonInfo()                       # 2018-3-19 已测试
        # self.VisualAnalysisBywork_num()           # 2018-3-23 已测试
        # self.VisualAnalysisByexp_num()            # 2018-3-24 已测试
        # self.VisaulAnalysisByedu_num()            # 2018-3-26 已测试
        # self.VisualAnalysisByexp_salary()         # 2018-4-2 已测试
        # self.VisualAnalysisBycity_salary()        # 2018-4-3 已测试
        # self.VisualAnalysisByedu_salary()         # 2018-4-5 已测试

    def setfilename(self, filename):

        self.filename = filename

    def getfilename(self):

        return self.filename

    def setResolvefilename(self, ResolveFileName):

        self.ResolveFileName = ResolveFileName

    def getResolveFileName(self):

        return self.ResolveFileName

    def ShowJsonInfo(self):

        self.log.info(u'显示DataFrame相关信息：')
        print(self.df.info())
        print('#'*100)
        print(self.df['ZWsalary'].value_counts(), self.df['ZWsalary'].count())
        print('#' * 100)
        print(self.df['ZWexp'].value_counts())
        print('#' * 100)
        print(self.df['ZDedu'].value_counts())
        print('#' * 100)

    def FindResolve(self):

        Resolve = pd.read_json(self.ResolveFileName)
        if Resolve.info:
            self.log.info(u'导入Resolve数据成功！')
        else:
            self.ResolveDataFrame()

    def ResolveDataFrame(self):
        self.log.info(u'开始进行json数据清洗')
        df = self.df
        # print(df['ZWsalary'].value_counts())  #This is a test line
        df['bottom'] = df['top'] = df['average'] = df["ZWsalary"]
        df['num'] = df['ZWnum']
        df['add'] = df['ZWadd']
        pattern = re.compile(r'\d+')          # 按数字对字符串进行匹配
        q1 = q2 = q3 = q4 = 0                 # q1代表8000-10000，q2代表10000以下，q3代表面议，q4代表统计失败
        for i in range(len(df['ZWsalary'])):  # 处理工资最高值与最低值以及平均值
            try:
                item = df['ZWsalary'].iloc[i].strip()
                if item == '面议':
                    continue
                print('数据处理中。。。', i, item)
                result = re.findall(pattern, item)
            except Exception as e:
                print(e)
                continue
            if result:
                try:     # 刑如“8000-10000月”形式
                    df['bottom'].iloc[i], df['top'].iloc[i] = int(result[0]), int(result[1])
                    df['average'].iloc[i] = str((int(result[0]) + int(result[1])) / 2)
                    q1 += 1
                    print('8000-10000月', i, result[0], result[1], df['bottom'].iloc[i], df['top'].iloc[i], df['average'].iloc[i])
                except:  # 刑如“10000月以下“形式
                    df['bottom'].iloc[i] = df['top'].iloc[i] = int(result[0])
                    df['average'].iloc[i] = str((int(result[0]) + int(result[0])) / 2)
                    q2 += 1
                    print('10000月以下', i, result[0], df['bottom'].iloc[i], df['top'].iloc[i], df['average'].iloc[i])
            else:
                df['bottom'].iloc[i] = df['top'].iloc[i] = 10000
                df['average'] = item
                print('面议', i, df['bottom'].iloc[i], df['top'].iloc[i], df['average'].iloc[i])
                q3 += 1
        print(df[['ZWsalary', 'bottom', 'top', 'average']].head(20))  # 2018-3-20 23:19
        print(q1, q2, q3, q4, q1 + q2 + q3 + q4)
        for i in range(len(df['ZWnum'])):  # 处理职位数量
            try:
                item = df['ZWnum'].iloc[i].strip()
                result = re.findall(pattern, item)
                if result:
                    print('数据处理中。。。', i, result[0], item.strip())    #This is a test line
                    df['num'].iloc[i] = result[0]
            except Exception as e:
                continue
        print('#'*150)
        print(df[['ZWnum', 'num']].head(5))         #This is a test line
        print('#' * 150)
        df_city = df['ZWadd'].copy()
        pattern2 = re.compile('(.*?)(\-)')          # 处理工作地点
        for i in range(len(df['ZWadd'])):
            item = df['ZWadd'].iloc[i].strip()
            result = re.search(pattern2, item)
            if result:
                print('数据处理中。。。', i, result.group(1).strip())
                df_city.iloc[i] = result.group(1).strip()
            else:
                print(item.strip())
                df_city.iloc[i] = item.strip()
        df['add'] = df_city
        print('#' * 150)
        print(df[['ZWadd', 'add']].head(10))  #This is a  test line
        print('#' * 150)
        print(df['add'].value_counts(), df['add'].value_counts().count())   #This is a  test line
        self.log.info(u'json数据清洗完毕')
        self.df = df
        print('#'*150)
        print(self.df[['ZWsalary', 'bottom', 'top', 'average']].head(20)) # This is a test line
        print('#'*150)
        self.df.to_json('Resolve.json')   #This ia a test line
        self.log.info(u'数据已写入Reslove.json中')

    def VisualAnalysisBywork_num(self):

        self.log.info(u'开始保存work_num分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        print(df['add'].value_counts(), "\ntotally line：", df['add'].value_counts().count())              #2018-3-21 18:26
        list_1 = df['add'].value_counts()
        # 开始绘制数据可视化图形
        plt.style.use('dark_background')
        fig = plt.figure(1, facecolor='black')  # 设置背景画布
        ax1 = fig.add_subplot(2, 1, 1, facecolor='#808080', alpha=0.3)  # 在视图中绘制子图，背景为灰色
        plt.tick_params(colors='white')
        df['add'].value_counts().plot(kind='bar', rot=0, color='cyan')
        # 设置标题和x轴与y轴
        plt.title('城市——职位数分布图', fontsize=20, color='yellow')        # 设置标题
        plt.xlabel('城市', fontsize=14, color='yellow')                       # 设置X轴轴标题
        plt.ylabel('职位数', fontsize=14, color='yellow')                     # 设置Y轴轴标题
        # 设置说明，位置在图的右上角
        text1 = ax1.text(25.05, 1400, u'数据来源:智联招聘', fontsize=13, color='#66FF66')
        text2 = ax1.text(25.05, 1250, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax1.text(25.05, 1100, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax1.text(25.05, 950, u'职位数量:共计6027(条)', fontsize=13, color='#66FF66')
        for i in range(30):
            ax1.text(i - 0.3, list_1[i], str(list_1[i]), color='yellow')
        # 可以用plt.grid(True)添加栅格线)
        ax2 = fig.add_subplot(2, 1, 2)  # 设置子图2，是位于子图1下面的饼状。
        x = df['add'].value_counts().values     # x是数值列表，pie图的比例根据数值占整体的比例而划分
        print(df['add'].value_counts(), x, len(x))      #This is line is test
        label_list = []        # label_list是构造的列表，装的是前8个城市的名称+职位占比。
        for i in range(8):
            t = df['add'].value_counts().values[i] / df['add'].value_counts().sum() * 100
            city = df['add'].value_counts().index[i]
            percent = str('%.1f%%' % t)
            label_list.append(city + percent)
        # print(label_list)
        labels = label_list + [''] * 132            #labels数量必须是城市数量的和
        # print(labels)
        explode = tuple([0.1] + [0] * 139)          #explode为tuple类型的值
        plt.pie(x, explode=explode, labels=labels, textprops={'color': 'white'})
        ax2.legend((u'北京', u'上海', u'深圳', u'广州', u'广州', u'成都', u'杭州', u'郑州', u'武汉'), fontsize=13, facecolor='black')
        plt.axis('equal')
        fig.set_size_inches(15.6, 10.8)
        plt.show()

    def VisualAnalysisByexp_num(self):

        self.log.info(u'开始保存exp_num分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # print(df['ZWexp'].value_counts(), df['ZWexp'].value_counts().count())   #This is a test line
        exp = df['ZWexp']
        # 开始绘制数据可视化图

        plt.style.use('dark_background')
        fig = plt.figure(2, facecolor='black')                                 ##808080为淡灰色
        ax1 = fig.add_subplot(2, 1, 1, facecolor='#808080', alpha=0.3)         #4f4f4f为灰色，#f06215为橙色
        plt.tick_params(colors='white')
        exp.value_counts().plot(kind='bar', rot=0, color='#7fc8ff')             #7fc8ff位青色
        plt.title('工作经验——职位数分布图', fontsize=18, color='yellow')
        plt.xlabel('工作经验', fontsize=14, color='yellow')
        plt.ylabel('职位数量', fontsize=14, color='yellow')
        plt.grid(True)
        ax1.text(5.05, 1750, u'数据来源:智联招聘', fontsize=13, color='#66FF66')
        ax1.text(5.05, 1600, u'职位关键词：Python', fontsize=13, color='#66FF66')
        ax1.text(5.05, 1450, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        ax1.text(5.05, 1300, u'职位数量:共计6027(条)', fontsize=13, color='#66FF66')
        explist = exp.value_counts().values
        for i in range(len(explist)):
            ax1.text(i - 0.1, explist[i], int(explist[i]), color='white')
        # 设置子图2，是位于子图1下面的饼状图
        ax2 = fig.add_subplot(2, 1, 2)
        # x是数值列表，pie图的比例根据数值占整体的比例而划分
        x2 = exp.value_counts().values
        labels = list(exp.value_counts().index[:5])+['']*2
        explode = tuple([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        plt.pie(x2, explode=explode, labels=labels, autopct='%1.1f%%', textprops={'color': 'white'})  #autopct是自动显示比例
        # 显示为等比例圆形
        plt.axis('equal')
        # 设置图例，方位为右下角
        ax2.legend(shadow=True, fontsize=12, edgecolor='cyan')
        fig.set_size_inches(15.6, 10.8)
        # plt.savefig('WorkAnalysisByExp_num.png')
        plt.show()

    def VisualAnalysisByexp_salary(self):

        self.log.info(u'开始保存exp_salary分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # average = df['average']
        # print(average.value_counts(), df['ZWsalary'], df['top'], df['bottom'])   # This is a test line
        df_ExpSalary = pd.DataFrame(data={'exp': df['ZWexp'], 'average': df['average']})
        pattern = re.compile('([0-9]+)')                #对average做类型装换，将str转换为float
        listi = []
        for i in range(len(df.average)):
            item = df.average.iloc[i].strip()
            result = re.findall(pattern, item)
            try:
                if result:
                    listi.append(float(result[0]))
                elif (item.strip() == 'found no element' or item.strip() == '面议'):
                    listi.append(np.nan)
                else:
                    print(item)
            except Exception as e:
                print(item, type(item), repr(e))
        df_ExpSalary['average'] = listi
        # print(type(df_ExpSalary['average']), df_ExpSalary['average'].value_counts().sum(), df_ExpSalary['average'].mean())     #This is a test line
        grouped = df_ExpSalary['average'].groupby(df_ExpSalary['exp'])
        # print(grouped.mean())   #This is a test line,用于显示工作经验和平均工资的关系      2018-3-25 22:40
        series = pd.Series(data={'average': df_ExpSalary['average'].mean()})         # 用于处理小数点位数
        result = grouped.mean().append(series)
        result.sort_values(ascending=False).round(1)                    # 将小数点后保存为一位，srot_values()方法用于排序
        print('#'*100)
        print(result.sort_values(ascending=False).round(1))           # This is a test line
        # 进行数据可视化绘图
        plt.style.use('dark_background')
        fig = plt.figure(3, facecolor='black')
        ax = fig.add_subplot(1, 1, 1, facecolor='#808080', alpha=0.3)
        result.sort_values(ascending=False).round(1).plot(kind='barh', rot=0)
        plt.title('工作经验——平均月薪分布图', fontsize=18, color='yellow')
        plt.xlabel('平均月薪', fontsize=14, color='yellow')
        plt.ylabel('工作经验', fontsize=14, color='yellow')
        list = result.sort_values(ascending=False).values
        for i in range(len(list)):
            ax.text(list[i], i, str(int(list[i])), color='white')
        # arrow用于设置标识箭头
        arrow = plt.annotate('Python平均月薪:'+str(df_ExpSalary['average'].mean().round(1))+'元', xy=(14197, 3.25), xytext=(20000, 4.05), color='white', fontsize=16,arrowprops=dict(facecolor='white', shrink=0.05))
        # 用于设置图例注释（df_ExpSalary['average'].value_counts().sum()为工作总数量
        ax.text(20000, 6.05, '月薪样本数:'+str(df_ExpSalary['average'].value_counts().sum())+'(个)', fontsize=16, color='white')
        # 设置轴刻度文字颜色为白色
        plt.tick_params(colors='white')
        # plt.savefig('WorkAnalysisByexp_salary.pdf', dpi=100)     #2018-4-2  17:50,其中dpi表示分辨率
        fig.set_size_inches(15.6, 10.8)
        plt.show()

    def VisaulAnalysisByedu_num(self):

        self.log.info(u'开始保存edu_num分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # print(df['ZDedu'].value_counts())
        edu = df['ZDedu'].replace(['其他', ['中技'], ['高中']], np.nan)
        # print(edu.value_counts())
        # 开始绘制图形
        plt.style.use('dark_background')
        fig = plt.figure(5, facecolor='black')                # #FFFFCC为淡黄色#808080为淡灰色
        ax1 = fig.add_subplot(2, 1, 1, facecolor='#808080', alpha=0.3)
        edu.value_counts().plot(kind='bar', rot=0, color='#7fc8ff')             # #7fc8ff为橙色
        plt.title(u'最低学历—职位数量分布图', fontsize=18, color='yellow')
        plt.xlabel(u'最低学历', fontsize=14, color='yellow')
        plt.ylabel(u'职位数量', fontsize=14, color='yellow')
        text1 = ax1.text(4.05, 2650, u'数据来源:智联招聘', fontsize=13, color='#66FF66')
        text2 = ax1.text(4.05, 2400, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax1.text(4.05, 2150, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax1.text(4.05, 1900, u'职位总数-共计:'+str(df['ZDedu'].value_counts().sum())+'(条)', fontsize=14, color='#66FF66')
        plt.tick_params(colors='white', labelsize=13)
        edulist = edu.value_counts().values
        for i in range(len(edulist)):
            ax1.text(i-0.1, edulist[i], int(edulist[i]), color='white')
        ax2 = fig.add_subplot(2, 1, 2)
        x2 = edu.value_counts().values
        labels = list(edu.value_counts().index)               #2018-3-24 18:33
        explode = ([0, 0.1, 0, 0, 0, 0])
        plt.pie(x2, explode=explode, labels=labels, autopct='%1.1f%%', textprops={'color': 'white'})  #autopct自动显示每个快的比例
        plt.axis('equal')
        # 设置饼状图的标签
        ax2.legend(shadow=True, fontsize=12, edgecolor='#7fc8ff')
        plt.tick_params(colors='white', labelsize=13)
        fig.set_size_inches(15.6, 10.8)
        # plt.savefig('WorkAnalysisByedu_num.png', dpi=100)
        plt.show()

    def VisualAnalysisBycity_salary(self):

        self.log.info(u'开始保存city_salary分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        dfcitysalary = pd.DataFrame(data={'city': df['add'], 'average': df['average']})
        # print(dfcitysalary.info())     # This is a test line
        pattern = re.compile('([0-9]+)')  # 对average做类型装换，将object转换为float
        listi = []
        for i in range(len(df.average)):
            item = df.average.iloc[i].strip()
            result = re.findall(pattern, item)
            try:
                if result:
                    listi.append(float(result[0]))
                elif (item.strip() == 'found no element' or item.strip() == '面议'):
                    listi.append(0)
                else:
                    print(item)
            except Exception as e:
                print(item, type(item), repr(e))
        dfcitysalary['average'] = listi
        # print(dfcitysalary.info())   # This is a test line
        # 按城市对平均月薪分类
        grouped = dfcitysalary['average'].groupby(dfcitysalary['city'])
        print(grouped.mean().round(1), grouped.count().sum())
        s = pd.Series(data={'平均工资': dfcitysalary['average'].mean()})
        result = grouped.mean().append(s)
        # sort_values()方法可以对值进行排序，默认按照升序，round（1）表示小数点后保留1位小数。
        print(result.sort_values(ascending=False).round(1))

        # 进行数据可视化绘图
        fig = plt.figure(6, facecolor='black')
        plt.style.use('dark_background')
        # facecolor为背景颜色，alpha为透明度
        ax = fig.add_subplot(1, 1, 1, facecolor='#808080', alpha=0.3)
        result.sort_values(ascending=False).round(1).plot(kind='bar', rot=30)  # 可选color='#ef9d9a'
        # 设置图标题，x和y轴标题
        plt.title(u'城市——平均月薪分布图', fontsize=18, color='yellow')  # 设置标题
        plt.xlabel(u'城市', fontsize=14, color='yellow')  # 设置X轴轴标题
        plt.ylabel(u'平均月薪', fontsize=14, color='yellow')  # 设置Y轴轴标题
        text1 = ax.text(30.05, 40000, u'数据来源:智联招聘', fontsize=13, color='#66FF66')
        text2 = ax.text(30.05, 38000, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax.text(30.05, 36000, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax.text(30.05, 34000, u'职位数量:共计6027(条)', fontsize=13, color='#66FF66')
        # 添加每一个城市的坐标值
        list_4 = result.sort_values(ascending=False).values
        for i in range(len(list_4)):
                ax.text(i - 0.5, list_4[i], int(list_4[i]), color='white')
        # 设置轴刻度文字颜色为白色
        plt.tick_params(colors='white')
        fig.set_size_inches(15.6, 10.8)
        # plt.savefig('WorkAnalysisBycity_salary.png')
        plt.show()           # 2018-4-3 12:30

    def VisualAnalysisByedu_salary(self):

        self.log.info(u'开始保存edu_salary分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号              #2018-4-3  15:30
        dfedu_salary = pd.DataFrame(data={'average': df['average'], 'edu': df['ZDedu'], 'exp': df['ZWexp']})
        # print(dfedu_salary.info())
        pattern = re.compile('([0-9]+)')  # 对average做类型装换，将object转换为float
        listi = []
        for i in range(len(df.average)):
            item = df.average.iloc[i].strip()
            result = re.findall(pattern, item)
            try:
                if result:
                    listi.append(float(result[0]))
                elif (item.strip() == 'found no element' or item.strip() == '面议'):
                    listi.append(0)
                else:
                    print(item)
            except Exception as e:
                print(item, type(item), repr(e))
        dfedu_salary['average'] = listi
        print(dfedu_salary.info())          # This is a test line
        # 按照工作经历和学历对平均工资进行分组
        grouped = dfedu_salary['average'].groupby([dfedu_salary['exp'], dfedu_salary['edu']])
        print(grouped.mean().round(1), grouped.count(), grouped.count().sum())              # This is a test line
        xlist = list(grouped.mean().round(1)['1-3年'].sort_values().index)
        print(grouped.mean().round(1)['1-3年'].reindex(xlist))
        print(xlist)
        # 开始绘制数据可视化图
        plt.style.use('dark_background')
        fig = plt.figure(7, facecolor='black')
        ax = fig.add_subplot(1, 1, 1, facecolor='#808080', alpha=0.3)
        plt.title(u'最低学历-工作经验-平均月薪分布图', fontsize=18, color='yellow')
        plt.xlabel(u'最低学历', fontsize=14, color='yellow')
        plt.ylabel(u'平均月薪', fontsize=14, color='yellow')
        plt.tick_params(colors='white')
        # ylist1~7分别是7种条形图的Y值列表
        ylist1 = grouped.mean().round(1)['无经验'].reindex(xlist).values
        ylist2 = grouped.mean().round(1)['1年以下'].reindex(xlist).values
        ylist3 = grouped.mean().round(1)['不限'].reindex(xlist).values
        ylist4 = grouped.mean().round(1)['1-3年'].reindex(xlist).values
        ylist5 = grouped.mean().round(1)['3-5年'].reindex(xlist).values
        ylist6 = grouped.mean().round(1)['5-10年'].reindex(xlist).values
        ylist7 = grouped.mean().round(1)['10年以上'].reindex(xlist).values

        # img1~img7分别表示7种条形图
        ind = np.arange(6)  # ind为x轴宽度，用numpy的array形式表示
        width = 0.1  # 条形图的宽度，要合理设置否则太宽会摆不下
        img1 = ax.bar(ind, ylist1, width)
        img2 = ax.bar(ind + width, ylist2, width)
        img3 = ax.bar(ind + width * 2, ylist3, width)
        img4 = ax.bar(ind + width * 3, ylist4, width)
        img5 = ax.bar(ind + width * 4, ylist5, width)
        img6 = ax.bar(ind + width * 5, ylist6, width)
        img7 = ax.bar(ind + width * 6, ylist7, width)

        # 设置X轴文本和位置调整
        ax.set_xticklabels(xlist)
        ax.set_xticks(ind + width / 2)

        # 设置文字说明
        text1 = ax.text(0.05, 52100, u'数据来源:智联招聘', fontsize=13, color='#66FF66')
        text2 = ax.text(0.05, 50200, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax.text(0.05, 48200, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax.text(0.05, 46200, u'职位数量:共计6027(条)', fontsize=13, color='#66FF66')

        # 设置图例
        ax.legend((img1[0], img2[0], img3[0], img4[0], img5[0], img6[0], img7[0]),
                   (u'无经验', u'1年以下', u'不限', u'1-3年', u'3-5年', u'5-10年', u'10年以上'), fontsize=13, facecolor='black')

        # 设置栅格
        plt.grid(True)
        fig.set_size_inches(15.6, 10.8)
        # plt.savefig('WorkAnalysisByedu_salary.png', dpi=100)
        plt.show()


if __name__ == '__main__':
    Analysis = JobAnalysisByZL('file:///D:/CODE/JobMessage/AnalysisByVisual/json/jobmessagebyzl.json',
                               'file:///D:/CODE/JobMessage/AnalysisByVisual/json/Resolve.json')
