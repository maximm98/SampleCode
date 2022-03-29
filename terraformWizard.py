import os
import sys
import json
import getpass
import time
from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats


def main(): #all we are doing in main is defining a basic menu.
    ans=True
    while ans:
        print("""
        1.Add a Node
        2.Change a Nodes state
        3.Add a New VIP
        4.Exit/Quit
        """)
        ans=input("What would you like to do? ")
        if ans=="1":
            addNode();
        elif ans=="2":
            nodeState();
        elif ans=="3":
            addVIP();
        elif ans=="4":
            print("\n Goodbye") 
            ans = None
        elif ans=="5":
            protoType() 
            ans = "5"
        else:
            print("\n Not Valid Choice Try again")



def addNode(): #addNode method - we are adding new nodes to the JSON based on user input.

    partitionName = input("Enter the partition name: ")
    nodeName = input("Enter the node name: ")
    ipAddress = input("Enter the IP Address: ")
    data = "pools"
    getData(data)
    poolName = input("Enter the pool name to attach the node to (You can copy pasta): ")
    nodeState = "user-up"
    with open('AddNode/vars.json', 'r+') as f: #with statement to safely open and close the json

        dic = json.load(f)
        f.seek(0) #need to seek to the begin to allow a clean overwrite.
        print(dic)
        # json.dump(dic, f)
        dic['nodes'].update({nodeName: {"Partition" : partitionName, "nodeName" : nodeName, "ipAddress" : ipAddress, "nodeState" : nodeState, "poolName" : poolName}})
        print(dic['nodes'])
        json.dump(dic, f, indent=1)
        f.truncate()

def nodeState():#nodeState method - Just updating the state of a node that is in the terraform tfstate...
    partitionName = input("Enter the partition name: ")
    nodeName = input("Enter the node name: ")
    ipAddress = input("Enter the IP Address: ")
    nodeState = input("Enter the node state you wish to place it in (user-up or user-down if you wish to disable it): ")
    poolName = input("Name of pool node is in: ")

    with open('AddNode/vars.json', 'r+') as f:

        dic = json.load(f)
        f.seek(0)

        dic['nodes'].update({nodeName: {"Partition" : partitionName, "nodeName" : nodeName, "ipAddress" : ipAddress, "nodeState" : nodeState, "poolName" : poolName}})
        json.dump(dic, f, indent=1)
        f.truncate()

def addVIP(): #addVIP method - full on building a VIP here. Gather a plethora of input needed for a clean turn-up.

    httpHostName = input("Enter the HTTP host name: ")
    nodeName = input("Enter the node name: ")
    nodeAdress = input("Enter the Back Side IP: ")
    vipAddress = input("Enter the Front Side IP: ")
    vipPartition = input("Enter the partition to add the VIP to (EX: Common): ")
    apiVersion = "/1_18_0"
    hostURL = input("Enter the URL being used for the VIP: ")
    data = "ssl"
    print(getData(data))
    client_ssl = input("Enter which SSL you would like (You can copy pasta): ")

    with open('VIP Demo/vars.json', 'r+') as f:

        dic = json.load(f)
        f.seek(0)
        print(dic)
        # json.dump(dic, f)

        dic['VIP'].update({hostURL: {"http-hostname" : httpHostName, "node-name" : nodeName, "node-address" : nodeAdress, "vip-address" : vipAddress, "vip-partition" : vipPartition, "api_version" : apiVersion, "host_header" : hostURL, "client_ssl" : client_ssl}})
        print(dic['VIP'])
        json.dump(dic, f, indent=1)
        f.truncate()

def getData(dataType): #getData method - We are going to making nested statements here to pull whatever data we want from the F5 DB...
    
    if dataType == "ssl":

        client_ssls = {}
        client_ssls = mgmt.tm.ltm.profile.client_ssls.get_collection()
        for ssl in client_ssls:
            print(ssl.name)
    elif dataType == "pools":

        pools = {}
        pools = mgmt.tm.ltm.pools.get_collection()
        for pool in pools:
            print(pool.name)

def protoType():
    nodes = {}
    rawNodes = {}
    test = 0
    nodes = mgmt.tm.ltm.nodes.get_collection()
    for node in nodes:
        while test == 0:

            stats = Stats(node.stats.load())
            print(stats.stat.serverside_curConns)
            time.sleep(5)

if __name__ == "__main__": 
    username = input("Enter your F5 username: ")
    pwd = getpass.getpass()
    mgmt = ManagementRoot(host, username, pwd)
    main();
