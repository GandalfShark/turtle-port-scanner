# port scanner adapted from python for pentesters on Tryhackme.com
# https://tryhackme.com/room/pythonforcybersecurity
import sys
import socket as s
import random
from time import sleep
print("""
-------------------------
   Turtle Scan: Beta
now with 0% real turtles
-------------------------\n""")
ip = input("Target IP: ")
open_ports = []
ports = [p for p in range(1, 65536)]

rand = input("randomise? Y/N: ").strip().lower()
if rand == 'y':
    random.shuffle(ports)
    #print(ports)

slow = input("slow ride? Y/N: ").strip().lower()
if slow == 'y':
    print('maybe go make some coffee, this will take a while...")    


def probe(ip, port, result = 1):
    try:
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        #print(sock)
        sock.settimeout(0.5)
        tup = (ip, port)
        r = sock.connect_ex(tup)
        if r == 0:
            result = r
        sock.close()
    except Exception as e:
        pass
    return result



for port in ports:
    if slow == 'y':
        sleep(random.randint(5,12))
    response = probe(ip, port)
    print(f"{response} : port# {port}")
    if response == 0: 
        open_ports.append(port)
    sys.stdout.flush()    

if open_ports:
    print("PORTS OPEN: ")
    print(sorted(open_ports))

else:
    print("boo-urns! No open ports.")
