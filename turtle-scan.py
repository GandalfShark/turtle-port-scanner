# port scanner adapted from python for pentesters on Tryhackme.com
# https://tryhackme.com/room/pythonforcybersecurity
import sys
import socket as s
import random
from time import sleep
from argparse import ArgumentParser


print("""
-------------------------
   Turtle Scan: Beta
now with 0% real turtles
-------------------------\n""")

# parse cli args
parser = ArgumentParser(prog="Turtle Scan")
parser.add_argument('--src-ip', '-s', dest='src_ip', help='Source IP addr to spoof')
parser.add_argument('--target-ip', '-t', dest='target_ip', help='Target IP addr')
args = parser.parse_args()


class TurtleScanner:
    def __init__(self):
        self.open_ports = []
        self.ports = [p for p in range(1, 65536)]
        self.slow = False  # check this in setup()
        self.src_ip = args.src_ip
        self.target_ip = args.target_ip

    def setup(self):
        """get user input - target IP, ports, random, etc"""
        if not self.target_ip:
            # get target ip if not passed in as CLI arg
            self.target_ip = input("Target IP: ")
        rand = input("randomise? Y/N: ").strip().lower()
        if rand == 'y':
            random.shuffle(self.ports)
            #print(ports)
        self.slow = input("slow ride? Y/N: ").strip().lower()
        if self.slow == 'y':
             print("maybe go make some coffee, this will take a while...")

    def probe(self, port, result=1):
        try:
            sock = s.socket(s.AF_INET, s.SOCK_STREAM)
            # print(f'{sock=}')
            # if user passed in a value for src_ip
            if self.src_ip:
                # bind socket to spoofed IP. port 0 selects unused port
                sock.bind((self.src_ip, 0))
            sock.settimeout(0.5)
            tup = (self.target_ip, port)
            r = sock.connect_ex(tup)
            if r == 0:
                result = r
            sock.close()
        except Exception as e:
            pass
        return result

    def scan_ports(self):
        for port in self.ports:
            if self.slow == 'y':
                sleep(random.randint(5,12))
            response = self.probe(port)
            print(f"{response} : port# {port}")
            if response == 0:
                self.open_ports.append(port)
            sys.stdout.flush()

        if self.open_ports:
            print("PORTS OPEN: ")
            print(sorted(self.open_ports))
        else:
             print("boo-urns! No open ports.")



def main():
    t = TurtleScanner()
    t.setup()
    t.scan_ports()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.\n")
