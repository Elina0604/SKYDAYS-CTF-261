#!/usr/bin/env python3
"""
Brooklyn Nine Nine Themed PCAP Traffic Generator for CTF
Generates realistic network traffic with hidden flags
"""

from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse, HTTP
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.l2 import Ether
import base64
import random
import time


class B99TrafficGenerator:
    def __init__(self, output_file="b99_challenge.pcap"):
        self.output_file = output_file
        self.packets = []

        # Brooklyn Nine Nine themed IPs and hostnames
        self.characters = {
            "jake.precinct99.local": "192.168.99.1",
            "amy.precinct99.local": "192.168.99.2",
            "holt.precinct99.local": "192.168.99.3",
            "gina.precinct99.local": "192.168.99.4",
            "charles.precinct99.local": "192.168.99.5",
            "rosa.precinct99.local": "192.168.99.6",
            "terry.precinct99.local": "192.168.99.7",
            "scully.precinct99.local": "192.168.99.8",
            "hitchcock.precinct99.local": "192.168.99.9",
            "server.precinct99.local": "192.168.99.100",
            "evidence.precinct99.local": "192.168.99.101",
        }

        self.seq_num = random.randint(1000, 9999)
        self.sport = random.randint(50000, 60000)

    def _get_seq(self):
        """Generate sequential sequence numbers"""
        self.seq_num += random.randint(1, 100)
        return self.seq_num

    def _get_sport(self):
        """Generate sequential source ports"""
        self.sport += 1
        return self.sport

    def add_dns_traffic(self):
        """Add DNS queries with hidden clues"""
        print("[+] Adding DNS traffic...")

        # Normal DNS queries
        queries = [
            "www.google.com",
            "www.nypd.gov",
            "evidence-system.gov",
            "mail.precinct99.local",
        ]

        for query in queries:
            pkt = (
                IP(dst="8.8.8.8", src=self.characters["jake.precinct99.local"])
                / UDP(sport=self._get_sport(), dport=53)
                / DNS(rd=1, qd=DNSQR(qname=query))
            )
            self.packets.append(pkt)
            time.sleep(0.01)

        # Hidden flag in DNS TXT query
        # The flag will be: B99{NINE_NINE}
        secret_query = "gina-secret-backup.precinct99.local"
        pkt = (
            IP(dst="8.8.8.8", src=self.characters["gina.precinct99.local"])
            / UDP(sport=self._get_sport(), dport=53)
            / DNS(rd=1, qd=DNSQR(qname=secret_query, qtype="TXT"))
        )
        self.packets.append(pkt)

        # DNS response with encoded flag
        flag_encoded = base64.b64encode(b"B99{NINE_NINE}").decode()
        response = (
            IP(src="8.8.8.8", dst=self.characters["gina.precinct99.local"])
            / UDP(sport=53, dport=self.sport)
            / DNS(
                qr=1,
                aa=1,
                qd=DNSQR(qname=secret_query, qtype="TXT"),
                an=DNSRR(rrname=secret_query, type="TXT", rdata=flag_encoded),
            )
        )
        self.packets.append(response)

    def add_http_traffic(self):
        """Add HTTP traffic with hidden data"""
        print("[+] Adding HTTP traffic...")

        # Normal HTTP requests
        normal_requests = [
            ("GET", "/index.html", "jake.precinct99.local"),
            ("GET", "/login", "amy.precinct99.local"),
            ("POST", "/api/cases", "holt.precinct99.local"),
        ]

        for method, path, host in normal_requests:
            # TCP SYN
            syn = IP(
                src=self.characters[host],
                dst=self.characters["server.precinct99.local"],
            ) / TCP(sport=self._get_sport(), dport=80, flags="S", seq=self._get_seq())
            self.packets.append(syn)

            # TCP SYN-ACK
            synack = IP(
                src=self.characters["server.precinct99.local"],
                dst=self.characters[host],
            ) / TCP(
                sport=80,
                dport=self.sport,
                flags="SA",
                seq=self._get_seq(),
                ack=syn.seq + 1,
            )
            self.packets.append(synack)

            # TCP ACK
            ack = IP(
                src=self.characters[host],
                dst=self.characters["server.precinct99.local"],
            ) / TCP(
                sport=self.sport,
                dport=80,
                flags="A",
                seq=syn.seq + 1,
                ack=synack.seq + 1,
            )
            self.packets.append(ack)

            # HTTP Request
            http_req = (
                IP(
                    src=self.characters[host],
                    dst=self.characters["server.precinct99.local"],
                )
                / TCP(
                    sport=self.sport,
                    dport=80,
                    flags="PA",
                    seq=syn.seq + 1,
                    ack=synack.seq + 1,
                )
                / f"{method} {path} HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Brooklyn99/1.0\r\n\r\n".encode()
            )
            self.packets.append(http_req)

        # Hidden flag in HTTP POST data
        # Jake uploading "evidence" - flag part 2: {TITLE_OF_YOUR_SEX_TAPE}
        sport = self._get_sport()
        seq = self._get_seq()

        syn = IP(
            src=self.characters["jake.precinct99.local"],
            dst=self.characters["evidence.precinct99.local"],
        ) / TCP(sport=sport, dport=80, flags="S", seq=seq)
        self.packets.append(syn)

        synack = IP(
            src=self.characters["evidence.precinct99.local"],
            dst=self.characters["jake.precinct99.local"],
        ) / TCP(sport=80, dport=sport, flags="SA", seq=self._get_seq(), ack=seq + 1)
        self.packets.append(synack)

        ack = IP(
            src=self.characters["jake.precinct99.local"],
            dst=self.characters["evidence.precinct99.local"],
        ) / TCP(sport=sport, dport=80, flags="A", seq=seq + 1, ack=synack.seq + 1)
        self.packets.append(ack)

        post_data = "case_id=9901&evidence_type=document&secret_note=Qjk5e1RJVExFX09GX1lPVVJfU0VYX1RBUEV9&officer=jake"
        # Qjk5e1RJVExFX09GX1lPVVJfU0VYX1RBUEV9 is base64 for B99{TITLE_OF_YOUR_SEX_TAPE}

        http_post = (
            IP(
                src=self.characters["jake.precinct99.local"],
                dst=self.characters["evidence.precinct99.local"],
            )
            / TCP(sport=sport, dport=80, flags="PA", seq=seq + 1, ack=synack.seq + 1)
            / f"POST /upload HTTP/1.1\r\nHost: evidence.precinct99.local\r\n"
            f"Content-Type: application/x-www-form-urlencoded\r\n"
            f"Content-Length: {len(post_data)}\r\n\r\n{post_data}".encode()
        )
        self.packets.append(http_post)

    def add_icmp_traffic(self):
        """Add ICMP traffic with hidden message"""
        print("[+] Adding ICMP traffic...")

        # Normal pings
        for i in range(5):
            ping = (
                IP(src=self.characters["terry.precinct99.local"], dst="8.8.8.8")
                / ICMP(type=8, code=0, id=random.randint(1, 65535), seq=i)
                / Raw(load=b"Terry loves yogurt!")
            )
            self.packets.append(ping)

            pong = (
                IP(src="8.8.8.8", dst=self.characters["terry.precinct99.local"])
                / ICMP(type=0, code=0, id=ping[ICMP].id, seq=i)
                / Raw(load=b"Terry loves yogurt!")
            )
            self.packets.append(pong)

        # Hidden message in ICMP data
        # Flag part 3: {COOL_COOL_COOL_NO_DOUBT}
        secret_message = "Qjk5e0NPT0xfQ09PTF9DT09MX05PX0RPVUJUX30="  # base64
        ping = (
            IP(
                src=self.characters["jake.precinct99.local"],
                dst=self.characters["rosa.precinct99.local"],
            )
            / ICMP(type=8, code=0, id=9999, seq=99)
            / Raw(load=secret_message.encode())
        )
        self.packets.append(ping)

        pong = (
            IP(
                src=self.characters["rosa.precinct99.local"],
                dst=self.characters["jake.precinct99.local"],
            )
            / ICMP(type=0, code=0, id=9999, seq=99)
            / Raw(load=b"NOICE")
        )
        self.packets.append(pong)

    def add_ftp_traffic(self):
        """Add FTP traffic with file transfer containing flag"""
        print("[+] Adding FTP traffic...")

        ftp_server = self.characters["server.precinct99.local"]
        ftp_client = self.characters["charles.precinct99.local"]
        sport = self._get_sport()

        # FTP Control Connection
        syn = IP(src=ftp_client, dst=ftp_server) / TCP(
            sport=sport, dport=21, flags="S", seq=self._get_seq()
        )
        self.packets.append(syn)

        synack = IP(src=ftp_server, dst=ftp_client) / TCP(
            sport=21, dport=sport, flags="SA", seq=self._get_seq(), ack=syn.seq + 1
        )
        self.packets.append(synack)

        ack = IP(src=ftp_client, dst=ftp_server) / TCP(
            sport=sport, dport=21, flags="A", seq=syn.seq + 1, ack=synack.seq + 1
        )
        self.packets.append(ack)

        # FTP Banner
        banner = (
            IP(src=ftp_server, dst=ftp_client)
            / TCP(
                sport=21, dport=sport, flags="PA", seq=synack.seq + 1, ack=syn.seq + 1
            )
            / Raw(load=b"220 Precinct99 FTP Server\r\n")
        )
        self.packets.append(banner)

        # USER command
        user_cmd = (
            IP(src=ftp_client, dst=ftp_server)
            / TCP(
                sport=sport,
                dport=21,
                flags="PA",
                seq=syn.seq + 1,
                ack=banner.seq + len(banner[Raw].load),
            )
            / Raw(load=b"USER charles\r\n")
        )
        self.packets.append(user_cmd)

        # PASS command with hidden hint
        pass_cmd = (
            IP(src=ftp_client, dst=ftp_server)
            / TCP(
                sport=sport,
                dport=21,
                flags="PA",
                seq=user_cmd.seq + len(user_cmd[Raw].load),
            )
            / Raw(load=b"PASS B99{HOT_DAMN!}\r\n")
        )  # Flag part 4
        self.packets.append(pass_cmd)

        # Login success
        login_ok = (
            IP(src=ftp_server, dst=ftp_client)
            / TCP(sport=21, dport=sport, flags="PA")
            / Raw(load=b"230 User logged in\r\n")
        )
        self.packets.append(login_ok)

        # RETR command - retrieving a file with flag
        retr_cmd = (
            IP(src=ftp_client, dst=ftp_server)
            / TCP(sport=sport, dport=21, flags="PA")
            / Raw(load=b"RETR holt_secret_recipe.txt\r\n")
        )
        self.packets.append(retr_cmd)

    def add_telnet_traffic(self):
        """Add Telnet session with hidden commands"""
        print("[+] Adding Telnet traffic...")

        telnet_server = self.characters["server.precinct99.local"]
        telnet_client = self.characters["holt.precinct99.local"]
        sport = self._get_sport()
        seq = self._get_seq()

        # TCP Handshake
        syn = IP(src=telnet_client, dst=telnet_server) / TCP(
            sport=sport, dport=23, flags="S", seq=seq
        )
        self.packets.append(syn)

        synack = IP(src=telnet_server, dst=telnet_client) / TCP(
            sport=23, dport=sport, flags="SA", seq=self._get_seq(), ack=syn.seq + 1
        )
        self.packets.append(synack)

        ack = IP(src=telnet_client, dst=telnet_server) / TCP(
            sport=sport, dport=23, flags="A", seq=syn.seq + 1, ack=synack.seq + 1
        )
        self.packets.append(ack)

        # Telnet login sequence
        commands = [
            b"login: holt\r\n",
            b"password: cheddar123\r\n",
            b"ls -la\r\n",
            b"cat flag.txt\r\n",
            b"B99{VINDICATION!}\r\n",  # Flag part 5
            b"exit\r\n",
        ]

        for cmd in commands:
            pkt = (
                IP(src=telnet_client, dst=telnet_server)
                / TCP(sport=sport, dport=23, flags="PA", seq=seq)
                / Raw(load=cmd)
            )
            self.packets.append(pkt)
            seq += len(cmd)
            time.sleep(0.05)

    def add_noise_traffic(self):
        """Add random noise traffic to make it more challenging"""
        print("[+] Adding noise traffic...")

        for _ in range(20):
            src = random.choice(list(self.characters.values()))
            dst = random.choice(list(self.characters.values()))

            if src != dst:
                # Random TCP traffic
                pkt = (
                    IP(src=src, dst=dst)
                    / TCP(
                        sport=random.randint(1024, 65535),
                        dport=random.choice([80, 443, 8080, 22, 3306]),
                        flags=random.choice(["S", "A", "PA", "F"]),
                    )
                    / Raw(load=RandString(random.randint(10, 100)))
                )
                self.packets.append(pkt)

    def generate(self):
        """Generate all traffic and save to PCAP"""
        print(f"[*] Generating Brooklyn Nine Nine themed PCAP challenge...")
        print(f"[*] Output file: {self.output_file}\n")

        # Add different types of traffic
        self.add_dns_traffic()
        self.add_http_traffic()
        self.add_icmp_traffic()
        self.add_ftp_traffic()
        self.add_telnet_traffic()
        self.add_noise_traffic()

        # Shuffle packets to make it more realistic
        random.shuffle(self.packets)

        # Write to PCAP file
        wrpcap(self.output_file, self.packets)

        print(f"\n[+] PCAP file generated successfully!")
        print(f"[+] Total packets: {len(self.packets)}")
        print(f"[+] File: {self.output_file}")

        # Print challenge information
        self.print_challenge_info()

    def print_challenge_info(self):
        """Print challenge description and hints"""
        print("\n" + "=" * 60)
        print("BROOKLYN NINE NINE CTF CHALLENGE")
        print("=" * 60)
        print("""
Challenge: "The Case of the Missing Files"

Captain Holt's important files have been compromised! 
Your mission is to analyze the network traffic dump from 
Precinct 99 and find all the hidden flags.

There are 5 flags hidden in different protocols:
1. DNS - Look for Gina's secret backup
2. HTTP - Jake uploaded evidence with a secret note
3. ICMP - Cool, cool, cool... check the ping data
4. FTP - Charles' password might be interesting
5. Telnet - Captain Holt's command history

Each flag follows the format: B99{SOMETHING}

HINTS:
- Use Wireshark filters: dns, http, icmp, ftp, telnet
- Check for base64 encoded strings
- Follow TCP streams
- Examine packet payloads carefully
- NINE-NINE!

Good luck, detective!
""")
        print("=" * 60)


def main():
    # Check if scapy is installed
    try:
        import scapy
    except ImportError:
        print("[!] Error: scapy not installed")
        print("[!] Install with: pip install scapy")
        return

    # Generate the PCAP
    generator = B99TrafficGenerator("b99_challenge.pcap")
    generator.generate()

    print("\n[*] You can now analyze the PCAP with:")
    print("    wireshark b99_challenge.pcap")
    print("    or")
    print("    tshark -r b99_challenge.pcap")


if __name__ == "__main__":
    main()
