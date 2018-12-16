#!/bin/bash
#
#  shaper.sh
#  ---------
#  A utility script for traffic shaping using tc
#
#  Usage
#  -----
#  shape.sh start - starts the shaper
#  shape.sh stop - stops the shaper
#  shape.sh restart - restarts the shaper
#  shape.sh show - shows the rules currently being shaped
#
#  AUTHORS
#  -------
#  Aaron Blankstein
#  Jeff Terrace
#  Minghao Xie
#
#  Original script written by: Scott Seong
#  Taken from URL: http://www.topwebhosts.org/tools/traffic-control.php
#

source config

help() {
    echo "Usage: start|stop|restart|show"
    echo "e.g. start tbf"
}

start() {
    OP=$1
    case $OP in

    "tbf")
        $TC qdisc add dev $IF root handle 1:0 tbf rate $RATE burst $BURST latency $LATENCY peakrate $PEAKRATE mtu 2000
        $TC qdisc add dev $IF parent 1:1 handle 10: netem delay $LATENCY $JITTER
    ;;

    "sfq")
        $TC qdisc add dev $IF root handle 1: sfq perturb $PTB
    ;;

    "prio")
        $TC qdisc add dev $IF root handle 1: prio
        $TC qdisc add dev $IF parent 1:1 handle 10: sfq 
        $TC qdisc add dev $IF parent 1:2 handle 20: tbf rate $RATE buffer 1600 limit 3000 
        $TC qdisc add dev $IF parent 1:3 handle 30: sfq
    ;;

    "red")
        $TC qdisc add dev $IF parent 1:1 handle 10: red limit $LIMIT min $MIN max $MAX avpkt $AVGPKT burst $BURST ecn adaptive bandwidth $BW
    ;;

    "htb")
        echo "please, this function is not ready"
        exit 0
        $TC qdisc add dev $IF root handle 1: htb default 30 
        $TC class add dev $IF parent 1: classid 1:1 htb rate $HRATE_0 burst $BURST
        $TC class add dev $IF parent 1:1 classid 1:10 htb rate $HRATE_1 burst $BURST
        $TC class add dev $IF parent 1:1 classid 1:20 htb rate $HRATE_2 ceil $CEIL burst $BURST 
        $TC class add dev $IF parent 1:1 classid 1:30 htb rate $HRATE_3 ceil $CEIL burst $BURST 
        $TC qdisc add dev $IF parent 1:10 handle 10: sfq perturb $PTB
        $TC qdisc add dev $IF parent 1:20 handle 20: sfq perturb $PTB
        $TC qdisc add dev $IF parent 1:30 handle 30: sfq perturb $PTB
        U32="tc filter add dev $IF protocol ip parent 1:0 prio 1 u32"
        $U32 match ip dport 80 0xffff flowid 1:10 
        $U32 match ip sport 25 0xffff flowid 1:20
    ;;

    "test")
        echo "nothing happens, no worries"
    ;;

    *)
        help
    ;;
    esac
}

stop() {
    OP=$1
    case $OP in

    "tbf")
        $TC qdisc del dev $IF root
        $TC qdisc del dev $IF parent 1:1
    ;;
    "sfq")
        $TC qdisc del dev $IF root
    ;;
    "prio")
        echo "FIXME: no implementation yet"
    ;;
    "htb")
	echo "FIXME: no implementation yet"
    ;;
    *)
        echo "Did you run start before?"
    ;;
    esac
}

restart() {
    stop
    sleep 1
    start
}

show() {
    $TC -s qdisc ls dev $IF
}

case "$1" in

start)

echo -n "Starting bandwidth shaping: "
start $2
echo "done"
;;

stop)

echo -n "Stopping bandwidth shaping: "
stop $2
echo "done"
;;

restart)

echo -n "Restarting bandwidth shaping: "
restart
echo "done"
;;

show)

echo "Bandwidth shaping status for $IF:"
show
echo ""
;;

*)
help
;;

esac 
exit 0
