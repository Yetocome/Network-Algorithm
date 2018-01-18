#!/usr/bin/python
# -*- coding: UTF-8 -*-


class SimplePacket(object):
    """
    """

    def __init__(self, coordinates, ID):
        self.dst_coordinates = coordinates
        self.dst_id = ID  # useless in this version
        self.path_dis = 0


class S2Node(object):
    """The Shuffle Space Node Class
    """

    def __init__(self, servers):
        """Initialize the node with ID of servers and coordinates of self&neighbours

        Args:
            servers - array of IDs
            coordinates - array of coordinates in different space
        """
        self.servers = servers
        self.coordinates = []
        self.neighbours = []

    def join_a_new_virtual_ring(self, coordinate, neighbours):
        self.coordinates.append(coordinate)
        

    def __update_routing_tables(self):
        pass

    def __cal_MDC(self, X, Y):
        MIN = 0.5
        for x, y in zip(X, Y):
            MIN = min(MIN, min(x, y))

    def forwarding(self, pkt):
        """Forward the packet delivered to this switch

        Args:

        Returns:
        """
        pkt.path_dis += 1
        if pkt.dst_coordinates == self.coordinates:
            return True  # Successfully find the destination
        else:

            return False  # Still need routing


class S2Topo(object):
    """The Shuffle Space Topology Class

    assign the coordinates to each nodes
    """
    def __init__(self, N, L, d):
        pass
