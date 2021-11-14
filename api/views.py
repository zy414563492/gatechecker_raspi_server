from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
import json
import requests
import random
import string
import datetime


def rand_str(num):
    salt = ''.join(random.sample(string.ascii_letters + string.digits, num))
    return salt


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

    body = json.loads(str(request.body, 'utf-8'))
    cid = body.get("cid")
    time = body.get("time")

    # ignore heartbeat data
    if time is None:
        print("No face checked.")
        return JsonResponse({})

    result = body.get("result")
    temperature = result.get("temperature")
    facemask = result.get("facemask")

    init_date = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    machine_time = datetime.timedelta(seconds=int(time))
    machine_date = init_date + machine_time
    # print(machine_date)
    # print(machine_date.strftime('%Y-%m-%d %H:%M:%S'))  # 这个也可以，适用于加减的时间带小数点却也像让其输出格式和输入一致的情况

    data = {
        "log_id": rand_str(4),
        "temperature": temperature,
        "time": str(machine_date),
        "is_blacklist": False,
        "to_device": cid
    }

    print('#' * 50)
    print("cid: {}\ntime: {}\ntemperature: {}\nfacemask: {}".format(cid, time, temperature, facemask))
    print('#' * 50)
    # print(json.dumps(data))
    # print('#' * 50)

    url = 'http://www.mechae.fun:8000/gatechecker/add_log'

    # headers中添加上content-type这个参数，指定为json格式
    headers = {'Content-Type': 'application/json'}

    # 将data字典形式的参数用json包转换成json格式。
    response_obj = requests.post(url=url, headers=headers, data=json.dumps(data))

    # 若服务器返回error，则报错返回
    if response_obj.status_code != 200:
        print("error!")
        return JsonResponse({"status": response_obj.status_code, "msg": "error!"})

    response = json.dumps(response_obj.text)
    print(response)
    print('#' * 50)

    return HttpResponse(response, content_type="application/json")
    # return JsonResponse({"status": 200, "msg": "OK", "data": response})


def zytest(request):
    print("hello test")
    # p={"word":"data"}
    # 查看客户端发来的请求,前端的数据
    print("request.body={}".format(request.body))
    # 返回给客户端的数据
    result = "success"
    if request.method == "POST":
        print(request.POST)

    # user_input = json.loads(str(request.body, 'utf-8'))

    # print(user_input['a'])

    data = {
        "log_id": "L000",
        "temperature": 36.3,
        "time": "2021-10-01 22:24:47",
        "is_blacklist": False,
        "to_device": "D2"
    }

    url = 'http://www.mechae.fun:8000/gatechecker/add_log'

    # headers中添加上content-type这个参数，指定为json格式
    headers = {'Content-Type': 'application/json'}

    # 将data字典形式的参数用json包转换成json格式。
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(r)

    # return JsonResponse({"status": 200, "msg": "OK", "data": output})
    # return JsonResponse({"status": 200, "msg": "OK"})
    # return JsonResponse(200, safe=False)
    return HttpResponse(json.dumps(data), content_type="application/json")
