# coding utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from .models import user
from .models import JobmessageByzl,JobmessageBy51
import pandas as pd
from django.db.models import Q
from .tasks import run_test_suit
from .tasks import spider_jobmessage
from Spider.JobSpiderByZL import GetJobMessagebyzl
from Spider.JobSpiderBy51job import GetJobMessageby51
from django.forms.models import model_to_dict

# Create your views here.
def index(request):
    return render(request, 'Jobsite/index.html')

def login(request):
    return render(request, 'Jobsite/index.html')

def login_action(request):

    if request.method == 'GET':
        page = request.GET.get('page')
        print(page)
        return render(request, 'Jobsite/index.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        try:
            user1 = user.objects.get(username=username)
            print(user1.username, user1.password, user1.pk)
            if user1.password == password:
                job_message_list = JobmessageByzl.objects.all()
                return render(request, 'Jobsite/main.html', {'job_message_list': job_message_list})
            else:
                return HttpResponse('<a href="http://127.0.0.1:8000/"><h1>用户密码错误请重新登录</h1></a>')
        except Exception as e:
            print(e)
            return HttpResponse('<a href="http://127.0.0.1:8000/register"><h1>用户不存在请注册</h1></a>')
    else:
        return render(request, 'Jobsite/index.html')

def register(request):
    return render(request, 'Jobsite/register.html')

def register_action(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        print('用 户 名：'+username)
        password = request.POST.get('password')
        print('密    码:'+password)
        repassword = request.POST.get('repassword')
        print('重复密码：'+repassword)
        try:
            user_info = user.objects.get(username=username)
            if user_info.username == username:
                message = '用户已存在，请重新注册'
                return render(request, '404error.html', {'message': message})
        except Exception as e:
            user.objects.create(username=username, password=password)
            message = '注册成功,请登录！'
            return render(request, 'registersuccess.html', {'message': message})
    elif request.mothod == 'GET':
        return render(request, 'Jobsite/register.html')
    else:
        return render(request, '404error.html', {'message': 'something gone be error！'})

def main_page_zl(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        job_message_list = JobmessageByzl.objects.all()
        if username:
            return render(request, 'Jobsite/mainbyzl.html', {'job_message_list': job_message_list, 'username': username})
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请先登录系统！'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        print('用户名：'+username)
        password = request.POST.get('password')
        print('密 码：'+password)
        try:
            user_info = user.objects.get(username=username)
            print(user_info.username, user_info.password, user_info.pk)
            if user_info.password == password:
                if username == 'admin':
                    message = '管理员登录成功！'
                    return render(request, 'adminlogin.html', {'message': message})
                else:
                    message = '用户登陆成功！'
                    return render(request, 'loginsuccess.html',{'message': message , 'username': user_info.username})
            else:
                message = '用户账户或密码错误，点击重新登录！'
                return render(request, '404error.html', {'message': message})
        except Exception as e:
            print(e)
            message = '用户不存在请注册，点击重新登录！'
            return render(request, '404error.html', {'message': message})
    else:
        return render(request, 'Jobsite/index.html')

def main_page_51(request):

    if request.method == 'GET':
        username =request.GET.get('username')
        job_message_list = JobmessageBy51.objects.all()
        if username:
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请先登录系统！'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        try:
            user1 = user.objects.get(username=username)
            print(user1.username, user1.password, user1.pk)
            if user1.password == password:
                job_message_list = JobmessageBy51.objects.all()
                return render(request, 'Jobsite/mainby51.html', {'job_message_list': job_message_list, 'username': user1.username})
            else:
                return HttpResponse('<a href="http://127.0.0.1:8000/"><h1>用户密码错误请重新登录</h1></a>')
        except Exception as e:
            print(e)
            return HttpResponse('<a href="http://127.0.0.1:8000/register"><h1>用户不存在请注册</h1></a>')
    else:
        return render(request, 'Jobsite/index.html')

def modify(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        oldpassword = request.POST.get('oldpassword')
        userupdate = user.objects.filter(username=username).update(password=password)
        message = '密码修改成功，请重新登录！'
        return render(request, 'loginfail.html', {'message': message})
    elif request.method == 'GET':
        username = request.GET.get('username')
        if username:
            return render(request, 'Jobsite/modify.html', {'username': username})
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请登录！'})
    else:
        return render(request, 'loginfail.html', {'message': 'something gone be wrong!' })

def Visual(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            return render(request, 'Jobsite/Visual.html', {'username': username})
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请先登录系统！'})

def messageby51(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        username = request.GET.get('username')
        message = JobmessageBy51.objects.get(id=id)
        print(message.GSname, message.ZWname)
        return render(request, 'Jobsite/message.html', {'message': message, 'username': username})
    elif request.method == 'POST':
        return render(request, 'Jobsite/message.html')
    else:
        message = '拒绝非法访问!'
        return render(request, '404error.html', {'message': message})

def messagebyzl(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print(id)
        username = request.GET.get('username')
        message = JobmessageByzl.objects.get(id=id)
        print(message.GSname, message.ZWname)
        return render(request, 'Jobsite/message.html', {'message': message, 'username': username})
    elif request.method == 'POST':
        return render(request, 'Jobsite/message.html')
    else:
        message = '拒绝非法访问'
        return render(request, '404error.html', {'message': message})

def user_info(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user1 = user.objects.get(username=username)
        return render(request, 'Jobsite/user_info.html', {'user': user1})
    elif request.method == 'GET':
        return render(request, 'Jobsite/user_info.html')
    else:
        return render(request, '404error.html')

def error(request):
    message = 'something gone be error!'
    return render(request, '404error.html', {'message': message})

def ZWaddbyzl(request):
    if request.method == 'GET':
        if request.GET.get('ZWadd') == 'BJ':
            job_message_list = JobmessageByzl.objects.filter(ZWadd='北京')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html', {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'SH':
            job_message_list = JobmessageByzl.objects.filter(ZWadd='上海')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'SZ':
            job_message_list = JobmessageByzl.objects.filter(ZWadd='深圳')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'GZ':
            job_message_list = JobmessageByzl.objects.filter(ZWadd='广州')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'NC':
            job_message_list = JobmessageByzl.objects.filter(ZWadd='南昌')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def ZWaddby51(request):
    if request.method == 'GET':
        if request.GET.get('ZWadd') == 'BJ':
            job_message_list = JobmessageBy51.objects.filter(ZWadd='北京')
            username = request.GET.get('username')
            # for message in job_message_list:
            #     print(message.pk, message.ZWadd)
            return render(request, 'Jobsite/mainby51.html', {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'SH':
            job_message_list = JobmessageBy51.objects.filter(ZWadd='上海')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'SZ':
            job_message_list = JobmessageBy51.objects.filter(ZWadd='深圳')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'GZ':
            job_message_list = JobmessageBy51.objects.filter(ZWadd='广州')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWadd') == 'NC':
            job_message_list = JobmessageBy51.objects.filter(ZWadd='南昌')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def ZDedubyzl(request):
    if request.method == 'GET':
        if request.GET.get('ZDedu') == 'BX':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='不限')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html', {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'ZZ':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='中专')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'DZ':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='大专')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'BK':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='本科')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'SS':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='硕士')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'BS':
            job_message_list = JobmessageByzl.objects.filter(ZDedu='博士')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',{'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def ZDeduby51(request):
    if request.method == 'GET':
        if request.GET.get('ZDedu') == 'BX':
            job_message_list = JobmessageBy51.objects.all()
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html', {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'ZZ':
            job_message_list = JobmessageBy51.objects.filter(ZDedu='中专')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'DZ':
            job_message_list = JobmessageBy51.objects.filter(ZDedu='大专')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'BK':
            job_message_list = JobmessageBy51.objects.filter(ZDedu='本科')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'SS':
            job_message_list = JobmessageBy51.objects.filter(ZDedu='硕士')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZDedu') == 'BS':
            job_message_list = JobmessageBy51.objects.filter(ZDedu='博士')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',{'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def Sortbyzl(request):
    if request.method == 'GET':
        if request.GET.get('sorttype') == 'ZWsalarySX':
            username = request.GET.get('username')
            job_list = JobmessageByzl.objects.all()
            df = pd.read_json('file:///D:/APP/Python编程/jobmessage/AnalysisByVisual/json/Resolve.json')
            print(df.info())
            return render(request, 'Jobsite/mainbyzl.html', {'job_message_list': job_list, 'username': username})
        elif request.GET.get('sorttype') == 'ZWsalaryJX':
            pass
        elif request.GET.get('sorttype') == 'ZWexpSX':
            pass
        elif request.GET.get('sorttype') == 'ZWexpJX':
            pass
    else:
        return render(request, '404error.html', {'message': '无权访问，请登录！'})

def Sortby51(request):
    pass

def ZWexpbyzl(request):
    if request.method == 'GET':
        if request.GET.get('ZWexp') == '1':
            job_message_list = JobmessageByzl.objects.filter(ZWexp='1年以下')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '1-3':
            job_message_list = JobmessageByzl.objects.filter(ZWexp='1-3年')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '3-5':
            job_message_list = JobmessageByzl.objects.filter(ZWexp='3-5年')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '5-10':
            job_message_list = JobmessageByzl.objects.filter(ZWexp='5-10年')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '10':
            job_message_list = JobmessageByzl.objects.filter(ZWexp='10年以上')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainbyzl.html',
                          {'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def ZWexpby51(request):
    if request.method == 'GET':
        if request.GET.get('ZWexp') == '1':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='1年经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '2':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='2年经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '3-4':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='3-4年经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '5-7':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='5-7年经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '8-9':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='8-9年经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        elif request.GET.get('ZWexp') == '10':
            job_message_list = JobmessageBy51.objects.filter(ZWexp='10年以上经验')
            username = request.GET.get('username')
            return render(request, 'Jobsite/mainby51.html',
                          {'job_message_list': job_message_list, 'username': username})
        else:
            message = 'something gone be error!'
            return render(request, '404error.html', {'message': message})
    else:
        message = 'something gone be error!'
        return render(request, '404error.html', {'message': message})

def spider(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        source = request.GET.get('source')
        num = request.GET.get('num')
        if username:
            if source == 'ZLJOB':
                if num == '1':
                    job_message_list = JobmessageByzl.objects.order_by('-pk')[:60]
                elif num == '2':
                    job_message_list = JobmessageByzl.objects.order_by('-pk')[:120]
                elif num == '3':
                    job_message_list = JobmessageByzl.objects.order_by('-pk')[:180]
                else:
                    job_message_list = JobmessageByzl.objects.order_by('-pk')[:60]
            elif source == '51JOB':
                if num == '1':
                    job_message_list = JobmessageBy51.objects.order_by('-pk')[:60]
                elif num == '2':
                    job_message_list = JobmessageBy51.objects.order_by('-pk')[:120]
                elif num == '3':
                    job_message_list = JobmessageBy51.objects.order_by('-pk')[:180]
                else:
                    job_message_list = JobmessageBy51.objects.order_by('-pk')[:60]
            else:
                job_message_list = JobmessageBy51.objects.order_by('-pk')[:60]
            return render(request, 'Jobsite/spider.html', {'username': username, 'job_message_list': job_message_list, 'source': source} )
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请先登录系统！'})
    elif request.method == 'POST':
        username = request.POST.get('username')
        spidertext = request.POST.get('spidertext')
        select = request.POST.get('select')
        spider_num = request.POST.get('spider_num')
        print(username, spidertext, select)
        if select == 'ZLJOB':
            print('celery before')
            result = spider_jobmessage.delay(select, spidertext, spider_num)
            print('celery after')
            job_message_list = JobmessageByzl.objects.all()
        elif select == '51JOB':
            result = spider_jobmessage.delay(select, spidertext, spider_num)
            job_message_list = JobmessageBy51.objects.all()
        else:
            return render(request, '404error.html', {'message': '请输入爬取关键字并选择数据来源！'})
        return render(request, 'spider_tip.html', {'message': '数据正在爬取中。。。','username': username, 'source': select, 'num': spider_num})
        # return render(request, 'Jobsite/spider.html', {'username': username, 'job_message_list': job_message_list})
    else:
        return render(request, '404error.html', {'message': 'something gone be wrong!'})

def searchbyzl(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        type = request.GET.get('type')
        keyword = request.GET.get('keyword')
        print('zl', username, type, keyword)
        if type == 'all':
            job_message_list = JobmessageByzl.objects.filter(
                Q(ZWinfo__icontains=keyword) | Q(ZWsalary__icontains=keyword) | Q(ZWadd__icontains=keyword) | Q(
                    ZDedu__icontains=keyword) | Q(ZWexp__icontains=keyword) | Q(date__icontains=keyword) | Q(ZWname__icontains=keyword))
        elif type == 'ZWname':
            job_message_list = JobmessageByzl.objects.filter(Q(ZWname__icontains=keyword)| Q(ZWinfo__icontains=keyword))
        else:
            job_message_list = JobmessageByzl.objects.all()
        return render(request, 'Jobsite/mainbyzl.html', {'username': username, 'job_message_list': job_message_list, 'type': type, 'keyword': keyword})
    elif request.method == 'POST':
        username = request.POST.get('username')
        keyword = request.POST.get('searchtext')
        select = request.POST.get('select')
        print(username, keyword, select, 'zl')
        if select == 'all':
            job_message_list = JobmessageByzl.objects.filter(Q(ZWname__icontains=keyword) | Q(ZWsalary__icontains=keyword)
                                                             | Q(ZWadd__icontains=keyword) | Q(ZDedu__icontains=keyword)
                                                             | Q(ZWexp__icontains=keyword) | Q(date__icontains=keyword)
                                                             | Q(ZWinfo__icontains=keyword))[:20]
        elif select == 'ZWname':
            job_message_list = JobmessageByzl.objects.filter(ZWname__icontains=keyword)[:20]
        elif select == 'ZWsalary':
            job_message_list = JobmessageByzl.objects.filter(ZWsalary__icontains=keyword)[:20]
        elif select == 'ZWadd':
            job_message_list = JobmessageByzl.objects.filter(ZWadd__icontains=keyword)[:20]
        elif select == 'ZDedu':
            job_message_list = JobmessageByzl.objects.filter(ZDedu__icontains=keyword)[:20]
        else:
            job_message_list = JobmessageByzl.objects.filter(ZWexp__icontains=keyword)[:20]
        return render(request, 'Jobsite/mainbyzl.html', {'username': username, 'job_message_list':job_message_list})
    else:
        message = 'something gone be worry!'
        return render(request, '404error.html', {'message' : message})

def searchby51(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        job_message_list = JobmessageBy51.objects.all()
        return render(request, 'Jobsite/mainby51.html', {'username': username, 'job_message_list': job_message_list})
    elif request.method == 'POST':
        username = request.POST.get('username')
        keyword = request.POST.get('searchtext')
        select = request.POST.get('select')
        print(username, keyword, select ,'51')
        if select == 'all':
            job_message_list = JobmessageBy51.objects.filter(Q(ZWname__icontains=keyword) | Q(ZWsalary__icontains=keyword) | Q(ZWadd__icontains=keyword) | Q(ZDedu__icontains=keyword) | Q(ZWexp__icontains=keyword) | Q(date__icontains=keyword))[:20]
        elif select == 'ZWname':
            job_message_list = JobmessageBy51.objects.filter(ZWname__icontains=keyword)[:20]
        elif select == 'ZWsalary':
            job_message_list = JobmessageBy51.objects.filter(ZWsalary__icontains=keyword)[:20]
        elif select == 'ZWadd':
            job_message_list = JobmessageBy51.objects.filter(ZWadd__icontains=keyword)[:20]
        elif select == 'date':
            job_message_list = JobmessageBy51.objects.filter(date__icontains=keyword)[:20]
        else:
            job_message_list = JobmessageBy51.objects.filter(ZWexp__icontains=keyword)[:20]
        return render(request, 'Jobsite/mainby51.html', {'username': username, 'job_message_list':job_message_list})
    else:
        message = 'something gone be worry!'
        return render(request, '404error.html', {'message' : message})

def search(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        source = request.GET.get('source')
        print('source is '+source)
        if username and source:
            return render(request, 'Jobsite/search.html', {'username': username, 'source': source})
        else:
            return render(request, 'loginfail.html', {'message': '当前未登录，请先登录系统！'})
    elif request.method == 'POST':
        keyword = request.POST.get('keyword')
        ZWname = request.POST.get('ZWname')
        ZWadd = request.POST.get('ZWadd')
        ZWsalary = request.POST.get('ZWsalary')
        ZWexp = request.POST.get('ZWexp')
        ZDedu = request.POST.get('ZDedu')
        date = request.POST.get('date')
        username = request.POST.get('username')
        source = request.POST.get('source')
        print(keyword, username, source)
        return render(request, 'search_tip.html', {'keyword': keyword, 'ZWname':ZWname, 'ZWadd': ZWadd,
                                                   'ZWsalary': ZWsalary, 'ZWexp': ZWexp, 'ZDedu': ZDedu,
                                                   'date': date, 'username': username,'source': source})
    else:
        message = 'something gone be worng!'
        return render(request, 'loginfail.html', {'message' : message})

def search_result(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        ZWname = request.GET.get('ZWname')
        ZWadd = request.GET.get('ZWadd')
        ZWsalary = request.GET.get('ZWsalary')
        ZWexp = request.GET.get('ZWexp')
        ZDedu = request.GET.get('ZDedu')
        date = request.GET.get('date')
        username = request.GET.get('username')
        source = request.GET.get('source')
        print(username, source, keyword, ZWname, ZWadd, ZWsalary, ZWexp, ZDedu,date)
        if source == '51':
            if ZWname=='all' and ZWadd=='all' and date=='all':
                print('test1')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(
                        ZWexp__icontains=ZWexp)
            elif ZWadd == 'all' and date == 'all' and ZWname != 'all':
                print('test2')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and date == 'all' and ZWadd != 'all':
                print('test3')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWadd__icontains=ZWadd).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and ZWadd == 'all' and date != 'all':
                print('test4')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and ZWadd != 'all' and date != 'all':
                print('test5')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWadd__icontains=ZWadd).filter(
                        ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname !='all' and ZWadd == 'all' and date != 'all':
                print('test6')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWname__icontains=ZWname).filter(
                        ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname !='all' and ZWadd != 'all' and date == 'all':
                print('test7')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWadd__icontains=ZWadd).filter(
                        ZWexp__icontains=ZWexp).filter(ZDedu__icontains=ZDedu).filter(ZWsalary__icontains=ZWsalary)
            else:
                print('test8')
                job_message_list = JobmessageBy51.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWadd__icontains=ZWadd).filter(
                        date__icontains=date).filter(ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(
                        ZWexp__icontains=ZWexp)
        elif source == 'zl':
            if ZWname=='all' and ZWadd=='all' and date=='all':
                print('test1')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(
                        ZWexp__icontains=ZWexp)
            elif ZWadd == 'all' and date == 'all' and ZWname != 'all':
                print('test2')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and date == 'all' and ZWadd != 'all':
                print('test3')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword)|Q(GSname__icontains=keyword)|Q(ZWnature__icontains=keyword)|Q(
                        ZWinfo__icontains=keyword)).filter(ZWadd__icontains=ZWadd).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and ZWadd == 'all' and date != 'all':
                print('test4')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWsalary__icontains=ZWsalary).filter(
                        ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname =='all' and ZWadd != 'all' and date != 'all':
                print('test5')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWadd__icontains=ZWadd).filter(
                        ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname !='all' and ZWadd == 'all' and date != 'all':
                print('test6')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(date__icontains=date).filter(ZWname__icontains=ZWname).filter(
                        ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(ZWexp__icontains=ZWexp)
            elif ZWname !='all' and ZWadd != 'all' and date == 'all':
                print('test7')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWadd__icontains=ZWadd).filter(
                        ZWexp__icontains=ZWexp).filter(ZDedu__icontains=ZDedu).filter(ZWsalary__icontains=ZWsalary)
            else:
                print('test8')
                job_message_list = JobmessageByzl.objects.filter(
                    Q(ZWname__icontains=keyword) | Q(GSname__icontains=keyword) | Q(ZWnature__icontains=keyword) | Q(
                        ZWinfo__icontains=keyword)).filter(ZWname__icontains=ZWname).filter(ZWadd__icontains=ZWadd).filter(
                        date__icontains=date).filter(ZWsalary__icontains=ZWsalary).filter(ZDedu__icontains=ZDedu).filter(
                        ZWexp__icontains=ZWexp)
        return render(request, 'Jobsite/search_result.html', {'job_message_list': job_message_list,'username': username, 'source': source})

def tasks(request):
    print('before run_test_suit')
    result = run_test_suit.delay('110')
    print('after run_test_suit')
    return HttpResponse("job is runing background~")
