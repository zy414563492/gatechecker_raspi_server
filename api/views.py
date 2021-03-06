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
        # get??????
        return HttpResponse('??????get??????')

    def post(self, request):
        # post??????
        return HttpResponse('??????post??????')

    def put(self, request):
        # ????????????
        return HttpResponse('??????????????????')


def face(request):
    print("hello face")
    # p={"word":"data"}
    # ??????????????????????????????,???????????????
    print("request.body={}".format(request.body))
    # ???????????????????????????
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
    machine_date_aws_time = machine_date.strftime('%Y-%m-%dT%H:%M:%SZ')
    # print(machine_date)
    print("machine_date_aws_time: ", machine_date_aws_time)
    # print(machine_date.strftime('%Y-%m-%d %H:%M:%S'))  # ?????????????????????????????????????????????????????????????????????????????????????????????????????????

    paylodmsg = {}

    if connflag is True and temperature > 0:
        paylodmsg = {
            "id": rand_str(8),
            "__typename": 'Log',
            "_version": 1,
            "createdAt": machine_date_aws_time,
            "updatedAt": machine_date_aws_time,
            "_lastChangedAt": time,

            "log_id": rand_str(4),
            "temperature": temperature,
            "time": machine_date_aws_time,
            "is_blacklist": False,
            "deviceID": cid
        }

        paylodmsg_jstr = json.dumps(paylodmsg)

        mqttc.publish("ElectronicsInnovation", paylodmsg_jstr,
                      qos=1)  # topic: temperature # Publishing Temperature values
        print("msg sent: ElectronicsInnovation")  # Print sent temperature msg on console
        print(paylodmsg_jstr)

    else:
        print("waiting for connection...")


    print('#' * 50)
    print("cid: {}\ntime: {}\ntemperature: {}\nfacemask: {}".format(cid, time, temperature, facemask))
    print('#' * 50)
    # print(json.dumps(data))
    # print('#' * 50)

    # url = 'http://www.mechae.fun:8000/gatechecker/add_log'
    #
    # # headers????????????content-type????????????????????????json??????
    # headers = {'Content-Type': 'application/json'}
    #
    # # ???data????????????????????????json????????????json?????????
    # response_obj = requests.post(url=url, headers=headers, data=json.dumps(data))
    #
    # # ??????????????????error??????????????????
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
#     # ??????????????????????????????,???????????????
#     print("request.body={}".format(request.body))
#     # ???????????????????????????
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
#     # print(machine_date.strftime('%Y-%m-%d %H:%M:%S'))  # ?????????????????????????????????????????????????????????????????????????????????????????????????????????
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
#     # headers????????????content-type????????????????????????json??????
#     headers = {'Content-Type': 'application/json'}
#
#     # ???data????????????????????????json????????????json?????????
#     response_obj = requests.post(url=url, headers=headers, data=json.dumps(data))
#
#     # ??????????????????error??????????????????
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
#     # ??????????????????????????????,???????????????
#     print("request.body={}".format(request.body))
#     # ???????????????????????????
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
#     # headers????????????content-type????????????????????????json??????
#     headers = {'Content-Type': 'application/json'}
#
#     # ???data????????????????????????json????????????json?????????
#     r = requests.post(url=url, headers=headers, data=json.dumps(data))
#     print(r)
#
#     # return JsonResponse({"status": 200, "msg": "OK", "data": output})
#     # return JsonResponse({"status": 200, "msg": "OK"})
#     # return JsonResponse(200, safe=False)
#     return HttpResponse(json.dumps(data), content_type="application/json")
