## Naive Benchmark to Linux Traffic Shaping

### Test Environment:

Receiver: Ubuntu 16.04.05, kernel 4.14.34, aarch64, 100GbE

Sender: Ubuntu 17.10, kernel 4.18.0-rc4+, x86_64, 100GbE

### Benchmark tools:
* neper
* iperf3
* (ping)

### TCP Options:
* Congestion control: renoO/cubic
* Max pacing rate
* Min retransmission timeout (RTO)
* Listen backlog
* TCP small queue (TSQ)

### Well-known algorithms:
1. Classless shaping:

* PFIFO/BFIFO (Packet/Byte FIFO, pfifo_fast in high speed ports) - Linux default 
* SFQ（Stochastic Fairness Queueing)
* RED (Random Early Drop)

2. Classful QDisc:

* TBF (Token Bucket Filter) - pure shaper, no need to simulate without filters
* HFSC (Hierarchical Fair Service Curve)
* PRIO (Priority Scheduler)
* HTB (Hierarchical Token Bucket)
* CBQ (Class Based Queueing)


### Filters
* classifier
* policer

### Experiments

1. Network performance v.s. Burstiness/Flows
2. Memory Cost v.s. Flows
3. Implementation cost v.s. Performance improvements


### References
[1] [kernel flow](https://wiki.linuxfoundation.org/networking/kernel_flow)

[2] [Traffic Control HOWTO](http://www.tldp.org/en/Traffic-Control-HOWTO/)

[3] [Queueing in the Linux Network Stack](https://www.linuxjournal.com/content/queueing-linux-network-stack)
