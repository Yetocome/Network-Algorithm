#!/usr/bin/python
# -*- coding: UTF-8 -*-

from s2 import *
from random import uniform


def helper_find_smallest_pair(l, n):
    """helper function to find the smallest difference in a sorted list

    return: the index pair
    """
    r1 = n-1
    r2 = 0
    diff = min(l[r1][1]-l[r2][1], 1+l[r2][1]-l[r1][1])
    for i in range(n-1):
        new_diff = min(diff, l[i+1][1]-l[i][1])
        if new_diff != diff:
            r1 = i
            r2 = i+1
            diff = new_diff
    return (r1, r1)


def BRC_generation(N):
    coordinates = []
    coordinates.append((1, uniform(0, 1)))  # n = 0
    a = coordinates[0][1]
    b = coordinates[0][1] + 1
    t = uniform(a+1/3, b-1/3)
    if t > 1:
        t -= 1
    coordinates.append((2, t))  # n = 1
    for n in range(2, N):  # n > 1
        coordinates.sort(key=lambda coord: coord[1])
        tr1, tr2 = helper_find_smallest_pair(coordinates, n)
        # not real r1 and r2, just the indexes of this sorted list

        if tr2 == n:  # it may be the last element
            tr1 = 0
            tr2 = n-1
        # print('Now tr1 is ', tr1, ' and tr2 is ', tr2)
        xr1 = coordinates[tr1][1]
        xr2 = coordinates[tr2][1]
        if xr2 - xr1 > 1/2:  # I reverse the condition in paper
            a = xr1
            b = xr2
        else:
            a = xr2
            b = xr1+1
        t = uniform(a+1/3/n, b-1/3/n)
        if t > 1:
            t -= 1
        coordinates.append((n+1, t))
    coordinates.sort(key=lambda coord: coord[0])
    return coordinates


if __name__ == '__main__':
    print(BRC_generation(20))
