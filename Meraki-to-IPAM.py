import csv
from datetime import datetime
import os
import meraki
from orionsdk import SwisClient
#In this script, we are exchanging and/or manipulating data against three different datastores. Utilizing a variation of data types. Data mutation is prevalent to assist in translations across stores.
def main():
    dashboard = meraki.DashboardAPI()
    # Get SOHO ORG number
    organizations = [omit]
    #Instantiate each list being used for data exchange in Meraki realm.
    mxNames = list()
    mxModel = list()
    mxSerial = list()
# Iterate through SOHO ORG
    for org in organizations:
        print(f'\nAnalyzing organization SOHO:')! 

        # Get list of networks in SOHO organization
        try:
            networks = dashboard.organizations.getOrganizationNetworks(org) #instantiate and ref. nets in SOHO org
        except meraki.APIError as e: #API except called from mod.
            print(f'Meraki API error: {e}')
            print(f'status code = {e.status}') 
            print(f'reason = {e.reason}')
            print(f'error = {e.message}')
            continue
        except Exception as e: #any sys. except declared or py env. excepts' declared.
            print(f'some other error: {e}')
            continue
            # Iterate through networks
        total = len(networks)
        counter = 1
        print(
            f'  - iterating through {total} networks in organization {org}') #f-string FTW
        for net in networks:
            try:
                print(net['id'])
                StoS = dashboard.networks.getNetworkDevices(
                net['id'])
                if not StoS:
                    print(f'Network does not have any devices: {net} ')
                elif StoS[0]['model'] == "MX67":
                    mxNames.append(StoS[0]['url'])
                    mxModel.append(StoS[0]['model'])
                    mxSerial.append(StoS[0]['serial'])
                    print("TRUE!!")
                elif StoS[0]['model'] == "MX68":
                    mxNames.append(StoS[0]['url'])
                    mxModel.append(StoS[0]['model'])
                    mxSerial.append(StoS[0]['serial'])
                    print("TRUE!!")

                elif StoS[0]['model'] == "MX67C-NA":
                    mxNames.append(StoS[0]['url'])
                    mxModel.append(StoS[0]['model'])
                    mxSerial.append(StoS[0]['serial'])
                    print("TRUE!!")
                elif StoS[0]['model'] == "MX68CW-NA":
                    mxNames.append(StoS[0]['url'])
                    mxModel.append(StoS[0]['model'])
                    mxSerial.append(StoS[0]['serial'])
                    print("TRUE!!")
                elif StoS[0]['model'] == "Z3C" or StoS[0]['model'] == "Z3-C" or StoS[0]['model'] == "Z3C-NA":
                    mxNames.append(StoS[0]['url'])
                    mxModel.append(StoS[0]['model'])
                    mxSerial.append(StoS[0]['serial'])
                    print("TRUE!!")
                else:
                    print(StoS[0]['model'])
            except meraki.APIError as e: #meraki API except
                print(f'Meraki API error: {e}')
                print(f'status code = {e.status}')
                print(f'reason = {e.reason}')
                print(f'error = {e.message}')
                print(net)
                print(StoS)
                continue
            except Exception as e: #sys/py env except
                print(f'some other error: {e}')
                print(StoS)

                continue
    meraki_Dict = dict(zip(mxSerial, zip(mxNames, mxModel))) #change tuple to iter. dict
    print(meraki_Dict)
    print("Total Meraki: ", len(meraki_Dict)) #len of ele's
    field_names = ["Serial Number", 'Direct URL', 'Model']
    # ntsql_Dict = inaccurateData()
    # print(ntsql_Dict)
    # print("Total NTSQL: ", len(ntsql_Dict)) #len of ele's
    # print(noSOHO_Dict)
    # print("Total No SOHO Setup: ", len(noSOHO_Dict))
    # matchingData(meraki_Dict, ntsql_Dict)
    with open('MerakiDataforAndy.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Serial Number', 'URL', 'Model'])
        for key, value in meraki_Dict.items():
            writer.writerow([key, value])

# def inaccurateData():

#     # pulling data from csv
#     # open the file in universal line ending mode
#     with open('inaccuratentsql.csv', 'r') as infile: #get ntsql data
#         # read the file as a dictionary for each row ({header : value})
#         reader = csv.DictReader(infile)
#         data = {}
#         for row in reader:
#             for header, value in row.items():
#                 try:
#                     data[header].append(value.strip())
#                 except KeyError:
#                     data[header] = [value]
#         # extract the variables you want
#     ips = data['ï»¿IP'] 
#     names = data['Name']
#     for index, name in enumerate(names):
#         names[index] = name + " VACANT SOHO SUBNET"
#     zip_iterator = zip(ips, names)
#     ntsql_Dict = dict(zip_iterator)
#     return ntsql_Dict


# def matchingData(meraki, ntsql): #BE CAREFUL HERE. DATA MANIPULATION ON PROD LEVEL BEGINS

#     matches = {**ntsql, **meraki} #merge dictionaries together now, where meraki takes precedence.
#     print(matches)
#     print("Total matches (INCLUDES VACANCIES. VACANIES WILL NOT HAVE SOHO IN THEIR NAME): ", len(matches))

#     with open ('soho_match_FINAL.csv', 'w') as csv_file:
#         writer = csv.writer(csv_file)
#         for key, value in matches.items():
#             writer.writerow([key, value])
#             # updateOrion(key, value) #BEGINNING CALL OF DATA MANIPULATION ON PROD LEVEL
#     os.system("pause")

# def updateOrion(subnet, desc): #ORION REQUEST
#     print(subnet)
#     print(desc)
#     subnet = "'%s'" % subnet
#     npm_server = 'orion'
#     username = ''
#     password = ''
#     try:

#         swis = SwisClient(npm_server, username, password)
#         print(subnet)
#         results = swis.query(f"SELECT Uri FROM IPAM.Subnet WHERE FriendlyName={subnet}")  # set valid NodeID!
#         uri = results['results'][0]['Uri']
#         swis.update(uri, Comments=f"{desc}")
#         obj = swis.read(uri)
#         print (obj)
#     except Exception as e:
#         print(f"Error: {e}")
#         print(results)
#         os.system("pause")
#         pass

if __name__ == '__main__':
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print(f'\nScript complete, total runtime {end_time - start_time}')
