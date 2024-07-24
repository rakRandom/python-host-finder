from host_finder import HostFinder


def run():
    hostf = HostFinder()
    hostf.scan_network()
    print(*hostf.get_addresses(), sep="\n")


if __name__ == "__main__":
    run()
