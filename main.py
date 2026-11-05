import socket
import requests
import os
from colorama import init, Fore, Style

# Colorama initialize karna
init(autoreset=True)

def banner():
    # Termux ke system command se website open/redirect karna
    try:
        url = "https://pythontechdev.netlify.app"
        os.system(f"am start -a android.intent.action.VIEW -d {url} > /dev/null 2>&1")
    except Exception:
        pass

    print(Fore.CYAN + Style.BRIGHT + """
      █████╗ ████████╗██████╗ 
     ██╔══██╗╚══██╔══╝██╔══██╗
     ███████║   ██║   ██║  ██║
     ██╔══██║   ██║   ██║  ██║
     ██║  ██║   ██║   ██████╔╝
     ╚═╝  ╚═╝   ╚═╝   ╚═════╝ 
    """)
    print(Fore.YELLOW + Style.BRIGHT + "========================================")
    print(Fore.GREEN + Style.BRIGHT + "       ADVANCED RECON & TOOL (ATD)      ")
    print(Fore.YELLOW + Style.BRIGHT + "========================================")
    print(Fore.MAGENTA + Style.BRIGHT + "Powered by **Akhil**\n")

def get_ip(target):
    try:
        ip = socket.gethostbyname(target)
        print(Fore.GREEN + f"[+] Target IP: {ip}")
        return ip
    except Exception as e:
        print(Fore.RED + f"[-] Error resolving IP: {e}")
        return None

def scan_ports(target_ip):
    print(Fore.CYAN + "\n[+] Scanning common ports...")
    ports = [21, 22, 80, 443, 8080, 8443]
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                print(Fore.GREEN + f"    Port {port}: OPEN")
            s.close()
        except:
            pass

def check_subdomains(target):
    print(Fore.CYAN + "\n[+] Checking subdomains...")
    subdomains = ["www", "mail", "test", "admin", "api", "shop"]
    for sub in subdomains:
        url = f"http://{sub}.{target}"
        try:
            response = requests.get(url, timeout=2)
            if response.status_code < 400:
                print(Fore.GREEN + f"    Found: {url}")
        except:
            pass

def get_content(target):
    print(Fore.CYAN + "\n[+] Fetching website content info...")
    url = f"http://{target}"
    try:
        res = requests.get(url, timeout=3)
        print(Fore.GREEN + f"    Status Code: {res.status_code}")
        print(Fore.GREEN + f"    Server: {res.headers.get('Server', 'Unknown')}")
    except Exception as e:
        print(Fore.RED + f"[-] Could not fetch content: {e}")

def cam_finder(target_ip):
    print(Fore.CYAN + "\n[+] Scanning for IP Cameras / DVR streams...")
    # Common CCTV, RTSP, and Camera ports
    cam_ports = {
        554: "RTSP (Real-Time Streaming Protocol)",
        8080: "HTTP Proxy / Web Cam Panel",
        37777: "Dahua DVR / IP Camera",
        8000: "Hikvision DVR / IP Camera",
        8888: "IP Camera Streaming Port"
    }
    
    found_cam = False
    for port, desc in cam_ports.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))
            if result == 0:
                found_cam = True
                print(Fore.YELLOW + Style.BRIGHT + f"[!] ALERT: Camera Port Detected -> Port {port} ({desc})")
            s.close()
        except:
            pass
            
    if found_cam:
        print(Fore.RED + Style.BRIGHT + "\n[+] Status: Yeh IP ek Security Camera ya DVR ki lag rahi hai!")
    else:
        print(Fore.GREEN + "[+] Status: Koi typical camera port open nahi mila.")

if __name__ == "__main__":
    banner()
    target = input(Fore.YELLOW + "Enter target domain or IP (e.g., example.com): " + Style.RESET_ALL)
    if target:
        ip = get_ip(target)
        if ip:
            scan_ports(ip)
            check_subdomains(target)
            get_content(target)
            cam_finder(ip)
