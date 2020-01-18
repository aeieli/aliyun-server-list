#!/usr/bin/env python
#coding=utf-8

import json
import xlwt
import os

from datetime import datetime, timedelta

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcms.request.v20190101.DescribeMetricListRequest import DescribeMetricListRequest

region = {"hangzou": "cn-hangzhou", "beijing": "cn-beijing"}

AccessKeyId = 'keyid'
AccessSecret = 'secret'

seachData = {"cpu" : "CPUUtilization",
            "memory" : "memory_usedutilization",
            "system load" :"load_1m",
            "diskusage" : "diskusage_utilization",
            "net_in" : "networkin_rate",
            "net_out" : "networkout_rate"}


serverlist = {"i-<instname>": "server name",
        "i-<inst2name>": "server name"}

def GetMetric(inst, name, region, startTime, endTime, period):
    client = AcsClient(AccessKeyId, AccessSecret, region)

    request = DescribeMetricListRequest()
    request.set_accept_format('json')

    request.set_StartTime(startTime)
    request.set_EndTime(endTime)
    request.set_Dimensions("{\"instanceId\":\"" + inst +"\"}")
    request.set_Period(period)
    request.set_Namespace("acs_ecs_dashboard")
    request.set_MetricName(name)

    response = client.do_action_with_exception(request)
    # python2:  print(response)
    res = json.loads(response.decode('utf-8'), encoding="utf-8")

    if res["Success"] == True:
        return json.loads(res["Datapoints"])

def calResult(datas):
    average = 0
    max = 0
    min = 100
    # print(datas)
    if datas is None or len(datas) < 1:
        return 0,0,0
    for d in datas:
        average = (d["Average"] + average) / 2 if average > 0 else d["Average"]
        max = d["Maximum"] if d["Maximum"] > max else max
        min = d["Minimum"] if d["Minimum"] < min else min
# print(str(response, encoding='utf-8'))
    return average, max, min

def dicResult(inst, region, name, namekey, startTime, endTime, period, outs):
    inn = {}
    for k in inst.keys():
        # print(k, namekey, region, startTime, endTime, period)
        inn[k] = GetMetric(k, namekey, region, startTime, endTime, period)
    for k in inn.keys():
        ds = inn[k]
        average, max, min = calResult(ds)
        # print(k, name, average, max, min)
        if k in outs:
            outs[k][name] = {"Average":average,"Maximum":max, "Minimum": min}
        else :
            outs[k] = {name:{"Average":average,"Maximum":max, "Minimum": min}}
    return outs

def WriterToExcel(path, filename,inst, data):
    book = xlwt.Workbook()

    sh = book.add_sheet(filename)
    names = list(seachData.keys())
    for n in range(len(names)):
        sh.write(0, 1 + n*3, names[n])
        sh.write(1, 1+n*3, "max")
        sh.write(1, 2+n*3, "min")
        sh.write(1, 3+n*3, "avg")

    keys = list(data.keys())
    for i in range(len(keys)):
        key = keys[i]
        sh.write(i+2, 0, inst[key])
        print("data[i]", data[key])
        for n in range(len(names)):
            print("names[n]", names[n])
            sh.write(i+2, 1 + n * 3, data[key][names[n]]["Maximum"])
            sh.write(i+2, 2 + n * 3, data[key][names[n]]["Minimum"])
            sh.write(i+2, 3 + n * 3, data[key][names[n]]["Average"])
    book.save(path+"/"+filename+".xls")


if __name__ == '__main__':
    region = {"hangzou":"cn-hangzhou", "beijing":"cn-beijing"}
    outs = {}
    filepath = ""
    if filepath == "":
        filepath = os.path.dirname(os.path.abspath(__file__))

    now = datetime.now()
    start  = now - timedelta(7)

    end_time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_ttime = start.strftime("%Y-%m-%d %H:%M:%S")

    for name in seachData.keys():
        outs = dicResult(serverlist, region["beijing"], name, seachData[name], start_ttime, end_time,  "3600", outs)

    for i in outs.keys():
        for k in outs[i].keys():
             print(k, outs[i][k])

    WriterToExcel(filepath, now.strftime("%Y-%m-%d %H%M%S"), serverlist, outs)