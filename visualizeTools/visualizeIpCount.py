import numpy as np
import json
import matplotlib.pyplot as plt
from collections import Counter

# This WILL require matplotlib; it has been
# installed using homebrew on my machine
def readNormalized(fileName):
    hosts, ips, counts = [], [], []
    with open(fileName, 'r') as fp:
        for line in fp.readlines():
            val = json.loads(line)
            hosts.append(val["hostname"])
    frequency = Counter(hosts).most_common()
    for ip, count in frequency:
    	ips.append(ip)
    	counts.append(count)
    plt.plot(ips, counts)
    plt.xlabel('hostnames')
    plt.ylabel('vendor count')
    plt.show()


readNormalized('../data/normalized.json')