# Introduction
This repository is created for simple simulations of well-known networking algorithms. The simulations are all of recursive style.

I will post some of my simulation results here. My simulation focus is on routing and caching efficiency (Routing path length and routing tables cost). The simulation scale is small restricted by my laptop performance, there would be some error statistically.



## Space Shuffle<sup>[[1]](http://ieeexplore.ieee.org/document/7416229/)</sup>

Space Shuffle provides a new solution for the architectures of data center networks.

### Routing Path Length:

* Experiment 1 - fixed condition

![Figure 1](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_1.png)
* Experiment 2 - when node number scales

![Figure 2](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_2.png)
* Experiment 3 - when stored hops scales

![Figure 3](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_3.png)
* Experiment 4 - when available spaces scales

![Figure 4](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_4.png)
* Experiment 5 - when used spaces scales



## Chord Protocol<sup>[[2]](https://dl.acm.org/citation.cfm?id=383071)</sup>
Chord protocol is one of the most famous P2P protocols.



### Routing Path Length

* Experiment 1 - fixed condition

![Figure 5](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_5.png)
* Experiment 2 - when node number scales

![Figure 6](https://github.com/mhxie/Networking-Algorithm/blob/master/s2_vs_chord/figures/Figure_6.png)

We can see that the curve is not so smooth. That's because the node ID is determined randomly in my simulations, which may lead a quite imbalanced assignment results. Obviously, a more balanced assignment will decrease the average routing path effectively.

### Finger Tables:

The size of finger table is determined by the size of the virtual space. The transformation is:

size of finger table = log2(size of virtual space)

We can see that there is some redundancy in a finger table. Each entry of this table is pointed to a successor. When there is no node between its KID and (its KID + 2^i), the entry saves a redundant successor. The redundant exists very likely because the M (scales of the virtual space) is much larger than N (the scales of the nodes).



## A Quick Comparison between Chord and S2

Chord is a protocol at application layer while S2 is at network year. But this will not prevent us to compare them at the simulation level.

As for routing efficiency, they both provide a decent performance. Their average routing length paths scale logarithmically with nodes scaling. From the simulation results (Fig. 1 and Fig. 5), we can find that S2 performs better than chord in the 250 node-topology case. Intuitively, S2 node can find the least-cost path quickly from different virtual spaces it's in.

The size of the finger/routing tables of them are fixed. Chord maintains a linear tables which is a set of pointers and its size is log2(size of name space). S2 maintains a set of vectors, which are the coordinates of neighbor nodes in different spaces. The size of this table scales exponentially when the stored hops scales. The search efficiency of Chord are much better. Chord was designed so because the node leaves and node joins occur frequently in P2P scenario. While in data center, the use case of S2, the topology is much more stable, so its complexity of tables is acceptable.

### _Reference_
[1] Yu, Y., & Qian, C. (2016). Space Shuffle: A Scalable, Flexible, and High-Performance Data Center Network. IEEE Transactions on Parallel and Distributed Systems, 27(11), 3351–3365. https://doi.org/10.1109/tpds.2016.2533618

[2] Stoica, I., Morris, R., Karger, D., Kaashoek, M. F., & Balakrishnan, H. (2001). Chord. In Proceedings of the 2001 conference on Applications, technologies, architectures, and protocols for computer communications - SIGCOMM ’01. ACM Press. https://doi.org/10.1145/383059.383071
