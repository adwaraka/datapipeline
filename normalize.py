import multiprocessing
from collections import Counter
import time, json

from fetchVendorData import VendorData
from dedupe import dedupVendorData


class VendorDetails(object):

    def __init__(self):
        pass

    def fetchVendorDetail(self, vendor, skip, level, timeout):
        vendorData = VendorData(vendor, skip, level)
        vendorDetails = vendorData.fireRequest()
        vendorDetails = json.loads(vendorDetails)
        for details in vendorDetails:
            yield details
        time.sleep(timeout)


# normalize the output
def normalize(vData, vendor):
    jData = {}

    if vendor in ['crowdstrike']:
        jData['hostname'] = vData['hostname']
    elif vendor in ['qualys']:
        jData['hostname'] = vData['dnsHostName']

    if vendor in ['crowdstrike']:
        jData['ip_addr'] = vData['connection_ip']
    elif vendor in ['qualys']:
        jData['ip_addr'] = vData['address']

    if vendor in ['crowdstrike']:
        jData['manufacturer'] = vData['bios_manufacturer']
    elif vendor in ['qualys']:
        jData['manufacturer'] = vData['manufacturer']

    if vendor in ['crowdstrike']:
        jData['platform'] = vData['platform_name']
    elif vendor in ['qualys']:
        jData['platform'] = vData["agentInfo"]['platform']

    if vendor in ['crowdstrike']:
        jData['cloud'] = "unknown"
    elif vendor in ['qualys']:
        jData['cloud'] = vData['cloudProvider']

    if vendor in ['crowdstrike']:
        jData['os_version'] = vData['os_version']
    elif vendor in ['qualys']:
        jData['os_version'] = vData['os']

    if vendor in ['crowdstrike']:
        jData['region'] = vData['zone_group']
    elif vendor in ['qualys']:
        jData['region'] = "unknown"

    if vendor in ['crowdstrike']:
        vJson = {'crowdstrike': vData}
    elif vendor in ['qualys']:
        vJson = {'qualys': vData}
    jData['vendor'] = [vJson]

    return json.dumps(jData)


def fetchCrwdDetails(normalizedData):
    crwdDetails  = VendorDetails()
    for crwdData in crwdDetails.fetchVendorDetail('crowdstrike', 0, 2, 1):
        normalizedData.put(normalize(crwdData, 'crowdstrike'))


def fetchQlysDetails(normalizedData):
    qlysDetails, op = VendorDetails(), []
    for qlysData in qlysDetails.fetchVendorDetail('qualys', 0, 2, 5):
        normalizedData.put(normalize(qlysData, 'qualys'))


def readDetails(normalizedData):
    with open('./data/normalized.json', 'w') as fp:
        while True:
            msg = normalizedData.get()
            if msg == "":
                break
            fp.write(msg + '\n')
            fp.flush()


def dedupe(fileName):
    print("Running Deduping Ops")
    hosts = []
    with open(fileName, 'r') as fp:
        for line in fp.readlines():
            val = json.loads(line)
            hosts.append(val.get("hostname"))
    frequency = Counter(hosts).most_common()
    dedupeRequired = False
    for ipAddress, freq in frequency:
        if freq == 1:
            continue
        else:
            dedupeRequired = True
            break
    if dedupeRequired:
        print("Duplicate IP addresses found. Deduping Ops Starting.")
        dedupVendorData(fileName, frequency)
    else:
        print("Dedupe logic not required.")
    print("Completed")


def execute():
    with multiprocessing.Manager() as manager:
        normalizedData = manager.Queue()
        pool = multiprocessing.Pool(multiprocessing.cpu_count())

        v1 = pool.apply_async(fetchCrwdDetails, (normalizedData,)) 
        v2 = pool.apply_async(fetchQlysDetails, (normalizedData,))
        rd = pool.apply_async(readDetails, (normalizedData,))

        v1.get()
        v2.get()

        normalizedData.put("")
        pool.close()
        pool.join()
    dedupe('./data/normalized.json')

execute()