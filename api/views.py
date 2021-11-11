from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
import json


class IndexView(generic.View):
    def get(self, request):
        # get请求
        return HttpResponse('这是get请求')

    def post(self, request):
        # post请求
        return HttpResponse('这是post请求')

    def put(self, request):
        # 其他请求
        return HttpResponse('这是其他请求')


def face(request):
    print("hello face")
    # p={"word":"data"}
    # 查看客户端发来的请求,前端的数据
    print("request.body={}".format(request.body))
    # 返回给客户端的数据
    result = "success"
    if request.method == "POST":
        print(request.POST)

    # user_input = json.loads(str(request.body, 'utf-8'))

    # print(user_input['a'])

    # output = int(user_input['a']) + int(user_input['b'])

    # return JsonResponse({"status": 200, "msg": "OK", "data": output})
    # return JsonResponse({"status": 200, "msg": "OK"})
    return JsonResponse(200, safe=False)


def hankvision(request):
    print("hello hankvision")
    # p={"word":"data"}
    # 查看客户端发来的请求,前端的数据
    print("request.body={}".format(request.body))
    # 返回给客户端的数据
    result = "success"
    if request.method == "POST":
        print(request.POST)

    # user_input = json.loads(str(request.body, 'utf-8'))

    # print(user_input['a'])

    # output = int(user_input['a']) + int(user_input['b'])

    # return JsonResponse({"status": 200, "msg": "OK", "data": output})
    # return JsonResponse({"status": 200, "msg": "OK"})
    return JsonResponse(200, safe=False)
