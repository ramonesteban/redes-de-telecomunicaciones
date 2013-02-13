import socket, time, thread, random

NBYTES = 42
PORT = 9999
HOST = 'localhost'
data_buffer = []
datalock = thread.allocate_lock()

def init():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, PORT))
    host, port = udp_socket.getsockname()
    print 'Server listening at', host, 'in port', port
    start_server(udp_socket)

def unpack_data(good):
    while True:
        time.sleep(1)
        if len(data_buffer) > 0:
            datalock.acquire()
            packet = data_buffer.pop()
            h_orig, h_dest, p_orig, p_dest, res, data = get_packet_data(packet)
            print h_orig, h_dest, p_orig, p_dest, res, data
            datalock.release()

def start_server(udp_socket):
    thread.start_new_thread(unpack_data, (True, ))
    while True:
        data, address = udp_socket.recvfrom(NBYTES)
        if data == 'READY':
            host_origin, port_origin = udp_socket.getsockname()
            host_destination, port_destination = address
            num = int(random.uniform(100000, 999999))
            packet = create_packet(0, host_origin, host_destination, port_origin, port_destination, 0, num)
            udp_socket.sendto(packet, address)

            packet, address = udp_socket.recvfrom(NBYTES)
            datalock.acquire()
            data_buffer.append(packet)
            datalock.release()

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

