# 🐍 PyARPPoisoner (ARPSpoofer.py)

## 📜 Description

**PyARPPoisoner** (or another name of your choosing, e.g., `ARPSpoofer.py`) is a Python tool designed to perform **ARP Poisoning attacks** on a **Local Area Network (LAN)**. This tool is developed specifically for **network security education**, **penetration testing**, and **ethical hacking** scenarios.

**ARP Poisoning** is a type of **Man-in-the-Middle (MITM)** attack where an attacker manipulates the ARP caches of other devices on the network, causing them to route traffic through the attacker's machine. This tool automates this process by manipulating the ARP tables of both the target device and the network gateway.

> ⚠️ **Legal Disclaimer:**  
This tool should only be used within **legal and ethical boundaries**. Any unauthorized use against networks or devices, other than for educational and testing purposes on your own network or in environments where you have **explicit authorization**, is strictly prohibited and may lead to legal consequences. The developer cannot be held responsible for the misuse of this tool.

---

## ✨ Features

- 🔥 **ARP Poisoning:** Automatically poisons the ARP caches of both the target device and the network gateway.
- 🔀 **IP Forwarding:** Automatically enables IP forwarding on the operating system for MITM attacks.
- 🔍 **Automatic MAC Address Resolution:** Automatically discovers the physical (MAC) addresses of the target and gateway.
- ♻️ **Graceful Exit:** Upon termination (`Ctrl + C`), the program restores the ARP tables to their original state to ensure normal network operation.
- 🧠 **Command-Line Arguments:** Offers easy-to-use `-t` (target IP) and `-g` (gateway IP) options.

---

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```
### 2️⃣ Install Required Libraries
```bash
This tool uses the Scapy library to interact with network packets. You can install it using the following command:

pip install scapy
# or
pip3 install scapy
```

## 🚀 Usage
To run the tool, you need to specify the target IP address and the gateway IP address.
The tool requires sudo/root privileges as it needs access to raw sockets.

```bash
sudo python3 arp_spoof.py -t <TARGET_IP_ADDRESS> -g <GATEWAY_IP_ADDRESS>
```

Example:
If your target IP address is 192.168.1.105 and your gateway IP address is 192.168.1.1, run:

```bash
sudo python3 arp_spoof.py -t 192.168.1.105 -g 192.168.1.1
```

While the program is running, it will display the number of packets sent.
When you stop it with Ctrl + C, it will restore the ARP tables to their original state.

## ⚙️ How It Works

Enabling IP Forwarding:
At the start, the program enables IP forwarding on Linux systems via /proc/sys/net/ipv4/ip_forward to allow the attacker's machine to route traffic between the target and the gateway.

MAC Address Resolution:
The get_mac_address() function uses Scapy's ARP requests to find the MAC addresses for the specified IP addresses.

ARP Poisoning:
The arp_poison() function crafts spoofed ARP replies:

To the target, it claims the attacker's MAC address belongs to the gateway's IP.

To the gateway, it claims the attacker's MAC address belongs to the target's IP.

These are sent continuously to poison the ARP caches.

Packet Forwarding:
Since IP forwarding is enabled, all traffic between the target and the gateway passes through the attacker's machine.

ARP Restoration:
When the program is interrupted with Ctrl + C, the restore_arp() function sends legitimate ARP replies using the correct MAC addresses to both the target and the gateway, restoring the network to its normal state.
