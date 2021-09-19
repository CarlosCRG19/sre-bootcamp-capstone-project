import re # for regular exression operations

def cidr_mask_conversion_handler(value, iscidr=True):
    """
    Assigns the method that will be used for conversion and
    returns a dictionary with the function info
    """
    if iscidr:
        fun, inp, out = cidr_to_mask(value)
    else:
        fun, inp, out = mask_to_cidr(value)

    return {
        "function": fun,
        "input": inp,
        "output": out,
    }

def cidr_to_mask(cidr):
    """
    Receives the number of the CIDR (as string) and returns the 
    netmask associated with it.
    """

    if str(cidr).isnumeric() is False or int(cidr) <= 0:
        return "Invalid"

    cidr = int(cidr)

    full_octects = cidr // 8
    incomplete_octet = cidr % 8
    
    netmask = ["255"]*full_octects + ["0"]*(4-full_octects)

    incomplete_pow = 8 - incomplete_octet
    netmask[full_octects] = str(256 - pow(2, incomplete_pow))

    return "cidrToMask", cidr, ".".join(netmask)


def mask_to_cidr(netmask):
    """
    Receives a netmask as an string and returns the count of 1's in its bit 
    representation (CIDR)
    """

    if is_valid_ipv4(netmask) is False:
        return "Invalid"

    cidr = 0

    octects = netmask.split(".")
    for octect in octects:
        octect_as_bin = bin(int(octect))
        cidr += octect_as_bin.count("1") 

    return "maskToCidr", netmask, str(cidr)

def is_valid_ipv4(ip_address):
    """
    Uses regex to validate the syntax of an ip address. It also handles 
    non-routable adresses
    """

    # 0.0.0.0 adress is non-routable and 255.255.255.255 is reserved for broadcast address
    if ip_address in ("0.0.0.0", "255.255.255.255"):
        return False

    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    return re.search(regex, ip_address) 
