import socket
import threading


# Ports specified to be verified
SCAN_PORTS = [
    80, 
    8000, 
    8080, 
    2024  # Custom port
]


class HostFinder():
    def __init__(self) -> None:
        self.__result: list[dict[str, str, int]] = list()

    # Function to verify if an IP is active and responding at the specified port
    def check_host(self, ip: str, port: int) -> None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            error = sock.connect_ex((ip, port))
            if error == 0:
                self.__result.append((f"{ip}:{port}", ip, port))
            sock.close()
        except:
            pass

    # Function to obtain the base IP of the network
    def get_base_ip(self) -> str:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        ip_parts = local_ip.split('.')
        base_ip = '.'.join(ip_parts[:-1])
        return base_ip

    # Main function to scan the network
    def scan_network(self) -> list[dict[str, str, int]]:
        self.__result = list()
        base_ip = self.get_base_ip()
        threads = []

        for i in range(1, 255):
            ip = f"{base_ip}.{i}"
            for port in SCAN_PORTS:
                t = threading.Thread(target=self.check_host, args=(ip, port))
                threads.append(t)
                t.start()
        
        for t in threads:
            t.join()
        
        return self.__result

    # Function to get formatted addresses
    def get_addresses(self) -> list[str] | list[None]:
        if not self.__result:
            return []
        return [element[0] for element in self.__result]
