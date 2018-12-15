## Naive Benchmark to Linux Traffic Shaping

### Test Environment:

Sender: Ubuntu 16.04, kernel 4.4.0, x86_64

Receiver: Ubuntu 17.10, kernel 4.18.0-rc4+, x86_64

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

### Available shaping algorithms:
* pfifo/bfifo (fast)
* tbf
* sfq
* prio
* htb
* red
* cbq

### Filters
* classifier
* policer

### Experiments

1. Network performance v.s. Burstiness/Flows
2. Implementation cost v.s. Performance improvements
3. Buffer utilization v.s. Flows


### References
[1] https://www.linuxjournal.com/content/july-2013-issue-linux-journal-networking

[2] http://www.tldp.org/en/Traffic-Control-HOWTO/
