import socket, time

NBYTES = 42
PORT = 9999
HOST = 'localhost'

def init():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.connect((HOST, PORT))
    host, port = udp_socket.getsockname()
    print 'Client at', host, 'in port', port
    start_server(udp_socket)

def start_server(udp_socket):
    while True:
        udp_socket.send('READY')
        packet = udp_socket.recv(NBYTES)
        h_orig, h_dest, p_orig, p_dest, res, data = get_packet_data(packet)
        if is_prime(int(data)):
            res = 1
            print int(data), "is prime"
        else:
            res = 0
            print int(data), "isn't prime"
        packet = create_packet(1, h_dest, h_orig, p_dest, p_orig, res, data)
        print 'Packet to send:', packet
        print '-----------'
        udp_socket.send(packet)
        time.sleep(3)

def is_prime(n):
    prime = True
    for div in range(2, n):
        if n % div == 0:
            prime = False
    return prime

def get_packet_data(packet):
    if len(packet) == NBYTES:
        type_from = packet[0]
        ho = packet[1:13]
        hd = packet[13:25]
        port_origin = packet[25:30]
        port_destination = packet[30:35]
        res = packet[35]
        data = packet[36:42]
        host_origin = str(int(ho[0:3]))+'.'+str(int(ho[3:6]))+'.'+str(int(ho[6:9]))+'.'+str(int(ho[9:12]))
        host_destination = str(int(hd[0:3]))+'.'+str(int(hd[3:6]))+'.'+str(int(hd[6:9]))+'.'+str(int(hd[9:12]))
        return (host_origin, host_destination, port_origin, port_destination, res, data)

def create_packet(t, host_origin, host_destination, port_origin, port_destination, r, num):
    ho = host_origin.split('.')
    host_origin = ho[0].zfill(3)+ho[1].zfill(3)+ho[2].zfill(3)+ho[3].zfill(3)

    hd = host_destination.split('.')
    host_destination = hd[0].zfill(3)+hd[1].zfill(3)+hd[2].zfill(3)+hd[3].zfill(3)

    port_origin = str(port_origin).zfill(5)
    port_destination = str(port_destination).zfill(5)
    return str(t)+host_origin+host_destination+port_origin+port_destination+str(r)+str(num)

def main():
    init()

if __name__ == '__main__':
    main()

