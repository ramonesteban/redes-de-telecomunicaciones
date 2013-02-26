import sys, os

def ping_test(host, count):
    test = 'ping ' + host + ' -c ' + str(count) + ' -s 120 -Q 0x10 -n > ping.dat'
    os.system(test)

    f = open('ping.dat', 'r')
    lines = f.readlines()

    times_list = list()
    n = 1
    while n < len(lines):
        if lines[n] == '\n':
            break
        else:
            current_line = lines[n].split(' ')
            text, time = current_line[6].split('=')
            times_list.append(float(time))
            n += 1

    percentage = (1 - len(times_list)/float(count))*100.0
    average = sum(times_list)/len(times_list)
    sqrt = list()
    for num in times_list:
        dif = (average - num)**2
        sqrt.append(dif)
    jitter = sum(sqrt)/count
    return len(times_list), count, percentage, max(times_list), min(times_list), average, jitter

def bandwidth_test():
    test = 'bmon -p eth1 -o "ascii:noheader;quitafter=11" > bmon.dat'
    os.system(test)

    f = open('bmon.dat', 'r')
    lines = f.readlines()

    bandwidth = list()
    for line in lines:
        current_line = line.split(' ')
        data = list()
        for splited in current_line:
            if splited != '':
                data.append(splited)
        bandwidth.append(float(data[1][:-3]))
    return sum(bandwidth)/len(bandwidth)

def complete_test(host, count):
    pacs_received, pacs_sended, percentage, max_time, min_time, average, jitter = ping_test(host, count)
    bandwidth_used = bandwidth_test()

    print 'Packets sended:', pacs_sended
    print 'Packets received:', pacs_received
    print 'Lost percentage: %0.1f' % percentage
    print 'Max time: %0.1f ms' % max_time
    print 'Min time: %0.1f ms' % min_time
    print 'Latency: %0.2f ms' % average
    print 'Jitter: %0.2f ms' % jitter
    print 'Bandwith used: %0.2f KiB/s' % bandwidth_used

def main():
    try:
        host = str(sys.argv[1])
        count = int(sys.argv[2])
    except:
        host = 'www.ustream.tv'
        count = 100
    complete_test(host, count)

if __name__ == '__main__':
    main()

