set ns [new Simulator -multicast on]
$ns color 1 Red
$ns color 30 Purple
$ns color 31 Green

set f [open out.tr w]
$ns trace-all $f
$ns namtrace-all [open out.nam w]

proc finish {} {
    global ns
    $ns flush-trace
    exec nam out.nam &
    exit 0
}

set group [Node allocaddr]
for {set i 0} {$i <= 6} {incr i} {
    set n($i) [$ns node]
}

# links between the nodes
$ns duplex-link $n(1) $n(0) 0.5Mb 10ms DropTail 
$ns duplex-link $n(2) $n(0) 0.3Mb 10ms DropTail
$ns duplex-link $n(3) $n(0) 0.5Mb 10ms DropTail
$ns duplex-link $n(4) $n(0) 0.3Mb 10ms DropTail
$ns duplex-link $n(5) $n(0) 0.5Mb 10ms DropTail
$ns duplex-link $n(6) $n(0) 0.3Mb 10ms DropTail

# configure multicast protocol
BST set RP_($group) $n(0)
$ns mrtproto BST

set udp1 [new Agent/UDP]
set udp2 [new Agent/UDP]
$ns attach-agent $n(1) $udp1
$ns attach-agent $n(2) $udp2

set src1 [new Application/Traffic/CBR]
$src1 attach-agent $udp1
$udp1 set dst_addr_ $group
$udp1 set dst_port_ 1
$src1 set random_ false

set src2 [new Application/Traffic/CBR]
$src2 attach-agent $udp2
$udp2 set dst_addr_ $group
$udp2 set dst_port_ 2
$src2 set random_ false

set rcvr [new Agent/LossMonitor]

$ns at 0.4 "$src1 start"
$ns at 0.6 "$n(3) join-group $rcvr $group"
$ns at 1.3 "$n(4) join-group $rcvr $group"
$ns at 1.6 "$n(5) join-group $rcvr $group"
$ns at 1.9 "$n(4) leave-group $rcvr $group"
$ns at 2.0 "$src2 start"
$ns at 2.3 "$n(6) join-group $rcvr $group"
$ns at 3.5 "$n(3) leave-group $rcvr $group"
$ns at 4.0 "finish"

$ns run
