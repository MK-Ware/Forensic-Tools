import sys
try:
    from _winreg import *
except:
    from winreg import *
try:
    from common_methods import *
except ImportError:
    sys.exit("Could not find common_methods.py... download the full toolkit from https://github.com/MonroCoury/Forensic_Tools")


def val2addr(val):
    if val:
        addr = ""
        for char in val:
            try:
                addr += ("%02x " % ord(char))
            except:
                addr += ("%02x " % ord(chr(char)))
        addr = addr.strip(" ").replace(" ", ":")[:17]
        return True, addr
    else:
        addr = "No data found for this network"
        return False, addr

def get_WIFIs():
    wlans = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList' \
            + r'\Signatures\Unmanaged'
    key = OpenKey(HKEY_LOCAL_MACHINE, wlans)
    data = ""
    num = 0
    for i in range(1000000):
        try:
            attempt = EnumKey(key, i)
            wlan_key = OpenKey(key, str(attempt))
            (n, addr, t) = EnumValue(wlan_key, 5)
            (n, name, t) = EnumValue(wlan_key, 4)
            res, mac_address = val2addr(addr)
            wlan_name = str(name)
            data += "<tr><td>%s</td><td>%s</td></tr>" % (wlan_name,  mac_address)
            CloseKey(wlan_key)
            num += 1
        except Exception as e:
            break
    complete_html = init_data("wlan_reader Wifi Networks", num) + init_table_header("./templates/init_wlan_html.html") \
                    + data + close_table_html()
    saveResult("Wifi_History.html", complete_html)

if __name__ == "__main__":
    print('\n\n    ##############A Python script to read WIFI activity #####################')
    print('    #              Mac Address can be used to determin the location         #')
    print('    #              of the wireless network with the help of online          #')
    print('    #              databases like wigle or skyhook, a feature I\'m           #')
    print('    #     planning on adding to this script to save you the effort          #')
    print('    #            Make sure you run command prompt as administrator          #')
    print('    #                      Coded by monrocoury                              #')
    print('    #########################################################################\n\n')
    print("Working...\n")
    get_WIFIs()
