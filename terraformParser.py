import json
import os.path as path
from django.core import serializers
from F5 import models


def Node():

    with open('dataDump.json', 'w') as f:
        data = serializers.serialize("json", models.Node.objects.all())
        deser = json.loads(data)
        json.dump(deser, f, indent=1)

    relpath = path.abspath(path.join(__file__, "../../../.."))
    terraformpath = path.abspath(
        path.join(relpath, "Terraform/AddNode/vars.json"))
    print(terraformpath)
    with open(terraformpath, 'r+') as f, open('dataDump.json', 'r') as f2:

        dic = json.load(f)
        f.seek(0)

        dic2 = json.load(f2)
        f2.seek(0)

        keys = []
        for key in dic['nodes']:
            keys.append(key)
        for key in keys:
            dic['nodes'].pop(key, None)
            print(dic['nodes'])

        for key2 in dic2:
            nodeName = key2['pk']
            partitionName = key2['fields']['Partition']
            ipAddress = key2['fields']['ipAddress']
            nodeState = key2['fields']['nodeState']
            poolName = key2['fields']['poolName']
            dic['nodes'].update({nodeName: {"Partition": partitionName, "nodeName": nodeName,
                                            "ipAddress": ipAddress, "nodeState": nodeState, "poolName": poolName}})
        print(dic)
        json.dump(dic, f, indent=1)
        f.truncate()


def VIP():

    with open('dataDumpVIP.json', 'w') as f:
        data = serializers.serialize("json", models.VIP.objects.all())
        deser = json.loads(data)
        json.dump(deser, f, indent=1)

    relpath = path.abspath(path.join(__file__, "../../../.."))
    terraformpath = path.abspath(
        path.join(relpath, "Terraform/VIP Demo/vars.json"))
    print(terraformpath)
    with open(terraformpath, 'r+') as f, open('dataDumpVIP.json', 'r') as f2:

        dic = json.load(f)
        f.seek(0)

        dic2 = json.load(f2)
        f2.seek(0)
        print(dic2)
        keys = []
        for key in dic['VIP']:
            keys.append(key)
        for key in keys:
            dic['VIP'].pop(key, None)
            print(dic['VIP'])

        for key2 in dic2:
            hostURL = key2['pk']
            nodeName = key2['fields']['nodeName']
            nodeAddress = key2['fields']['nodeAddress']
            vipAddress = key2['fields']['vipAddress']
            vipPartition = key2['fields']['vipPartition']
            clientSSL = key2['fields']['clientSSL']
            httpHostname = key2['fields']['httpHostname']
            poolName = key2['fields']['poolName']
            apiVersion = "GET /index.html HTTP/1.0\r\n"
            dic['VIP'].update({hostURL: {"http-hostname": httpHostname, "node-name": nodeName, "node-address": nodeAddress, "vip-address": vipAddress,
                                         "vip-partition": vipPartition, "api_version": apiVersion, "host_header": hostURL, "client_ssl": clientSSL}})
        json.dump(dic, f, indent=1)
        f.truncate()
