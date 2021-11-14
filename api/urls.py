from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    # 下面是类视图名
    path('', views.IndexView.as_view(), name='index'),
    url(r'face', views.face, name='face'),
    url(r'zytest', views.zytest, name='zytest'),
    # url(r'face/hankvision', views.hankvision, name='hankvision'),
]
