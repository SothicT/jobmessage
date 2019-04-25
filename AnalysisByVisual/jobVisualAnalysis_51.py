import re
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from MyLog import MyLog as mylog


class JobAnalysisByZL(object):
    def __init__(self, filename, ResolveFileName):
        self.setfilename(filename)
        self.setResolvefilename(ResolveFileName)
        self.df = pd.read_json(self.filename)
        self.log = mylog()
        self.ShowJsonInfo(ResolveFileName)                                # 2018-4-16 已测试
        # self.ResolveDataFrame()                                           # 2018-4-16 已测试
        # self.VisualAnalysisBywork_num()                                   # 2018-4-17 已测试
        # self.VisualAnalysisByexp_num()                                    # 2018-4-17 已测试
        # self.VisaulAnalysisByedu_num()                                    # 2018-4-17 已测试
        # self.VisualAnalysisByexp_salary()                                 # 2018-4-22 已测试
        # self.VisualAnalysisBycity_salary()                                # 2018-4-22 已测试
        # self.VisualAnalysisByedu_salary()                                 # 2018-4-17

    def setfilename(self, filename):

        self.filename = filename

    def getfilename(self):

        return self.filename

    def setResolvefilename(self, ResolveFileName):

        self.ResolveFileName = ResolveFileName

    def getResolveFileName(self):

        return self.ResolveFileName

    def ShowJsonInfo(self, filename):
        df = pd.read_json(filename)
        self.log.info(u'显示DataFrame相关信息：')
        print(df.info())
        print('#' * 100)
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
        df['bottom'] = df['top'] = df['average'] = df["ZWsalary"]
        df['num'] = df['ZWnum']
        df['add'] = df['ZWadd']
        # print(df['ZWsalary'].value_counts())
        pattern = re.compile(r'\d+')          # 按数字对字符串进行匹配
        q1 = q2 = q3 = q4 = q5 = q6 = q7 = 0
        # 处理工资最高值与最低值以及平均值
        # q1代表8-10千/月类型
        # q2代表10千元以下类型
        # q3代表形如1,5-2万/月以下类型
        # q4代表形如2万/月以下类型
        # q5代表15-20万/年类型
        # q6代表15万/年以下类型
        # q7代表特殊情况
        for i in range(len(df['ZWsalary'])):
            try:
                item = df['ZWsalary'].iloc[i].strip()
                if item == '面议':
                    continue
                print('数据处理中。。。', i, item)  # This is a test line
                result = re.findall(pattern, item)
            except Exception as e:
                print(e)
                continue
            if result:
                if re.search(r'月', df['ZWsalary'].iloc[i]):
                    if re.search(r'千', df['ZWsalary'].iloc[i]):
                        try:     # 刑如“8-10千/月”形式
                            df['bottom'].iloc[i], df['top'].iloc[i] = int(result[0])*1000, int(result[1])*1000
                            df['average'].iloc[i] = str((int(result[0]) + int(result[1])) * 500)
                            print('test,q1', i, q1, int(result[0])*1000, int(result[1])*1000, str((int(result[0]) + int(result[1])) * 500))
                            q1 += 1
                        except:  # 刑如“10千月以下“形式
                            df['bottom'].iloc[i] = df['top'].iloc[i] = int(result[0])*1000
                            df['average'].iloc[i] = str((int(result[0]) + int(result[0])) * 500)
                            q2 += 1
                            print('test,q2', i, q2, int(result[0])*1000, str((int(result[0]) + int(result[0])) * 500))
                    if re.search(r'万', df['ZWsalary'].iloc[i]):
                        try:     # 刑如“8-10万/月”形式
                            df['bottom'].iloc[i], df['top'].iloc[i] = int(result[0])*10000, int(result[1])*10000
                            df['average'].iloc[i] = str((int(result[0]) + int(result[1])) * 5000)
                            print('test,q3', i, q3, int(result[0]) * 10000, int(result[1]) * 10000,
                                  str((int(result[0]) + int(result[1])) * 5000))
                            q3 += 1
                        except:  # 刑如“10万月以下“形式
                            df['bottom'].iloc[i] = df['top'].iloc[i] = int(result[0])*10000
                            df['average'].iloc[i] = str((int(result[0]) + int(result[0])) * 5000)
                            print('test,q4', i, q4, int(result[0]) * 10000, int(result[0]) * 10000,
                                  str((int(result[0]) + int(result[0])) * 5000))
                            q4 += 1
                elif re.search(r'年', df['ZWsalary'].iloc[i]):
                    if re.search(r'万', df['ZWsalary'].iloc[i]):
                        try:  # 刑如“8-10万/年”形式
                            df['bottom'].iloc[i] = int(int(result[0]) * 10000 / 12)
                            df['top'].iloc[i] = int(int(result[1]) * 10000 / 12)
                            df['average'].iloc[i] = str(int((int(result[0]) + int(result[1])) * 10000 / 12))
                            print('test,q5', i, q5, int(int(result[0]) * 10000 / 12), int(int(result[1]) * 10000 / 12),
                                  str((int(result[0]) + int(result[1])) * 10000 / 12))
                            q5 += 1
                        except:  # 刑如“10万/年以下“形式
                            df['bottom'].iloc[i] = df['top'].iloc[i] = int(result[0]) * 10000 / 12
                            df['average'].iloc[i] = str(int((int(result[0]) + int(result[0])) * 5000))
                            print('test,q6', i, q6,  df['bottom'].iloc[i], df['top'].iloc[i], df['average'].iloc[i])
                            q6 += 1
            else:
                df['bottom'].iloc[i] = df['top'].iloc[i] = df['average'] = item
                q7 += 1

        # 处理职位数量
        for i in range(len(df['ZWnum'])):
            try:
                item = df['ZWnum'].iloc[i].strip()
                result = re.findall(pattern, item)
                if result:
                    print('数据处理中。。。', i, result[0], item.strip())    # This is a test line
                    df['num'].iloc[i] = result[0]
            except Exception as e:
                continue
        df_city = df['ZWadd'].copy()
        pattern2 = re.compile('(.*?)(\-)')      # 对工作地点进行处理
        for i in range(len(df['ZWadd'])):       # 处理工作地点
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
        print(df[['ZWnum', 'num']].head(5))  # This is a test line
        print('#' * 150)
        print('#' * 150)
        print(df[['ZWadd', 'add']].head(10))                               # This is a  test line
        print('#' * 150)
        print('#' * 150)
        print(q1, q2, q3, q4, q5, q6, q7, q1 + q2 + q3 + q4 + q5 + q6 + q7)
        print(self.df[['ZWsalary', 'bottom', 'top', 'average']].head(20))  # This is a test line
        print('#' * 150)
        print(df['add'].value_counts(), df['add'].value_counts().count())   # This is a  test line
        self.df = df
        self.df.to_json('Resolve_51.json')
        self.log.info(u'json数据清洗完毕')
        self.log.info(u'数据已写入Reslove_51.json中')

    def VisualAnalysisBywork_num(self):

        self.log.info(u'开始保存work_num分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        # print(df['add'].value_counts(), "\ntotally line：", df['add'].value_counts().count())              #2018-3-21 18:26
        list_1 = df['add'].value_counts()
        # 开始绘制数据可视化图形
        plt.style.use('dark_background')
        fig = plt.figure(1, facecolor='black')  # 设置背景画布
        ax1 = fig.add_subplot(2, 1, 1, facecolor='#808080', alpha=0.3)  # 在视图中绘制子图，背景为灰色
        plt.tick_params(colors='white')
        df['add'].value_counts().plot(kind='bar', rot=0, color='cyan')
        # 设置标题和x轴与y轴
        plt.title('城市——职位数分布图', fontsize=20, color='yellow')  # 设置标题
        plt.xlabel('城市', fontsize=14, color='yellow')  # 设置X轴轴标题
        plt.ylabel('职位数', fontsize=14, color='yellow')  # 设置Y轴轴标题
        # 设置说明，位置在图的右上角
        text1 = ax1.text(23.05, 3000, u'数据来源:前程无忧', fontsize=13, color='#66FF66')
        text2 = ax1.text(23.05, 2800, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax1.text(23.05, 2600, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax1.text(23.05, 2400, u'职位数量:共计15930(条)', fontsize=13, color='#66FF66')
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
        labels = label_list + [''] * 146            #labels数量必须是城市数量的和
        # print(labels)
        explode = tuple([0.1] + [0] * 153)          #explode为tuple类型的值
        plt.pie(x, explode=explode, labels=labels, textprops={'color': 'white'})
        ax2.legend((u'上海', u'北京', u'深圳', u'广州', u'杭州', u'成都', u'南京', u'武汉'), fontsize=13, facecolor='black')
        plt.axis('equal')
        fig.set_size_inches(15.6, 10.8)
        plt.show()

    def VisualAnalysisByexp_num(self):

        self.log.info(u'开始保存exp_num分析结果')
        filename = self.getResolveFileName()
        df = pd.read_json(filename)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        print(df['ZWexp'].value_counts(), df['ZWexp'].value_counts().count())   #This is a test line
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
        ax1.text(5.05, 4500, u'数据来源:前程无忧', fontsize=13, color='#66FF66')
        ax1.text(5.05, 4100, u'职位关键词：Python', fontsize=13, color='#66FF66')
        ax1.text(5.05, 3700, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        ax1.text(5.05, 3300, u'职位数量:共计15930(条)', fontsize=13, color='#66FF66')
        explist = exp.value_counts().values
        for i in range(len(explist)):
            ax1.text(i-0.1, explist[i], int(explist[i]), color='white')
        # 设置子图2，是位于子图1下面的饼状图
        ax2 = fig.add_subplot(2, 1, 2)
        # x是数值列表，pie图的比例根据数值占整体的比例而划分
        x2 = exp.value_counts().values
        labels = list(exp.value_counts().index[:5])+['']*2
        explode = tuple([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])
        plt.pie(x2, explode=explode, labels=labels, autopct='%1.1f%%', textprops={'color': 'w'})  #autopct是自动显示比例
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
        df_ExpSalary = pd.DataFrame(data={'exp': df['ZWexp'], 'average': df['average']})
        pattern = re.compile('([0-9]+)')                #对average做类型装换，将str转换为float
        print('#'*150)
        print(df['average'].value_counts(), df_ExpSalary['average'].count(), len(df.average), len(df_ExpSalary['average']))
        print('#' * 150)
        listi = []
        for i in range(len(df.average)):
            try:
                item = df.average.iloc[i]
                print('处理前', i, item)
                result = re.findall(pattern, item)
                if result:
                    listi.append(float(result[0]))
                    print('处理后', i, result[0])
                else:
                    print('none处理：', i, item)
                    listi.append(np.nan)
            except Exception as e:
                print('异常：', item, i, type(item), repr(e))
                listi.append(np.nan)
        print(len(listi), len(df_ExpSalary['average']))
        df_ExpSalary['average'] = listi
        print(type(df_ExpSalary['average']), df_ExpSalary['average'].value_counts().sum(), df_ExpSalary['average'].mean())     #This is a test line
        grouped = df_ExpSalary['average'].groupby(df_ExpSalary['exp'])
        # print(grouped.mean())   #This is a test line,用于显示工作经验和平均工资的关系
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
        arrow = plt.annotate('Python平均月薪:'+str(df_ExpSalary['average'].mean().round(1))+'元', xy=(25000, 3.25), xytext=(30000, 4.05), color='white', fontsize=16,arrowprops=dict(facecolor='white', shrink=0.05))
        # 用于设置图例注释（df_ExpSalary['average'].value_counts().sum()为工作总数量
        ax.text(32000, 6.05, '月薪样本数:'+str(df_ExpSalary['average'].value_counts().sum())+'(个)', fontsize=16, color='white')
        ax.text(32000, 5.55, '数据来源：前程无忧', fontsize=16,color='white')
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
        edu = df['ZDedu'].replace([['初中及以下'], ['中技']], np.nan)
        print(edu.value_counts())
        # 开始绘制图形
        plt.style.use('dark_background')
        fig = plt.figure(5, facecolor='black')                # #FFFFCC为淡黄色#808080为淡灰色
        ax1 = fig.add_subplot(2, 1, 1, facecolor='#808080', alpha=0.3)
        edu.value_counts().plot(kind='bar', rot=0, color='#7fc8ff')             # #7fc8ff为橙色
        plt.title(u'最低学历—职位数量分布图', fontsize=18, color='yellow')
        plt.xlabel(u'最低学历', fontsize=14, color='yellow')
        plt.ylabel(u'职位数量', fontsize=14, color='yellow')
        text1 = ax1.text(4.05, 9800, u'数据来源:前程无忧', fontsize=13, color='#66FF66')
        text2 = ax1.text(4.05, 9000, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax1.text(4.05, 8200, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax1.text(4.05, 7400, u'职位总数-共计:'+str(df['ZDedu'].value_counts().sum())+'(条)', fontsize=14, color='#66FF66')
        plt.tick_params(colors='white', labelsize=13)
        edulist = edu.value_counts().values
        for i in range(len(edulist)):
            ax1.text(i-0.1, edulist[i], int(edulist[i]), color='white')
        ax2 = fig.add_subplot(2, 1, 2)
        x2 = edu.value_counts().values
        labels = list(edu.value_counts().index)
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
            try:
                item = df.average.iloc[i]
                print('处理前', i, item)
                result = re.findall(pattern, item)
                if result:
                    listi.append(float(result[0]))
                    print('处理后', i, result[0])
                else:
                    print('none处理：', i, item)
                    listi.append(np.nan)
            except Exception as e:
                print('异常：', item, i, type(item), repr(e))
                listi.append(np.nan)
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
        ax.text(120.05, 35000, u'数据来源:前程无忧', fontsize=13, color='#66FF66')
        ax.text(120.05, 33000, u'职位关键词：Python', fontsize=13, color='#66FF66')
        ax.text(120.05, 31000, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        ax.text(120.05, 29000, u'职位数量:共计6027(条)', fontsize=13, color='#66FF66')
        # 添加每一个城市的坐标值
        list_4 = result.sort_values(ascending=False).values
        for i in range(len(list_4)):
            try:
                ax.text(i - 0.5, list_4[i], int(list_4[i]), color='white')
            except:
                continue
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
            try:
                item = df.average.iloc[i]
                print('处理前', i, item)
                result = re.findall(pattern, item)
                if result:
                    listi.append(float(result[0]))
                    print('处理后', i, result[0])
                else:
                    print('none处理：', i, item)
                    listi.append(0)
            except Exception as e:
                print('异常：', item, i, type(item), repr(e))
                listi.append(0)
        dfedu_salary['average'] = listi
        print(dfedu_salary.info())          # This is a test line
        # 按照工作经历和学历对平均工资进行分组
        grouped = dfedu_salary['average'].groupby([dfedu_salary['exp'], dfedu_salary['edu']])
        print(grouped.mean().round(1), grouped.count(), grouped.count().sum())              # This is a test line
        xlist = list(grouped.mean().round(1)['无工作经验'].sort_values().index)
        print(grouped.mean().round(1)['无工作经验'].reindex(xlist))
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
        ylist1 = grouped.mean().round(1)['无工作经验'].reindex(xlist).values
        ylist2 = grouped.mean().round(1)['1年经验'].reindex(xlist).values
        ylist3 = grouped.mean().round(1)['2年经验'].reindex(xlist).values
        ylist4 = grouped.mean().round(1)['3-4年经验'].reindex(xlist).values
        ylist5 = grouped.mean().round(1)['5-7年经验'].reindex(xlist).values
        ylist6 = grouped.mean().round(1)['8-9年经验'].reindex(xlist).values
        ylist7 = grouped.mean().round(1)['10年以上经验'].reindex(xlist).values
        # img1~img7分别表示7种条形图
        ind = np.arange(8)  # ind为x轴宽度，用numpy的array形式表示
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
        text1 = ax.text(0.05, 69000, u'数据来源:前程无忧', fontsize=13, color='#66FF66')
        text2 = ax.text(0.05, 66000, u'职位关键词：Python', fontsize=13, color='#66FF66')
        text3 = ax.text(0.05, 63000, u'工作城市:全国范围', fontsize=13, color='#66FF66')
        text4 = ax.text(0.05, 60000, u'职位数量:共计15930(条)', fontsize=13, color='#66FF66')
        # 设置图例
        ax.legend((img1[0], img2[0], img3[0], img4[0], img5[0], img6[0], img7[0]),
                   (u'无经验', u'1年', u'2年', u'3-4年', u'5-7年', u'8-9年', u'十年以上'), fontsize=13, facecolor='black')
        # 设置栅格
        plt.grid(True)
        fig.set_size_inches(15.6, 10.8)
        # plt.savefig('WorkAnalysisByedu_salary.png', dpi=100)
        plt.show()


if __name__ == '__main__':
    Analysis = JobAnalysisByZL("file:///D:/APP/Python编程/jobmessage/AnalysisByVisual/json/jobsite_jobmessageby51.json",
                               "file:///D:/APP/Python编程/jobmessage/AnalysisByVisual/Resolve_51.json")
