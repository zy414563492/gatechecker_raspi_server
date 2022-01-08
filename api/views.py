from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import generic
import json
import requests
import random
import string
import datetime

# importing libraries
import paho.mqtt.client as paho
import os
import socket
import ssl
import random
import string
import json
from time import sleep
from random import uniform

connflag = False


def on_connect(client, userdata, flags, rc):  # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc))


def on_message(client, userdata, msg):  # Func for Sending msg
    print(msg.topic + " " + str(msg.payload))


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str


def getMAC(interface='eth0'):
    # Return the MAC address of the specified interface
    try:
        str = open('/sys/class/net/%s/address' % interface).read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]


def getEthName():
    # Get name of the Ethernet interface
    try:
        for root, dirs, files in os.walk('/sys/class/net'):
            for dir in dirs:
                if dir[:3] == 'enx' or dir[:3] == 'eth':
                    interface = dir
    except:
        interface = "None"
    return interface


# def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = paho.Client()  # mqttc object
mqttc.on_connect = on_connect  # assign on_connect func
mqttc.on_message = on_message  # assign on_message func
# mqttc.on_log = on_log

#### Change following parameters ####
awshost = "a2dh96ghlbuuat-ats.iot.ap-northeast-1.amazonaws.com"  # Endpoint
awsport = 8883  # Port no.
clientId = "My_RasPi"  # Thing_Name
thingName = "My_RasPi"  # Thing_Name
caPath = "/home/pi/AWS_IoT/My_RasPi/AmazonRootCA1.pem"  # Root_CA_Certificate_Name
certPath = "/home/pi/AWS_IoT/My_RasPi/My_RasPi-certificate.pem.crt"  # <Thing_Name>.cert.pem
keyPath = "/home/pi/AWS_IoT/My_RasPi/My_RasPi-private.pem.key"  # <Thing_Name>.private.key

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)  # pass parameters

mqttc.connect(awshost, awsport, keepalive=60)  # connect to aws server

mqttc.loop_start()  # Start the loop




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

    init_date = datetime.datetime.strptime('1970-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
    machine_time = datetime.timedelta(seconds=int(time))
    machine_date = init_date + machine_time
    # print(machine_date)
    # print(machine_date.strftime('%Y-%m-%d %H:%M:%S'))  # 这个也可以，适用于加减的时间带小数点却也像让其输出格式和输入一致的情况

    paylodmsg = {}

    if connflag is True:
        # ethName = getEthName()
        # ethMAC = getMAC(ethName)
        # macIdStr = ethMAC
        # randomNumber = uniform(20.0, 25.0)
        # random_string = get_random_string(8)

        # paylodmsg0 = "{"
        # paylodmsg1 = "\"log_id\": \""
        # paylodmsg2 = "\", \"temperature\":"
        # paylodmsg3 = ", \"time\": \""
        # paylodmsg4 = "\", \"is_blacklist\":"
        # paylodmsg5 = ", \"to_device\": \""
        # paylodmsg6 = "\"}"
        # paylodmsg = "{}{}{}{}{}{}{}{}{}{}{}{}".format(
        #     paylodmsg0, paylodmsg1, rand_str(4), paylodmsg2, temperature, paylodmsg3,
        #     str(machine_date), paylodmsg4, False, paylodmsg5, cid, paylodmsg6)

        paylodmsg_json = {
            "log_id": rand_str(4),
            "temperature": temperature,
            "time": str(machine_date),
            "is_blacklist": False,
            "to_device": cid
        }

        # paylodmsg = json.dumps(paylodmsg)
        # paylodmsg_json = json.loads(paylodmsg)
        mqttc.publish("ElectronicsInnovation", paylodmsg_json,
                      qos=1)  # topic: temperature # Publishing Temperature values
        print("msg sent: ElectronicsInnovation")  # Print sent temperature msg on console
        print(paylodmsg_json)

    else:
        print("waiting for connection...")


    print('#' * 50)
    print("cid: {}\ntime: {}\ntemperature: {}\nfacemask: {}".format(cid, time, temperature, facemask))
    print('#' * 50)
    # print(json.dumps(data))
    # print('#' * 50)

    # url = 'http://www.mechae.fun:8000/gatechecker/add_log'
    #
    # # headers中添加上content-type这个参数，指定为json格式
    # headers = {'Content-Type': 'application/json'}
    #
    # # 将data字典形式的参数用json包转换成json格式。
    # response_obj = requests.post(url=url, headers=headers, data=json.dumps(data))
    #
    # # 若服务器返回error，则报错返回
    # if response_obj.status_code != 200:
    #     print("error!")
    #     return JsonResponse({"status": response_obj.status_code, "msg": "error!"})
    #
    # response = json.dumps(response_obj.text)
    # print(response)
    # print('#' * 50)

    return HttpResponse(json.dumps(paylodmsg), content_type="application/json")
    # return JsonResponse({"status": 200, "msg": "OK", "data": response})



# def face(request):
#     print("hello face")
#     # p={"word":"data"}
#     # 查看客户端发来的请求,前端的数据
#     print("request.body={}".format(request.body))
#     # 返回给客户端的数据
#     result = "success"
#     if request.method == "POST":
#         print(request.POST)
#
#     body = json.loads(str(request.body, 'utf-8'))
#     cid = body.get("cid")
#     time = body.get("time")
#
#     # ignore heartbeat data
#     if time is None:
#         print("No face checked.")
#         return JsonResponse({})
#
#     result = body.get("result")
#     temperature = result.get("temperature")
#     facemask = result.get("facemask")
#
#     init_date = datetime.datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
#     machine_time = datetime.timedelta(seconds=int(time))
#     machine_date = init_date + machine_time
#     # print(machine_date)
#     # print(machine_date.strftime('%Y-%m-%d %H:%M:%S'))  # 这个也可以，适用于加减的时间带小数点却也像让其输出格式和输入一致的情况
#
#     data = {
#         "log_id": rand_str(4),
#         "temperature": temperature,
#         "time": str(machine_date),
#         "is_blacklist": False,
#         "to_device": cid
#     }
#
#     print('#' * 50)
#     print("cid: {}\ntime: {}\ntemperature: {}\nfacemask: {}".format(cid, time, temperature, facemask))
#     print('#' * 50)
#     # print(json.dumps(data))
#     # print('#' * 50)
#
#     url = 'http://www.mechae.fun:8000/gatechecker/add_log'
#
#     # headers中添加上content-type这个参数，指定为json格式
#     headers = {'Content-Type': 'application/json'}
#
#     # 将data字典形式的参数用json包转换成json格式。
#     response_obj = requests.post(url=url, headers=headers, data=json.dumps(data))
#
#     # 若服务器返回error，则报错返回
#     if response_obj.status_code != 200:
#         print("error!")
#         return JsonResponse({"status": response_obj.status_code, "msg": "error!"})
#
#     response = json.dumps(response_obj.text)
#     print(response)
#     print('#' * 50)
#
#     return HttpResponse(response, content_type="application/json")
#     # return JsonResponse({"status": 200, "msg": "OK", "data": response})


# def zytest(request):
#     print("hello test")
#     # p={"word":"data"}
#     # 查看客户端发来的请求,前端的数据
#     print("request.body={}".format(request.body))
#     # 返回给客户端的数据
#     result = "success"
#     if request.method == "POST":
#         print(request.POST)
#
#     # user_input = json.loads(str(request.body, 'utf-8'))
#
#     # print(user_input['a'])
#
#     data = {
#         "log_id": "L000",
#         "temperature": 36.3,
#         "time": "2021-10-01 22:24:47",
#         "is_blacklist": False,
#         "to_device": "D2"
#     }
#
#     url = 'http://www.mechae.fun:8000/gatechecker/add_log'
#
#     # headers中添加上content-type这个参数，指定为json格式
#     headers = {'Content-Type': 'application/json'}
#
#     # 将data字典形式的参数用json包转换成json格式。
#     r = requests.post(url=url, headers=headers, data=json.dumps(data))
#     print(r)
#
#     # return JsonResponse({"status": 200, "msg": "OK", "data": output})
#     # return JsonResponse({"status": 200, "msg": "OK"})
#     # return JsonResponse(200, safe=False)
#     return HttpResponse(json.dumps(data), content_type="application/json")
