import json
from collections import defaultdict


def dedupVendorData(fileName, frequency):
    ips = []
    for ipAddress, freq in frequency:
        if freq > 1:
            ips.append(ipAddress)
    for ip in ips:  # for every hostname that is duplicated
        jlists = []
        with open(fileName, 'r') as fp, open('./data/results.json', 'w') as fw:
            for line in fp.readlines():
                val = json.loads(line)
                if ip != val["hostname"]:
                    fw.write(str(val) + '\n')
                else:
                    jlists.append(val)
            newData = merge_dict(jlists)
            fw.write(str(newData) + "\n")
    return

def merge_dict(dct):
    dd = defaultdict(list)
    for d in dct:
        for key, value in d.items():
            if not isinstance(value, list):
                if value != "unknown":
                    # same key won't have unknown in all dicts
                    dd[key] = value
            else:
                dd[key].extend(value)
    return dict(dd)


if __name__ == '__main__':
    dct1 = {
                "hostname": "ip-172-31-93-76.ec2.internal",
                "ip_addr": "172.31.93.76", 
                "manufacturer": "unknown", 
                "platform": "unknown",
                "cloud": "unknown", 
                "os_version": "Amazon Linux 2", 
                "region": "us-east-1b",
                "vendor":[
                    {
                        "crowdstrike": {
                            "s1": "1"
                        }
                    }
                ]
            }
    dct2 = {
                "hostname": "ip-172-31-93-76.ec2.internal",
                "ip_addr": "172.31.93.76",
                "manufacturer": "Xen",
                "platform": "Linux",
                "cloud": "AWS",
                "os_version": "Amazon Linux 2",
                "region": "unknown",
                "vendor":[
                    {
                        "qualys": {
                            "s2": "2"
                        }
                    }
                ]
            }
    dct3 = {
                "hostname": "ip-172-31-93-76.ec2.internal",
                "ip_addr": "172.31.93.76",
                "manufacturer": "unknown",
                "platform": "unknown",
                "cloud": "AWS",
                "os_version": "unknown",
                "region": "unknown",
                "vendor":[
                    {
                        "panw": {
                            "s3": "3"
                        }
                    }
                ]
            }
    combined_dct = merge_dict([dct1, dct2, dct3])
    json_str3 = json.dumps(combined_dct)
    print(json_str3)
    fileName = "output.json"
    frequency = [('ip-172-31-93-76.ec2.internal', 2),
                 ('ip-172-31-14-41.ec2.internal', 1),
                 ('ip-172-31-19-223.ec2.internal', 1)]
    dedupVendorData(fileName, frequency)
