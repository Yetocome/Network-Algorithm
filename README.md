# Introduction
This repository is created for simple simulations of well-known networking algorithms.

I will post some of my simulation results here. My simulation focus is on routing and caching efficiency (Routing path length and routing tables cost). The simulation scale is small restricted by my laptop performance, there would be some error statistically.

## Chord Protocol<sup>[[1]](https://dl.acm.org/citation.cfm?id=383071)</sup>
Chord protocol is one of the most famous protocols in P2P networking.



Routing Path Length

* Experiment 1 - fixed condition
* Experiment 2 - when node number scales


Finger Tables:

* Experiment 1 - fixed condition
* Experiment 2 - when file scales


## Space Shuffle<sup>[[2]](http://ieeexplore.ieee.org/document/7416229/)</sup>

Space Shuffle provides a new solution for data center networks.

Routing Path Length:

* Experiment 1 - fixed condition

![](https://github.com/Yetocome/Networking-Algorithm/blob/master/Figure_1.png)
* Experiment 2 - when node number scales

![](https://github.com/Yetocome/Networking-Algorithm/blob/master/Figure_2.png)
* Experiment 3 - when stored hops scales

![](https://github.com/Yetocome/Networking-Algorithm/blob/master/Figure_3.png)
* Experiment 4 - when available spaces scales

![](https://github.com/Yetocome/Networking-Algorithm/blob/master/Figure_4.png)
* Experiment 5 - when used spaces scales

Routing Tables:


## A Quick Comparison between Chord and S2

### _Reference_
[1] Stoica, I., Morris, R., Karger, D., Kaashoek, M. F., & Balakrishnan, H. (2001). Chord. In Proceedings of the 2001 conference on Applications, technologies, architectures, and protocols for computer communications - SIGCOMM ’01. ACM Press. https://doi.org/10.1145/383059.383071

[2] Yu, Y., & Qian, C. (2016). Space Shuffle: A Scalable, Flexible, and High-Performance Data Center Network. IEEE Transactions on Parallel and Distributed Systems, 27(11), 3351–3365. https://doi.org/10.1109/tpds.2016.2533618
