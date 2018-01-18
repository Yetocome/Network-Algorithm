#!/usr/bin/python
# -*- coding: UTF-8 -*-

M = 16
Max_Size = 2**M


class NodeInfo:
    """节点信息的数据结构，这里仅仅用IP和端口号来标识"""
    def __init__(self, ip, port):
        self.IP = ip
        self.PORT = port
# 文件信息的数据结构，包括其名字，Hash值和所在节点的列表


class FileInfo:
    def __init__(self, KID, Name):
        self.name = Name
        self.DHTID = KID
        self.saved_Node = []

    def add_Place(self, NodeInfo):
        self.saved_Node.append(NodeInfo)


# 一个简单的自定义的针对节点信息的Hash函数
def Hash(NInfo):
    subip = NInfo.IP.split('.')
    id = 0
    for i in range(4)[::-1]:
        id += int(subip[i])*(2**(i*4))
    id += NInfo.PORT*(2**16)
    return id%Max_Size


class ChordNode(object):
    """最核心的Chord节点类"""
    # Chord节点类的构造函数，模拟时还需要输入节点的信息，要加入Chord环，还需要找到环内任意一个节点进行“通信”
    def __init__(self, NodeInfo, FNode = None):
        super(ChordNode, self).__init__()
        self.NInfo = NodeInfo
        self.NID = Hash(NodeInfo)
        self.predecessor = None
        self.preSource = {}
        self.FingerTable = {}

        # Init Self and Neighbour
        if FNode == None:
            self.successor = self
            for i in range(M):
                self.FingerTable[(self.NID+2**i)%Max_Size] = self
            self.predecessor = self
        else:
            self.successor = FNode.find_successor(self.NID)
            self.predecessor = self.successor.predecessor
            self.successor.predecessor = self
            # 重要数据结构，保存一个长度为M的hash表
            self.FingerTable[self.NID+1] = self.successor
            #Initialize finger_table
            for i in range(M-1):
                Last = (self.NID+2**i)%Max_Size
                Curr = (Last+2**i)%Max_Size
                if self.in_interval(Curr, self.NID, self.FingerTable[Last].NID):
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
    # 关键函数：通过ID号寻找最近的后继节点，几乎所有操作都离不开它
    def find_successor(self, KID):
        if(self.NID == KID):
            return self
        elif(self.in_interval(KID, self.NID, self.successor.NID)):
            return self.successor
        else:
            pNode = self.get_ClosestNode_in_FingerTable(KID)
            return pNode.find_successor(KID)

    # 节点初始化时用来更新与之相关节点的FingerTable
    def update_others(self):
        for i in range(M):
            pNode = self.find_successor((self.NID-2**i)%Max_Size)
            pNode.update_finger_table(self, i)

    # 更新函数的辅助函数
    def update_finger_table(self, s, i):
        Curr = (self.NID+2**i)%Max_Size
        if self.in_interval(s.NID, self.NID, self.FingerTable[Curr].NID):
            self.FingerTable[Curr] = s
            pNode = self.predecessor
            pNode.update_finger_table(s, i)

    # 判断ID是否在某个区间内，不同的DHT算法有着不同的实现，在这里的定义是是环状结构某一弧内
    def in_interval(self, KID, FID, BID):
        if BID > FID:
            return (KID > FID and KID <= BID)
        else:
            return (KID > FID or KID <= BID)

    # find_successor的辅助函数：寻找在FingerTable中距离某个ID最近的节点
    def get_ClosestNode_in_FingerTable(self, KID):
        for i in range(M)[::-1]:
            curr = (self.NID+2**i)%Max_Size
            if self.FingerTable[curr] == None:
                continue
            # elif (self.FingerTable[curr].NID == KID):
            #     continue
            elif (self.in_interval(self.FingerTable[curr].NID, self.NID, KID)):
                # if self.FingerTable[curr].NID == KID:
                #     return self.successor
                # else:
                return self.FingerTable[curr]
        # return self.successor

    # 自己对FingerTable内的表项的更新
    def fix_FingerTable(self):
        for i in range(M):
            Curr = (self.NID+2**i)%Max_Size
            self.FingerTable[Curr] = self.find_successor(Curr)
            if self.FingerTable[Curr] == self:
                for j in range(i+1, M):
                    self.FingerTable[(self.NID+2**j)%Max_Size] = self
                break

    # 模拟使用，依据内容和名字表示某个节点保存了一个新的文件
    def add_Source(self, Content, Name):
        KID = hash(Content)
        FInfo = FileInfo(KID, Name)
        Info_saved_Node = self.find_successor(KID)
        if Info_saved_Node.preSource.get(KID) == None:
            Info_saved_Node.preSource[KID] = FInfo
        Info_saved_Node.preSource.get(KID).add_Place(self.NInfo)

    # 模拟使用，依据Hash值和名字表示某个节点保存了一个新的文件，和上一个函数的区别时测试时可以自定义文件Hash值
    def add_Source_by_ID(self, KID, Name):
        FInfo = FileInfo(KID, Name)
        Info_saved_Node = self.find_successor(KID)
        if Info_saved_Node.preSource.get(KID) == None:
            Info_saved_Node.preSource[KID] = FInfo
        Info_saved_Node.preSource.get(KID).add_Place(self.NInfo)

    def stabilize(self):
        """
            稳定函数：用于更新节点的前继和后继，设定应该是定期执行
            没有及时执行会对效率有一定影响，但应该是收束在某个范围内的
        """
        while self.successor.predecessor != self:
            self.successor = self.successor.predecessor
            if(self.successor.predecessor == None or self.in_interval(self.NID, self.successor.predecessor.NID, self.successor.NID)):
                self.successor.predecessor = self
        self.fix_FingerTable()

    def print_info(self):
        """打印节点的某些信息，测试用"""
        print('The information of Node-'+str(self.NID))
        print('IP: ', self.NInfo.IP)
        print('PORT: ', self.NInfo.PORT)
        print('Predecessor: Node-'+str(self.predecessor.NID))
        print('Successor: Node-'+str(self.successor.NID))
        print('File index:')
        if self.preSource == {}:
            print('(It seems that no file is in this node.)')
        else:
            for key, value in self.preSource.items():
                print(key, value.name, 'saved in:')
                i = 0
                for place in value.saved_Node:
                    print('['+str(i)+']', place.IP, place.PORT)

        print('FingerTable:')
        for i in range(M):
            Curr = (self.NID+2**i)%Max_Size
            if self.FingerTable[Curr] != None:
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
