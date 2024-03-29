#Snippet entnommen von dieser Seite https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/28950776#28950776
#Dieser Code ermittelt die lokale IP-Adresse des Rechners, die dann vom Server genutzt wird
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
