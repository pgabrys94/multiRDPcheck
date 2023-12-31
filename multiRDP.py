import subprocess
import os


def multiple_sessions_check():

    with open(file, "rb") as f:
        code = f.read().hex().upper()

    return patch in code


def send_to_zabbix(content):

    zabbix_host = None
    pskid = None
    pskfile = None
    zabbix_server = None
    zabbix_port = "10051"

    with open("zabbix_agent2.conf", "r") as f:
        for line in f:
            if "TLSPSKIdentity=" in line:
                pskid = line.replace("TLSPSKIdentity=", "").strip()
            if "TLSPSKFile=" in line:
                pskfile = line.replace("TLSPSKFile=", "").strip()
            if "Hostname=" in line:
                zabbix_host = line.replace("Hostname=", "").strip()
            if "ServerActive=" in line:
                if ":" in line and line.split(":")[1].isdigit():
                    zabbix_server, zabbix_port = line.split(":")
                    zabbix_server = zabbix_server.replace("ServerActive=", "").strip()
                elif ":" in line and not line.split(":")[1].isdigit():
                    zabbix_server = line.split(":")[0].replace("ServerActive=", "").strip()
                else:
                    zabbix_server = line.replace("ServerActive=", "").strip()

    subprocess.run([zabbix_sender_path, "-z", zabbix_server, "-p", zabbix_port, "-s", zabbix_host, "--tls-connect",
                    "psk", "-k", "RDP.multi.check", "--tls-psk-identity", pskid, "--tls-psk-file", pskfile, "-o",
                    str(content), "-c", zabbix_agent_config])


file = r"C:\Windows\system32\termsrv.dll"
patch = "B80001000089813806000090"
zabbix_sender_path = "zabbix_sender.exe"
zabbix_agent_config = "zabbix_agent2.conf"

if os.path.exists(zabbix_sender_path) and os.path.exists(zabbix_agent_config):
    if os.name == "nt":
        send_to_zabbix(multiple_sessions_check())
    else:
        print("This program works only in Windows NT systems.")
else:
    print("Cannot found 'zabbix sender.exe' or config file.")
    print("Those files (including this .exe) must be in the same directory.")
