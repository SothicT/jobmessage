"""Mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from Jobsite import views

urlpatterns = [
    path('admin/', admin.site.urls),                                            # 用于访问admin管理界面
    path('login/', views.login, name="login"),                                  # 用于访问登录界面
    # path('login_action/', views.login_action, name="login_action"),           # 用于处理登录信息
    path('register/', views.register, name="register"),                         # 用于访问注册界面
    path('register_action/', views.register_action, name="register_action"),    # 用于处理注册信息
    path('mainbyzl/', views.main_page_zl, name="mainbyzl"),                     # 用于访问智联主界面
    path('mainby51/', views.main_page_51, name="mainby51"),                     # 用于访问前程无忧主界面
    path('modify/', views.modify, name="modify"),                               # 用于访问用户信息修改界面
    path('Visual/', views.Visual, name="VIsual"),                               # 用于访问可视化分析界面
    path('messageby51/', views.messageby51, name="message"),                    # 用于访问前程无忧职位详情
    path('messagebyzl/', views.messagebyzl, name="message"),                    # 用于访问智联职位详情
    path('userinfo/', views.user_info, name="user_info"),                       # 用于访问用户信息
    path('error/', views.error, name="404error"),                               # 用于访问404错误界面
    path('ZWaddbyzl/', views.ZWaddbyzl, name='ZWaddbyzl'),                      # 用于返回智联指定城市的相关工作
    path('ZWaddby51/', views.ZWaddby51, name='ZWaddby51'),                      # 用于返回前程无忧指定城市的相关工作
    path('ZWexpbyzl/', views.ZWexpbyzl, name='ZWexpbyzl'),                      # 用于返回智联指定工作经验的相关工作
    path('ZWexpby51/', views.ZWexpby51, name='ZWexpby51'),                      # 用于返回前程无忧指定工作经验的相关工作
    path('ZDedubyzl/', views.ZDedubyzl, name='ZDedubyzl'),                      # 用于返回智联指定学历的相关工作
    path('ZDeduby51/', views.ZDeduby51, name='ZDeduby51'),                      # 用于返回前程无忧指定学历的相关工作
    path('Sortby51/', views.Sortby51, name='Sortby51'),                         # 用于返回前程无忧指定排序的相关工作
    path('Sortbyzl/', views.Sortbyzl, name='Sortbyzl'),                         # 用于返回智联招聘指定排序的相关工作
    path('spider/', views.spider, name='spider'),                               # 用于爬取相关工作信息
    path('search/', views.search, name='search'),                               # 用于联合搜索相关职位信息（高级搜索）
    path('Searchinzl/', views.searchbyzl, name='searchbyzl'),                   # 用于搜索智联相关工作信息
    path('Searchin51/', views.searchby51, name='searchby51'),                   # 用于搜索前程无忧相关工作信息
    path('search_result/', views.search_result, name='search_result'),          # 用于display高级搜索的结果
    path('celery/', views.tasks),                                               # 用于测试celery多线程
    path('', views.index),                                                      # 用于访问index页面
]
