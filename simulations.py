#!/usr/bin/python
# -*- coding: UTF-8 -*-

from s2 import S2Topo
from chord import ChordNode, stabilize_all, rand_string, print_info_all
import matplotlib.pyplot as plt
import math
import random


class SimData(object):
    """This Class is designed to simplify the helper funciton of each simulations
    Due to the limited time, there is no realization now
    """
    def __init__(self):
        self.avg = 0
        sekf.data = {}

def helper_find_percentile(data, size, percentile, zero_hop_enabled=False):
    print('Now handling the percentile', data, size)
    base = 0
    count = 0
    index = 1
    if zero_hop_enabled:
        index = 0
    limit = math.ceil(size*percentile/100)
    while base < limit:
        try:
            count = data[index]
            base += count
            index += 1
        except KeyError:
            index += 1
    return index-1


def helper_s2_sim(num, ports, used_ports, neighour_level):
    """This function will simulate a shuffle space case with the given conditions
    The raw data is also stored in a dict because it may not be continuous
    Returns:
        The dict of the results
    """
    data = {'avg': None, 'raw': {}, '90p': None, '10p': None, 'largest': 0}
    topo = S2Topo(num, ports, used_ports, neighour_level)
    data['connections'] = num*(num-1)/2
    sum = 0

    for index_a in range(num):
        for index_b in range(index_a+1, num):
            length = topo.cal_path(index_a, index_b)
            if data['raw'].get(length) is None:
                print('New length found:', length)
                data['raw'][length] = 1
                if length > data['largest']:
                    data['largest'] = length
            else:
                data['raw'][length] += 1  # create a new bin

    for key, value in data['raw'].items():
        sum += key*value
    data['avg'] = sum/data['connections']
    data['10p'] = helper_find_percentile(data['raw'], data['connections'], 10)
    data['90p'] = helper_find_percentile(data['raw'], data['connections'], 90)
    return data


def s2_sim_1():
    result = helper_s2_sim(250, 4, 4, 2)
    print('The average path length is', result['avg'])
    print('The 10th percentile of the data is', result['10p'])
    print('The 90th percentile of the data is', result['90p'])
    print('The largest routing path length is', result['largest'])
    boundary = min(12, result['largest'])
    x = [i for i in range(1, boundary+1)]
    y = []

    for i in range(1, boundary+1):
        try:
            y.append(result['raw'][i]/result['connections'])
        except KeyError:
            y.append(0)
            print('Just a blank area, don\'t worrry')
    plt.plot(x, y)
    plt.title('PDF (250-node, 8 ports, 2 hops storation)')
    plt.ylabel('Percentage')
    plt.xlabel('Routing Path Length (Average: '+str(result['avg'])+')')
    plt.show()


def s2_sim_2():
    x = []
    y1 = []
    y2 = []
    y3 = []

    for scales in range(50, 501, 50):
        result = helper_s2_sim(scales, 4, 4, 2)
        x.append(scales)
        y1.append(result['avg'])
        y2.append(result['10p'])
        y3.append(result['90p'])
    fig, ax = plt.subplots()
    ax.plot(x, y1, 'k', label='Average')
    ax.plot(x, y2, 'k--', label='10th percentile')
    ax.plot(x, y3, 'k:', label='90th percentile')
    ax.legend(loc='upper left', shadow=True)
    plt.title('Routing Path Length vs. Scale')
    plt.ylabel('Routing Path Length')
    plt.xlabel('Node Scale')
    plt.show()


def s2_sim_3():
    x = [i for i in range(1, 11)]
    result1 = helper_s2_sim(250, 4, 4, 1)
    result2 = helper_s2_sim(250, 4, 4, 2)
    result3 = helper_s2_sim(250, 4, 4, 3)
    y1 = []
    y2 = []
    y3 = []

    for i in range(1, 11):
        try:
            y1.append(result1['raw'][i]/result1['connections'])
        except KeyError:
            y1.append(0)
        try:
            y2.append(result2['raw'][i]/result2['connections'])
        except KeyError:
            y2.append(0)
        try:
            y3.append(result3['raw'][i]/result3['connections'])
        except KeyError:
            y3.append(0)
    fig, ax = plt.subplots()
    ax.plot(x, y1, 'k', label='Stored 1 hop (Avg:'+str(result1['avg'])+')')
    ax.plot(x, y2, 'k--', label='Stored 2 hops (Avg:'+str(result2['avg'])+')')
    ax.plot(x, y3, 'k:', label='Stored 3 hops (Avg:'+str(result3['avg'])+')')
    ax.legend(loc='upper right', shadow=True)
    plt.title('PDF - Routing Path Length Distribution vs. storation hops')
    plt.ylabel('Percentage')
    plt.xlabel('Routing Path Length')
    plt.show()


def s2_sim_4():
    x = []
    y1 = []
    y2 = []
    y3 = []

    for sp in range(2, 6):
        result = helper_s2_sim(250, sp, sp, 2)
        x.append(sp)
        y1.append(result['avg'])
        y2.append(result['10p'])
        y3.append(result['90p'])
    fig, ax = plt.subplots()
    ax.plot(x, y1, 'k', label='Average')
    ax.plot(x, y2, 'k--', label='10th percentile')
    ax.plot(x, y3, 'k:', label='90th percentile')
    ax.legend(loc='upper right', shadow=True)
    plt.title('Routing Path Length vs. #Virtual Spaces')
    plt.ylabel('Average Routing Path Length')
    plt.xlabel('#Virtual Spaces')
    plt.show()


def s2_sim_5():
    pass


def helper_chord_sim(node_scale):
    data = {'avg': None, 'raw': {}, '90p': None, '10p': None, 'largest': 0}
    data['connections'] = node_scale*(node_scale-1)/2
    sum = 0
    chain = [ChordNode(rand_string())]  # First Node
    chain += [ChordNode(rand_string(), chain[0]) for i in range(node_scale-1)]
    stabilize_all(chain)

    # print_info_all(chain)
    for index_a in range(node_scale):
        for index_b in range(index_a+1, node_scale):
            length = chain[index_a].find_successor(chain[index_b].NID).last_request_path
            if data['raw'].get(length) is None:
                print('New length found:', length)
                data['raw'][length] = 1
                if length > data['largest']:
                    data['largest'] = length
            else:
                data['raw'][length] += 1  # create a new bin
            sum += length

    data['avg'] = sum/data['connections']
    data['10p'] = helper_find_percentile(data['raw'], data['connections'], 10, True)
    data['90p'] = helper_find_percentile(data['raw'], data['connections'], 90, True)
    return data


def chord_sim_1():
    result = helper_chord_sim(250)
    print('The average path length is', result['avg'])
    print('The 10th percentile of the data is', result['10p'])
    print('The 90th percentile of the data is', result['90p'])
    print('The largest routing path length is', result['largest'])
    boundary = min(12, result['largest'])
    x = [i for i in range(1, boundary+1)]
    y = []

    for i in range(1, boundary+1):
        try:
            y.append(result['raw'][i]/result['connections'])
        except KeyError:
            y.append(0)
            print('Just a blank area, don\'t worrry')
    plt.plot(x, y)
    plt.title('PDF (250-node)')
    plt.ylabel('Percentage')
    plt.xlabel('Routing Path Length (Average: '+str(result['avg'])+')')
    plt.show()


def chord_sim_2():
    x = []
    y1 = []
    y2 = []
    y3 = []

    for scales in range(50, 501, 50):
        result = helper_chord_sim(scales)
        x.append(scales)
        y1.append(result['avg'])
        y2.append(result['10p'])
        y3.append(result['90p'])
    fig, ax = plt.subplots()
    ax.plot(x, y1, 'k', label='Average')
    ax.plot(x, y2, 'k--', label='10th percentile')
    ax.plot(x, y3, 'k:', label='90th percentile')
    ax.legend(loc='upper left', shadow=True)
    plt.title('Routing Path Length vs. Scale')
    plt.ylabel('Routing Path Length')
    plt.xlabel('Node Scale')
    plt.show()

def chord_sim_3():
    pass

s2_sim_3()

# BUG NOTES
# 1. when there are two unconnected free ports, the simulation may fail
