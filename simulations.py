#!/usr/bin/python
# -*- coding: UTF-8 -*-

from s2 import S2Topo
from chord import ChordNode, stabilize_all
import matplotlib.pyplot as plt
import math


def helper_find_percentile(data, percentile):
    pass


def s2_sim_tool(num, ports, used_ports, neighour_level):
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
    data['10p'] = helper_find_percentile(data, 10)
    data['90p'] = helper_find_percentile(data, 90)
    return data


def s2_sim_1():
    result = s2_sim_tool(250, 4, 4, 2)
    print('The average path length is', result['avg'])
    print('The 10th percentile of the data is', result['10p'])
    print('The 90th percentile of the data is', result['90p'])
    print('The largest routing path length is', result['largest'])
    boundary = min(13, result['largest'])
    x = [i for i in range(1, boundary)]
    y = []
    for i in range(1, boundary):
        y.append(result['raw'][i]/result['connections'])
    plt.plot(x, y)
    plt.title('Average path length - '+str(result['avg']))
    plt.show()


def s2_sim_2():
    x = []
    y1 = []
    y2 = []
    y3 = []
    for scales in range(50, 501, 50):
        result = s2_sim_tool(scales, 4, 4, 2)
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
    plt.ylabel('Average Routing Path Length')
    plt.xlabel('Number of Nodes')
    plt.show()


def s2_sim_3():
    for hops in range(3):
        result = s2_sim_tool(250, 4, 4, hops)
        plt.hist(result['raw'], 50)
        plt.title('Average path length - '+str(result['avg']))
        plt.show()


def s2_sim_4():
    x = []
    y1 = []
    y2 = []
    y3 = []
    for sp in range(2, 6):
        result = s2_sim_tool(250, sp, sp, 2)
        x.append(sp)
        y1.append(result['avg'])
        y2.append(result['10p'])
        y3.append(result['90p'])
    fig, ax = plt.subplots()
    ax.plot(x, y1, 'k', label='Average')
    ax.plot(x, y2, 'k--', label='10th percentile')
    ax.plot(x, y3, 'k:', label='90th percentile')
    ax.legend(loc='upper left', shadow=True)
    plt.title('Routing Path Length vs. Scale')
    plt.ylabel('Average Routing Path Length')
    plt.xlabel('Number of Nodes')
    plt.show()


def s2_sim_5():
    pass


def chord_sim_1():
    pass


s2_sim_1()
