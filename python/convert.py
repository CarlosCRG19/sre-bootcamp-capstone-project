import re

class CidrMaskConvert:
    def cidr_to_mask(self, cidr):

        if cidr.isnumeric() == False or int(cidr) <= 0:
            return "Invalid"

        cidr = int(cidr)

        full_octects = cidr // 8
        incomplete_octet = cidr % 8
        
        netmask = ["255"]*full_octects + ["0"]*(4-full_octects)

        incomplete_pow = 8 - incomplete_octet
        netmask[full_octects] = str(256 - pow(2, incomplete_pow))

        return ".".join(netmask)


    def mask_to_cidr(self, netmask):

        validator = IpValidate()
        if not validator.is_ipv4(netmask):
            return "Invalid"

        cidr = 0

        octects = netmask.split(".")
        for octect in octects:
            octect_as_bin = bin(int(octect))
            cidr += octect_as_bin.count("1")

        return str(cidr)

class IpValidate:
    def is_ipv4(self, ip_address):

        if ip_address == "0.0.0.0" or ip_address == "255.255.255.255":
            return False

        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        return re.search(regex, ip_address)
