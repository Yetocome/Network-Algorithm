#!/usr/bin/python
# -*- coding: UTF-8 -*-
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
    coordinates.append((0, uniform(0, 1)))  # n = 0
    a = coordinates[0][1]
    b = coordinates[0][1] + 1
    t = uniform(a+1/3, b-1/3)
    if t > 1:
        t -= 1
    coordinates.append((1, t))  # n = 1
    for n in range(1, N-1):  # n > 1
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
    coordinates.sort(key=lambda coord: coord[1])
    # coordinates.sort(key=lambda coord: coord[0])
    return coordinates


class FakePacket(object):
    """
    """

    def __init__(self, src, dst):
        self.src = src
        self.dst_coordinates = dst.coordinates
        # self.src = (src_ip, src_port)
        # self.dst = (dst_ip, dst_port)
        # self.protocol_type = protocol_type
        self.path_dis = 0


class S2Node(object):
    """The Shuffle Space Node Class
    """
    counter = 0

    def __init__(self, server_IDs=None):
        """Initialize the node with IDs of servers and coordinates of self&neighbours

        Args:
            servers - array of IDs
            coordinates - array of coordinates in different space
        """
        S2Node.counter += 1
        self.ID = S2Node.counter
        self.servers = server_IDs  # useless in this version
        self.coordinates = []
        self.neighbours = []
        self.repeated_neighbours = []

    def join_a_new_virtual_ring(self, coordinate):
        self.coordinates.append(coordinate)

    def add_neighbour(self, new_neighbour):
        if new_neighbour in self.repeated_neighbours:
            pass
        elif new_neighbour in self.neighbours:
            self.repeated_neighbours.append(new_neighbour)
        else:
            self.neighbours.append(new_neighbour)

    def __update_routing_tables(self):
        pass

    def __cal_CD(self, dst_coordinates):
        CD = []
        for x, y in zip(self.coordinates, dst_coordinates):
            CD.append(min(abs(x-y), 1-abs(x-y)))
        return CD

    def __cal_hash(self, pkt):
        pass

    def cal_MCD(self, dst_coordinates):
        return self.__cal_CD(dst_coordinates).sort[0]

    def forwarding(self, pkt):
        """Forward the packet delivered to this switch

        Returns: the path length of a sucessful delivered paket
        """
        if pkt.src is self:  # first hop
            V = []
            for neighbour in self.neighbours:
                if neighbour.cal_MCD(pkt.dst_coordinates) < \
                   self.cal_MCD(pkt.dst_coordinates):
                    V.append(neighbour)
            return V[self.__cal_hash(pkt)].forwarding(pkt)
        pkt.path_dis += 1
        if pkt.path_dis > 255:
            raise Exception('Possible loop routing')
        # recursive fowarding, this is the end condition
        if pkt.dst_coordinates == self.coordinates:
            return pkt.path_dis  # Successfully find the destination
        # assure that the forwarding is loop-free, otherwise it won't end
        else:
            mcds = []
            for neighbour in self.neighbours:
                mcds.append((neighbour, neighbour.cal_MCD(pkt.coordinates)))
                # though executed by neighour node, we assume that the
                # calculation happens in local; this will save the memory
                # needed by simulation
            mcds.sort(key=lambda mcd: mcd[1])  # sorted by mcd
            return mcds[0].forwarding(pkt)  # send packet to next switch

    def print_info(self):
        print('#', self.ID, 'S2 node info:')
        print('    coordinates:', self.coordinates)
        print('    neighour:', [ni.ID for ni in self.neighbours])
        print('    repeated_neighbours:', [ni.ID for ni in self.repeated_neighbours])


class S2Topo(object):
    """The Shuffle Space Topology Class

    "tell" nodes where they are and who their neighbours are
    """
    def __init__(self, N, L, d):
        """Topology construction

        Args:
            N: the number of switches
            L: the number of virtual rings
            d: the number of actually using rings
        """
        self.N = N
        self.L = L
        self.d = d
        self.topo = [S2Node() for i in range(N)]  # create N S2 nodes
        for i in range(L):
            reversed_ring = BRC_generation(N)
            ring = reversed_ring.copy()
            reversed_ring.reverse()
            last_v_id = ring[-1][0]
            last_rv_id = reversed_ring[-1][0]
            # for ring_id, v_node_id, v_node_coord in ring.enumerate():
            #     left_node = self.topo[ring[(N+ring_id-1)%N]]
            #     self.topo[v_node_id].join_a_new_virtual_ring(
            #         v_node_coord,
            #         [,]
            #     )
            for (v_id, v_coord), (rv_id, rv_coord) in zip(ring, reversed_ring):
                # print("last_v_id", last_v_id, "last_rv_id", last_rv_id)
                self.topo[v_id].join_a_new_virtual_ring(v_coord)
                self.topo[v_id].add_neighbour(self.topo[last_v_id])
                self.topo[rv_id].add_neighbour(self.topo[last_rv_id])
                last_v_id = v_id  # update for next
                last_rv_id = rv_id

    def __generate_coordinates(self, N):
        pass

    def __eliminate_free_ports(self):
        pass

    def sales(self, number):
        pass

    def print_info(self):
        for node in self.topo:
            node.print_info()


if __name__ == '__main__':
    # print(BRC_generation(20))
    S2Topo(100, 4, 4).print_info()
