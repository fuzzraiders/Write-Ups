# Metapress — HTB Write‑Up

> **Category:** Web / Linux  
> **Focus:** Enumeration → SQLi → XXE → Credential Abuse → Privilege Escalation

---

## Enumeration

![Description](images/image 1.png)

Initial enumeration shows **ports 21, 22, and 80** open. Browsing to port 80 redirects to `http://metapress.htb`, so we add it to `/etc/hosts`:

```bash
sudo nano /etc/hosts
```

---

## Web Analysis

![Description](images/image 1.png)

The web application is running **WordPress**, with the versions visible in the page information. At this stage, no useful public exploits were available for the detected WordPress core version.

The login page exposes **public credentials**, but multiple SQL injection attempts against the login functionality failed.

---

## Finding a Potential Attack Surface

![image](images/image 1.png)

While browsing the site, an **Events** feature stood out — a section that allows users to add and view events. Features like this are often backed by plugins and can introduce vulnerabilities.

To investigate further, the page source was inspected.

![Description](images/image 1.png)

This revealed the plugin:

**BookingPress version 1.0.10**

---

## Exploitation — BookingPress SQL Injection

![Description](images/image 1.png)

BookingPress **v1.0.10** is vulnerable to **SQL Injection**. Using a public exploit tool available online, database access was achieved.

![Description](images/image 1.png)

Two hashed passwords were extracted from the database. Using **Hashcat** with the **rockyou** wordlist, one hash was successfully cracked:

```
manager : partylikearockstar
```

---

## Exploitation — WordPress XXE

A known exploit exists for **WordPress 5.6.2**, involving **XXE via media upload**. The vulnerability allows an attacker to upload a malicious media file containing an XXE payload.

Relevant references:

- First link
- Second link

![Description](images/image 1.png)

### XXE Attack Flow

1. A malicious **`.wav`** file is crafted and uploaded.
2. WordPress attempts to parse the WAV file.
3. The parser fails to properly sanitize XML input.
4. The server fetches and executes a remote **evil.dtd** file.

![Description](images/image 1.png)

### evil.dtd

![Description](images/image 1.png)

The `evil.dtd` file executes and returns sensitive files in encoded form.

![Description](images/image 1.png)

Using the same technique, sensitive configuration files were retrieved.

![Description](images/image 1.png)

---

## Credential Reuse

Using the extracted credentials, SSH access was attempted first — unsuccessfully. The same credentials were then tested against **FTP**, which worked.

![Description](images/image 1.png)

Additional credentials were discovered and reused.

---

## SSH Access

![Description](images/image 1.png)

SSH access was obtained. While enumerating the user’s home directory, a hidden file named **`.passpie`** was discovered.

---

## Privilege Escalation — Passpie

### What is Passpie?

Passpie is a **password manager** that stores credentials encrypted using **PGP keys**.

To read the stored passwords, an export operation is required — which prompts for a password.

![Description](images/image 1.png)

![Description](images/image 1.png)

The `.keys` directory was copied locally. Since the files are PGP‑encrypted, they were converted using **pgp2john**.

![Description](images/image 1.png)

After cracking the key, the passwords were successfully exported.

---

## Root Access

Using the recovered credentials:

```bash
su root
```

```
Password: p7qfAZt4_A1xo_0x
```

Root shell achieved 🎯

---

## Final Notes

Thanks for reading! This is part of our **CPTS → OSCP** learning series.
Feel free to drop a comment, feedback, or questions below. See you in the next write‑up 🚀
