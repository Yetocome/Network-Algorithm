#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
M = 16
MAX_SIZE = 2**M


class ChordNodeInfo:
    """节点信息的数据结构，这里仅仅用IP和端口号来标识"""
    def __init__(self, ip='192.168.0.1', port='8080'):
        self.IP = ip
        self.PORT = port


class FileInfo:
    """文件信息的数据结构，包括其名字，Hash值和所在节点的列表
    """
    def __init__(self, KID, Name):
        self.name = Name
        self.DHTID = KID
        self.saved_Node = []

    def add_Place(self, ChordNodeInfo):
        self.saved_Node.append(ChordNodeInfo)


# # 一个简单的自定义的针对节点信息的Hash函数
# def Hash(NInfo):
#     subip = NInfo.IP.split('.')
#     id = 0
#     for i in range(4)[::-1]:
#         id += int(subip[i])*(2**(i*4))
#     id += NInfo.PORT*(2**16)
#     print('You get the hash value,', id % MAX_SIZE)
#     return id % MAX_SIZE

def my_hash(info):
    return hash(info) % MAX_SIZE


class ChordNode(object):
    """最核心的Chord节点类"""

    def __init__(self, ChordNodeInfo, FNode=None):
        """Chord节点类的构造函数，模拟时还需要输入节点的信息
        要加入Chord环，还需要找到环内任意一个节点进行“通信”

        Args:
            ChordNodeInfo: 节点的IP和端口信息
            FNode: 选择一个认识的节点
        """
        super(ChordNode, self).__init__()
        self.NInfo = ChordNodeInfo
        self.NID = my_hash(ChordNodeInfo)
        self.predecessor = None
        self.preSource = {}  # File will be saved in this map
        self.FingerTable = {}
        self.last_request_path = 0

        # Init Self and Neighbour
        if FNode is None:
            self.successor = self
            for i in range(M):
                self.FingerTable[(self.NID+2**i) % MAX_SIZE] = self
            self.predecessor = self
        else:
            self.successor = FNode.find_successor(self.NID)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            # 重要数据结构，保存一个长度为M的hash表
            self.FingerTable[self.NID+1] = self.successor
            # Initialize finger_table
            for i in range(M-1):
                Last = (self.NID+2**i) % MAX_SIZE
                Curr = (Last+2**i) % MAX_SIZE
                if self.in_interval(Curr,
                                    self.NID,
                                    self.FingerTable[Last].NID):
                    self.FingerTable[Curr] = self.FingerTable[Last]
                else:
                    self.FingerTable[Curr] = FNode.find_successor(Curr)
            # Update Others
            self.update_others()

        # preSource Update
        for key, value in self.successor.preSource.items():
            if key <= self.NID:
                self.preSource[key] = value
                self.successor.preSource.pop(key)

    def find_successor(self, KID, hops=0):
        """关键函数：通过ID号寻找最近的后继节点，几乎所有操作都离不开它
        """
        if hops > 255:
            raise Exception('out of range')
        if(self.NID == KID):
            # print('hops is', hops)
            self.last_request_path = hops
            return self
        elif(self.in_interval(KID, self.NID, self.successor.NID)):
            self.successor.last_request_path = hops+1
            return self.successor
        else:
            pNode = self.get_ClosestNode_in_FingerTable(KID)
            return pNode.find_successor(KID, hops+1)

    def update_others(self):
        """节点初始化时用来更新与之相关节点的FingerTable
        """
        for i in range(M):
            pNode = self.find_successor((self.NID-2**i) % MAX_SIZE)
            pNode.update_finger_table(self, i)

    def update_finger_table(self, s, i):
        """辅助函数：用于更新finger table
        """
        Curr = (self.NID+2**i) % MAX_SIZE
        if self.in_interval(s.NID, self.NID, self.FingerTable[Curr].NID):
            self.FingerTable[Curr] = s
            pNode = self.predecessor
            pNode.update_finger_table(s, i)

    def in_interval(self, KID, FID, BID):
        """判断ID是否在某个区间内，不同的DHT算法实现方式不同，在这里的定义是是环状结构某一弧内
        """
        if BID > FID:
            return (KID > FID and KID <= BID)
        else:
            return (KID > FID or KID <= BID)

    def get_ClosestNode_in_FingerTable(self, KID):
        """find_successor的辅助函数：寻找在FingerTable中距离某个ID最近的节点
        """
        for i in range(M)[::-1]:
            curr = (self.NID+2**i) % MAX_SIZE
            if self.FingerTable[curr] is None:
                continue
            # elif (self.FingerTable[curr].NID == KID):
            #     continue
            elif (self.in_interval(self.FingerTable[curr].NID, self.NID, KID)):
                # if self.FingerTable[curr].NID == KID:
                #     return self.successor
                # else:
                return self.FingerTable[curr]
        # return self.successor

    def fix_FingerTable(self):
        """自己对FingerTable内的表项的更新
        """
        for i in range(M):
            Curr = (self.NID+2**i) % MAX_SIZE
            self.FingerTable[Curr] = self.find_successor(Curr)
            if self.FingerTable[Curr] == self:
                for j in range(i+1, M):
                    self.FingerTable[(self.NID+2**j) % MAX_SIZE] = self
                break

    def add_Source(self, Content, Name='Untitled'):
        """模拟使用，依据内容和名字表示某个节点保存了一个新的文件
        """
        KID = hash(Content)
        FInfo = FileInfo(KID, Name)
        Info_saved_Node = self.find_successor(KID)
        if Info_saved_Node.preSource.get(KID) is None:
            Info_saved_Node.preSource[KID] = FInfo
        Info_saved_Node.preSource.get(KID).add_Place(self.NInfo)

    def add_Source_by_ID(self, KID, Name='Untitled'):
        """模拟使用，依据Hash值和名字表示某个节点保存了一个新的文件
        和上一个函数的区别时测试时可以自定义文件Hash值
        """
        FInfo = FileInfo(KID, Name)
        Info_saved_Node = self.find_successor(KID)
        if Info_saved_Node.preSource.get(KID) is None:
            Info_saved_Node.preSource[KID] = FInfo
        Info_saved_Node.preSource.get(KID).add_Place(self.NInfo)

    def stabilize(self):
        """稳定函数：用于更新节点的前继和后继，设定应该是定期执行
        没有及时执行会对效率有一定影响，但应该是收束在某个范围内的
        """
        while self.successor.predecessor != self:
            self.successor = self.successor.predecessor
            if(self.successor.predecessor is None or
               self.in_interval(self.NID,
                                self.successor.predecessor.NID,
                                self.successor.NID)):
                self.successor.predecessor = self
        self.fix_FingerTable()

    def print_info(self, table=False):
        """打印节点的某些信息，测试用"""
        print('You reached here by', self.last_request_path, 'hops')
        print('The information of Node-'+str(self.NID))
        # print('IP: ', self.NInfo.IP)
        # print('PORT: ', self.NInfo.PORT)
        print('Predecessor: Node-'+str(self.predecessor.NID))
        print('Successor: Node-'+str(self.successor.NID))
        print('File index:')
        if self.preSource == {}:
            print('(It seems that no file is in this node.)')
        else:
            for key, value in self.preSource.items():
                print(key, value.name, 'saved in:')
                for index, place in enumerate(value.saved_Node):
                    # print('['+str(index)+']', place.IP, place.PORT)
                    print('['+str(index)+']', place)
        if table:
            self.print_finger_table()

    def print_finger_table(self):
        print('FingerTable:')
        for i in range(M):
            Curr = (self.NID+2**i) % MAX_SIZE
            if self.FingerTable[Curr] is not None:
                print(Curr, 'Node-'+str(self.FingerTable[Curr].NID))
            else:
                print(Curr, 'Node-None')


def stabilize_all(list):
    """单线程测试版本的整合函数，相当于在输出测试结果前所有节点自己更新了一次"""
    # stabilize from back to front
    for i in range(list.__len__())[::-1]:
        list[i].stabilize()
    # stabilize from front to back
    for i in range(list.__len__()):
        list[i].stabilize()


def print_info_all(list):
    """打印的整合函数，省去了对每个节点调用一次打印函数的代码"""
    for node in list:
        node.print_info()


def rand_string(size=M):
    seed = "1234567890abcdefghijklmnopqrstuvwxyz\
            ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    salt = ''
    for i in range(M):
        salt += random.choice(seed)
    return salt


if __name__ == '__main__':
    fnode = ChordNode(rand_string())
    chord_chain = [fnode]+[ChordNode(rand_string(), fnode) for i in range(100)]
    stabilize_all(chord_chain)

    chord_chain[15].add_Source('Hello, World!', 'Hello.txt')
    chord_chain[13].add_Source('Good morning, World!', 'Morning.txt')
    chord_chain[12].add_Source('Have fun!', 'Fun.txt')
    chord_chain[10].add_Source('Hello, World!', 'Hello.txt')
    chord_chain[9].add_Source('Let\'s play!', 'Play.txt')
    chord_chain[19].add_Source('!', 'Short.txt')
    chord_chain[2].add_Source(12345, 'ID_0.txt')
    chord_chain[3].add_Source(23456, 'ID_1.txt')
    chord_chain[4].add_Source(44635, 'ID_2.txt')
    # print_info_all(chord_chain)
    KID = hash('Have fun!')
    t = chord_chain[8].find_successor(KID)
    print('WE GET THE FILE by', t.last_request_path, 'hops')
    # t.print_info()
    # print('PREDECESSOR NODEINFO IS\n\n\n')
    # t.predecessor.print_info()
    # print('I found \'Have fun!\' for', t.last_request_path, 'hops')
