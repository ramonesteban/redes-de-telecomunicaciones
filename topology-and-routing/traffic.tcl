set ns [new Simulator]
$ns namtrace-all [open out.nam w]

set topology [lindex $argv 0]
set traffic_app [lindex $argv 1]

proc finish {} {
    exec nam out.nam &
    exit 0
}

set first [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]
set n7 [$ns node]

proc star {} {
	global ns first n1 n2 n3 n4 n5 n6 n7
	$ns duplex-link $first $n1 2.5Mb 10ms DropTail
	$ns duplex-link $first $n2 2Mb 10ms DropTail
	$ns duplex-link $first $n3 2Mb 10ms DropTail
	$ns duplex-link $first $n4 1.5Mb 10ms DropTail
	$ns duplex-link $first $n5 1.5Mb 10ms DropTail
	$ns duplex-link $first $n6 1.5Mb 10ms DropTail
	$ns duplex-link $first $n7 1.5Mb 10ms DropTail
}

proc line {} {
	global ns first n1 n2 n3 n4 n5 n6 n7
	$ns duplex-link $first $n1 2.5Mb 10ms DropTail
	$ns duplex-link $n1 $n2 2Mb 10ms DropTail
	$ns duplex-link $n2 $n3 2Mb 10ms DropTail
	$ns duplex-link $n3 $n4 1.5Mb 10ms DropTail
	$ns duplex-link $n4 $n5 1.5Mb 10ms DropTail
	$ns duplex-link $n5 $n6 1.5Mb 10ms DropTail
	$ns duplex-link $n6 $n7 1.5Mb 10ms DropTail
}

proc random {} {
	global ns first n1 n2 n3 n4 n5 n6 n7
	$ns duplex-link $first $n1 2.5Mb 10ms DropTail
	$ns duplex-link $first $n2 2.5Mb 10ms DropTail
	$ns duplex-link $n1 $n2 2Mb 10ms DropTail
	$ns duplex-link $n1 $n4 2Mb 10ms DropTail
	$ns duplex-link $n2 $n5 1.5Mb 10ms DropTail
	$ns duplex-link $n5 $n4 1.5Mb 10ms DropTail
	$ns duplex-link $n4 $n3 1.5Mb 10ms DropTail
	$ns duplex-link $n3 $n6 1.5Mb 10ms DropTail
	$ns duplex-link $n3 $n4 1.5Mb 10ms DropTail
	$ns duplex-link $n6 $n7 1.5Mb 10ms DropTail
	$ns duplex-link $n7 $n4 1.5Mb 10ms DropTail
}

global ns first n6 n7
set tcp [new Agent/TCP]
$ns attach-agent $first $tcp
set sink [new Agent/TCPSink]
$ns attach-agent $n6 $sink
$ns connect $tcp $sink
set tcp2 [new Agent/TCP]
$ns attach-agent $first $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n7 $sink2
$ns connect $tcp2 $sink2
set ftp [new Application/FTP]
$ftp attach-agent $tcp
set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2
set udp [new Agent/UDP]
$ns attach-agent $first $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null

if {$topology == "star"} {
	star
} elseif {$topology == "line"} {
	line
} else {
	random
}

if {$traffic_app == "exponential"} {
	set traffic [new Application/Traffic/Exponential]
	$traffic attach-agent $udp
	$traffic set packetSize_ 1024
	$traffic set rate_ 1
	$traffic set burst_time_ 500ms
	$traffic set idle_time_ 50ms
} elseif {$traffic_app == "pareto"} {
	set traffic [new Application/Traffic/Pareto]
	$traffic attach-agent $udp
    $traffic set packetSize_ 1024
    $traffic set rate_ 1
    $traffic set burst_time_ 500ms
    $traffic set idle_time_ 50ms
    $traffic set shape_ 1.5
} else {
	set traffic [new Application/Traffic/CBR]
	$traffic attach-agent $udp
	$traffic set packetSize_ 1024
	$traffic set rate_ 1
	$traffic set type_ CBR
	$traffic set random_ true
}

$ns at 0.05 "$traffic start"
$ns at 0.10 "$ftp start"
$ns at 0.50 "$ftp2 start"
$ns at 1.4 "$ftp stop"
$ns at 1.8 "$ftp2 stop"
$ns at 2.0 "$traffic stop"
$ns at 2.0 "finish"
$ns run
