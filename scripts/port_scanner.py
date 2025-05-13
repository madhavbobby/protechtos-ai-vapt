import nmap

def basic_port_scan(target_ip):
    scanner = nmap.PortScanner()
    print(f"🔎 Scanning {target_ip} for open ports...")
    scanner.scan(target_ip, '1-1024')  # Scans ports 1 to 1024

    for host in scanner.all_hosts():
        print(f"📍 Host: {host}")
        print(f"📶 State: {scanner[host].state()}")
        
        for proto in scanner[host].all_protocols():
            print(f"--- Protocol: {proto}")

            ports = scanner[host][proto].keys()
            for port in ports:
                print(f"     Port: {port} | State: {scanner[host][proto][port]['state']}")

if __name__ == "__main__":
    target = input("🔎 Enter a target IP address: ")
    basic_port_scan(target)