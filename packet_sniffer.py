#!/usr/bin/python3
# https://github.com/EONRaider/Packet-Sniffer

__author__ = 'EONRaider @ keybase.io/eonraider'

import abc
import argparse
import time
from itertools import count
import struct, fcntl 
from socket import ntohs, socket, PF_PACKET, SOCK_RAW, AF_INET, SOCK_STREAM, inet_ntoa

import protocols

i = ' ' * 4  # Basic indentation level

class PacketSniffer(object):
    def __init__(self, interface: str):
        self.interface = interface
        self.data = None
        self.protocol_queue = ['Ethernet']
        self.__observers = list()

    def register(self, observer):
        self.__observers.append(observer)

    def __notify_all(self, *args):
        for observer in self.__observers:
            observer.update(*args)
        del self.protocol_queue[1:]

    def execute(self):
        self.sock = sock = socket(PF_PACKET, SOCK_RAW, ntohs(0x0003))
        if self.interface is not None:
            sock.bind((self.interface, 0))
        for self.packet_num in count(1):
            start: int = 0
            raw_packet = sock.recv(140)
            for proto in self.protocol_queue:
                proto_class = getattr(protocols, proto)
                end: int = start + proto_class.header_len
                protocol = proto_class(raw_packet[start:end])
                setattr(self, proto.lower(), proto_class)
                if protocol.encapsulated_proto is None:
                    break
                self.protocol_queue.append(protocol.encapsulated_proto)
                start = end
            return
            self.data = raw_packet[end:]
            self.__notify_all(self)

    def _execute(self):
        self.execute()
        sb = struct.pack("256s", bytes(self.sock.getsockname()[0], encoding="utf8"))
        addr = inet_ntoa(fcntl.ioctl(self.sock.fileno(), 0x8915, sb)[20:24])

        with socket(AF_INET, SOCK_STREAM) as s:
            s.bind((addr, 8006))
            s.listen()
            conn, addr = s.accept()
            self.data = conn.recv(1024) + self.sock.recv(1024)
           

class OutputMethod(abc.ABC):
    """Interface for the implementation of all classes responsible for
    further processing and/or output of the information gathered by
    the PacketSniffer class (referenced as 'subject')."""

    def __init__(self, subject):
        subject.register(self)

    @abc.abstractmethod
    def update(self, *args, **kwargs):
        pass


class SniffToScreen(OutputMethod):
    def __init__(self, subject, *, displaydata: bool):
        super().__init__(subject)
        self.p = None
        self.display_data = displaydata

    def update(self, packet):
        self.p = packet
        self._display_output_header()
        self._display_packet_info()
        self._display_packet_contents()

    def _display_output_header(self):
        local_time = time.strftime('%H:%M:%S', time.localtime())
        print('[>] Packet #{0} at {1}:'.format(self.p.packet_num, local_time))

    def _display_packet_info(self):
        for proto in self.p.protocol_queue:
            getattr(self, '_display_{}_data'.format(proto.lower()))()

    def _display_ethernet_data(self):
        print('{0}[+] MAC {1:.>23} -> {2}'.format(i, self.p.ethernet.source,
                                                  self.p.ethernet.dest))

    def _display_ipv4_data(self):
        print('{0}[+] IPv4 {1:.>22} -> {2: <15} | '
              'PROTO: {3} TTL: {4}'.format(i, self.p.ipv4.source,
                                           self.p.ipv4.dest,
                                           self.p.ipv4.encapsulated_proto,
                                           self.p.ipv4.ttl))

    def _display_ipv6_data(self):
        print('{0}[+] IPv6 {1:.>22} -> {2: <15}'.format(i, self.p.ipv6.source,
                                                        self.p.ipv6.dest))

    def _display_arp_data(self):
        if self.p.arp.oper == 1:  # ARP Request
            print('{0}[+] ARP Who has {1: >13} ? '
                  '-> Tell {2}'.format(i, self.p.arp.target_proto,
                                       self.p.arp.source_proto))
        else:                     # ARP Reply
            print('{0}[+] ARP {1:.>23} -> '
                  'Is at {2}'.format(i, self.p.arp.source_proto,
                                     self.p.arp.source_hdwr))

    def _display_tcp_data(self):
        print('{0}[+] TCP {1:.>23} -> {2: <15} | '
              'Flags: {3} > {4}'.format(i, self.p.tcp.sport,
                                        self.p.tcp.dport,
                                        self.p.tcp.flag_hex,
                                        self.p.tcp.flag_txt))

    def _display_udp_data(self):
        print('{0}[+] UDP {1:.>23} -> {2}'.format(i, self.p.udp.sport,
                                                  self.p.udp.dport))

    def _display_icmp_data(self):
        print('{0}[+] ICMP {1:.>22} -> {2: <15} | '
              'Type: {3}'.format(i, self.p.ipv4.source,
                                 self.p.ipv4.dest,
                                 self.p.icmp.type_txt))

    def _display_packet_contents(self):
        if self.display_data is True:
            print('{0}[+] DATA:'.format(i))
            data = self.p.data.decode(errors='ignore').\
                replace('\n', '\n{0}'.format(i*2))
            print('{0}{1}'.format(i, data))


def sniff(interface: str, displaydata: bool):
    """Control the flow of execution of the Packet Sniffer tool."""

    packet_sniffer = PacketSniffer(interface)
    to_screen = SniffToScreen(subject=packet_sniffer,
                              displaydata=displaydata)
    try:
        print('\n[>>>] Sniffer initialized. Waiting for incoming packets. '
              'Press Ctrl-C to abort...\n')

        packet_sniffer._execute()
        print(packet_sniffer.data)

    except KeyboardInterrupt:
        raise SystemExit('Aborting packet capture...')


if __name__ == '__main__':
    sniff(interface="enp7s0",
    displaydata=False)
