from zeroconf import ServiceBrowser, Zeroconf

class EnphaseEnvoyListener:
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def update_service(self, zeroconf, type, name):
        print("Service %s updated" % (name,))

zeroconf = Zeroconf()
listener = EnphaseEnvoyListener()
browser = ServiceBrowser(zeroconf, "_enphase-envoy._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
