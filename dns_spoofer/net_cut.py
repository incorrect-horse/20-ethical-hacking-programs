#net_cut
import netfilterqueue


def process_packet(packet):
    packet.drop()
    return


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
