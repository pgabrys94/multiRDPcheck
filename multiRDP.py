import subprocess


def multiple_sessions_check():
    file = r"C:\Windows\system32\termsrv.dll"
    patch = "B80001000089813806000090"

    with open(file, "rb") as f:
        code = f.read().hex().upper()

    return patch in code


def send_to_zabbix(content):
    zabbix_sender_path = r"C:\zabbix_agent2-6.4.0-windows-amd64-openssl-static\bin\zabbix_sender.exe"
    zabbix_agent_config = r"C:\zabbix_agent2-6.4.0-windows-amd64-openssl-static\bin\zabbix_agent2.conf"
    zabbix_host = "DANE-OPTIMA"

    pskid = None
    pskfile = None

    with open(r"C:\zabbix_agent2-6.4.0-windows-amd64-openssl-static\bin\zabbix_agent2.conf", "r") as f:
        for line in f:
            if "TLSPSKIdentity=" in line:
                pskid = line.replace("TLSPSKIdentity=", "").strip()
            if "TLSPSKFile=" in line:
                pskfile = line.replace("TLSPSKFile=", "").strip()

    subprocess.run([zabbix_sender_path, "-z", "node4.koag.pl", "-p", "10051", "-s", zabbix_host, "--tls-connect", "psk",
                    "-k", "RDP.multi.check", "--tls-psk-identity", pskid, "--tls-psk-file", pskfile, "-o", str(content),
                    "-c", zabbix_agent_config])


send_to_zabbix(multiple_sessions_check())
