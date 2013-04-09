set ns [new Simulator]
$ns color 1 Blue
$ns color 2 Red

set file1 [open out.tr w]
$ns trace-all $file1
set file2 [open out.nam w]
$ns namtrace-all $file2

proc finish {} {
    global ns file1 file2
    $ns flush-trace
    close $file1
    close $file2
    exec nam out.nam &
    exit 0
}

# configure unicast protocol
$ns rtproto DV

set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]
set n7 [$ns node]
set n8 [$ns node]

# links between the nodes
$ns duplex-link $n0 $n1 0.3Mb 10ms DropTail
$ns duplex-link $n1 $n2 0.3Mb 10ms DropTail
$ns duplex-link $n2 $n3 0.3Mb 10ms DropTail
$ns duplex-link $n1 $n4 0.3Mb 10ms DropTail
$ns duplex-link $n3 $n5 0.5Mb 10ms DropTail
$ns duplex-link $n4 $n5 0.5Mb 10ms DropTail
$ns duplex-link $n0 $n6 0.2Mb 10ms DropTail
$ns duplex-link $n6 $n7 0.2Mb 10ms DropTail
$ns duplex-link $n7 $n8 0.5Mb 10ms DropTail
$ns duplex-link $n8 $n5 0.5Mb 10ms DropTail

# node position
$ns duplex-link-op $n0 $n1 orient right
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient up-left
$ns duplex-link-op $n1 $n4 orient up-left
$ns duplex-link-op $n3 $n5 orient left
$ns duplex-link-op $n4 $n5 orient left-up
$ns duplex-link-op $n0 $n6 orient left
$ns duplex-link-op $n6 $n7 orient up
$ns duplex-link-op $n7 $n8 orient up-left
$ns duplex-link-op $n8 $n5 orient right-up

set tcp [new Agent/TCP/Newreno]
$ns attach-agent $n0 $tcp
set sink [new Agent/TCPSink/DelAck]
$ns attach-agent $n5 $sink
$ns connect $tcp $sink
$tcp set fid_ 1

set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP

$ns rtmodel-at 0.7 down $n1 $n4
$ns rtmodel-at 1.5 down $n1 $n2
$ns rtmodel-at 2.5 up $n1 $n4
$ns at 0.1 "$ftp start"
$ns at 3.0 "finish"

$ns run
