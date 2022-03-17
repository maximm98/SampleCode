from bigrest.bigip import BIGIP
from django import db
import psycopg2
from credlib import sys_db
from credlib import sys_f5
import time
import smtplib
import ssl
import sys
# This file is used by the linux service daemon: node-connections.service
# Connect to the BIG-IP iControl API Bridge.
device = BIGIP(sys_f5.hostname, sys_f5.username, sys_f5.password)
conn = psycopg2.connect(database=sys_db.database, user=sys_db.username,
                        password=sys_db.password, host=sys_db.hostname, port=sys_db.port)


class VIPs:
    def __init__(self, host_header, nodeName, nodeAddress, vipAddress):
        self.host_header = host_header
        self.nodeName = nodeName
        self.nodeAddress = nodeAddress
        self.vipAddress = vipAddress


class Nodes:
    def __init__(self, nodeName, partition, ipAddress, nodeState, poolName, vipName, fqn):
        self.nodeName = nodeName
        self.partition = partition
        self.ipAddress = ipAddress
        self.nodeState = nodeState
        self.poolName = poolName
        self.vipName = vipName
        self.fqn = fqn


class NodeConnections:
    def __init__(self, nodeName, ipAddress, currentConnections, pool):
        self.nodeName = nodeName
        self.ipAddress = ipAddress
        self.currentConnections = currentConnections
        self.pool = pool


class PoolList:
    def __init__(self, poolName):
        self.poolName = poolName


def getNodeStats():

    vips = device.load("/mgmt/tm/ltm/virtual/")
    vipName = None
    vipPools = []
    pools = None
    poolName = None
    nodeList = []
    if vipName is None and vipPools == [] and pools is None and poolName is None and nodeList == []:
        for vip in vips:
            vipPools = []
            if 'pool' in vip.properties:
                vipName = vip.properties['name']
                if isinstance(vip.properties['pool'], list):
                    for pool in vip.properties['pool']:
                        vipPools.append(PoolList(pool))
                else:
                    vipPools.append(
                        PoolList(vip.properties['pool'].replace('/', '~')))
                for pool in vipPools:
                    nodes = device.load(
                        f'/mgmt/tm/ltm/pool/{pool.poolName}/members')
                    connectionNodes = device.show(
                        f'/mgmt/tm/ltm/pool/{pool.poolName}/members')
                    zip_nodes = zip(nodes, connectionNodes)
                    for node, connection in zip_nodes:
                        nodeList.append(NodeConnections(node.properties['name'],
                                                        node.properties['address'], connection.properties['serverside.curConns']['value'], vip.properties['pool']))

    return nodeList


def updateConnections():
    try:
        connections = getNodeStats()

        cursor = conn.cursor()

        sql = '''SELECT * from vips_node'''
        cursor.execute(sql)
        for node in connections:
            updateTable = f'''UPDATE VIPS_NODE SET "currentconnections" = ('{node.currentConnections}') WHERE "poolname" = ('{node.pool}') AND "nodename" = ('{node.nodeName}')'''
            cursor.execute(updateTable)
            conn.commit()
    except Exception as error:
        print(error)
        conn.close()


def getVIPNodePool():
    try:
        vips = device.load("/mgmt/tm/ltm/virtual/")
        vipName = None
        vipPools = []
        pools = None
        poolName = None
        nodeList = []
        otherVIPPoolsList = []
        nodeState = None
        if vipName is None and vipPools == [] and pools is None and poolName is None and nodeList == []:
            for vip in vips:
                vipPools = []
                # if 'pool' in vip.properties:
                if 'pool' in vip.properties and "redir_vs" not in vip.properties['name']:
                    vipName = vip.properties['name']
                    if isinstance(vip.properties['pool'], list):
                        for pool in vip.properties['pool']:
                            vipPools.append(PoolList(pool))
                    else:
                        vipPools.append(
                            PoolList(vip.properties['pool'].replace('/', '~')))
                        otherVIPPoolsList.append(
                            PoolList(vip.properties['pool'].replace('/', '~')))

                    for pool in vipPools:
                        nodes = device.load(
                            f'/mgmt/tm/ltm/pool/{pool.poolName}/members')  # Get all other pools and pool members not strictly associated to VIP with this endpoint.
                        for node in nodes:
                            if(node.properties['session'] == 'user-disabled' or node.properties['session'] == 'user-down' or node.properties['state'] == 'down' or node.properties['state'] == 'user-down'):
                                node.properties['state'] = 'down'
                            elif(node.properties['session'] == 'monitor-enabled' or node.properties['session'] == 'user-enabled' or node.properties['state'] == 'up' or node.properties['state'] == 'user-up'):
                                node.properties['state'] = 'up'
                            else:
                                node.properties['state'] = node.properties['state']
                            nodeList.append(Nodes(node.properties['name'], node.properties['partition'],
                                                  node.properties['address'], node.properties['state'], vip.properties['pool'], vipName, f"={vipName}{vip.properties['pool']}={node.properties['name']}"))
            allPools = device.load("/mgmt/tm/ltm/pool")
            allPoolsList = []
            allVipsPoolList = []

            for pool in otherVIPPoolsList:
                allVipsPoolList.append(pool.poolName)
            for pool in allPools:
                if 'pool' in vip.properties:
                    allPoolsList.append(
                        PoolList(pool.properties['fullPath'].replace('/', '~')))
            for pool in allPoolsList:
                if(pool.poolName not in allVipsPoolList):
                    nodes = device.load(
                        f'/mgmt/tm/ltm/pool/{pool.poolName}/members')
                    for node in nodes:
                        if(node.properties['session'] == 'user-disabled' or node.properties['session'] == 'user-down' or node.properties['state'] == 'down' or node.properties['state'] == 'user-down'):
                            node.properties['state'] = 'down'
                        elif(node.properties['session'] == 'monitor-enabled' or node.properties['session'] == 'user-enabled' or node.properties['state'] == 'up' or node.properties['state'] == 'user-up'):
                            node.properties['state'] = 'up'
                        else:
                            node.properties['state'] = node.properties['state']
                        nodeList.append(Nodes(node.properties['name'], node.properties['partition'],
                                              node.properties['address'], node.properties['state'], pool.poolName, "NO_STATIC_VIP", f"=NO_STATIC_VIP{pool.poolName}={node.properties['name']}"))

        return nodeList
    except Exception as error:
        print(error)


def nodeStateAlert():
    try:
        """
        The method, getVIPNodePool() grabs every piece of VIP data for every partition, therefore it eats up a lot of resources on the F5.
        To reduce resource usage, we are going to combine the code for alerting as well as the code for 
        updating the PostGreSQL table to eliminate redundant API calls.
        """

        port = 25  # For starttls
        server = smtplib.SMTP(smtp_server, port)

        nodeList = getVIPNodePool()[:]
        cursor = conn.cursor()

        sql = '''SELECT * from vips_node'''
        cursor.execute(sql)

        rows = cursor.fetchall()
        dbList = [[*row] for row in rows]

        for row in dbList:
            for node in nodeList:
                if(node.nodeName == row[0] and node.poolName == row[4] and node.nodeState != row[3] and node.nodeState != "up" and row[8] == False):
                    message = f'Subject: F5 Node Down Alert in VIP {node.vipName} \n\n An F5 node has gone down in {node.poolName}.\n\n Node Name: {node.nodeName}\n Partition: {node.partition}\n Ip Address: {node.ipAddress}\n Pool: {node.poolName}\n VIP: {node.vipName}'
                    server.sendmail(sender_email, receiver_email, message)
                    print("Email Sent")
                    updateTable = f'''UPDATE VIPS_NODE SET "isAlerted" = ('True'), "nodestate" = ('{node.nodeState}') WHERE "fqn" = ('{row[6]}')'''
                    row[8] = True
                    row[3] = 'down'
                    cursor.execute(updateTable)
                    conn.commit()
                    print(row)
                elif(node.nodeName == row[0] and node.poolName == row[4] and node.nodeState != row[3] and node.nodeState == "up" and row[8] == True):
                    message = f'Subject: F5 Node Recovery Alert in VIP {node.vipName} \n\n An F5 node has recovered in {node.poolName}.\n\n Node Name: {node.nodeName}\n Partition: {node.partition}\n Ip Address: {node.ipAddress}\n Pool: {node.poolName}\n VIP: {node.vipName}'
                    server.sendmail(sender_email, receiver_email, message)
                    updateTable = f'''UPDATE VIPS_NODE SET "isAlerted" = ('False'), "nodestate" = ('{node.nodeState}') WHERE "fqn" = ('{row[6]}')'''
                    row[8] = False
                    row[3] = 'up'
                    cursor.execute(updateTable)
                    conn.commit()
                    print(row)

        server.close()

    except Exception as error:
        print(error)
        conn.close()


def main():
    nodeStateAlert()
    time.sleep(15)
    updateConnections()


if __name__ == "__main__":
    while True:
        print("Checking Node Connections...")
        main()
        time.sleep(60)
