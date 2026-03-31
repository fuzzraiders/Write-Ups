![header](assets/badges/fuzzraiders-Member.svg)

# Android Static Analysis — Deep Dive Into Application Reversal & Attack Surface Mapping

**Category:** Mobile Security / Static Analysis
**Difficulty:** Beginner → Advanced
**Platform:** Mobile Security Learning

---

This module provides a comprehensive introduction to **Android Static Analysis**, demonstrating how modern mobile applications can be reverse engineered, analyzed, and exploited **without execution**, focusing on:

* APK reverse engineering and resource extraction
* Deep analysis of AndroidManifest.xml attack surface
* Identification of hardcoded secrets and insecure logic
* Enumeration of cloud infrastructure (AWS S3 & Firebase)
* Combining manual and automated analysis for full coverage

---

## 🛠 Tools

Advanced static analysis using real-world tooling.

```bash
apktool        → decompiling APK resources & manifest
jadx-gui       → reconstructing Java/Kotlin source code
MobSF          → automated static + security analysis
strings        → extracting embedded data
grep           → pattern matching for secrets
awscli         → enumerating S3 buckets
curl           → interacting with exposed endpoints
```

---

## 📌 Overview

Android applications often expose critical information through their internal structure. Static analysis allows security professionals to **map the entire attack surface before execution**, reducing risk and increasing efficiency.

By analyzing APK contents, it is possible to uncover:

* hidden application logic
* insecure configurations
* exposed endpoints
* sensitive credentials

This module emphasizes a **methodology-driven approach**, where analysis moves from **structure → logic → data → infrastructure**.

---

## 🔍 APK Acquisition & Reverse Engineering

The first phase involves acquiring and unpacking the APK.

```bash
apktool d target.apk -o app_decoded
```

**Figure 1 — Decompiled APK structure showing resources and manifest**

![Image](https://futurestud.io/blog/content/images/2015/09/Screen-Shot-2015-09-22-at-8-22-36-AM.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A704/1%2A7X9BRqPq8TXQFSkRu55xHA.png)

![Image](https://user-images.githubusercontent.com/118523/142730720-839f017e-38db-423e-b53f-39f5f0a0316f.png)

This reveals:

* `AndroidManifest.xml`
* `res/` resources
* `smali/` bytecode representation
* compiled assets and configurations

---

## 📄 AndroidManifest.xml — Attack Surface Mapping

The manifest defines the application’s exposed components and permissions.

Key areas analyzed:

* `android:exported="true"` → exposed components
* dangerous permissions (`READ_EXTERNAL_STORAGE`, `INTERNET`)
* activities, services, broadcast receivers
* intent filters

**Figure 2 — AndroidManifest.xml analysis of exported components**

![Image](https://global.discourse-cdn.com/ionicframework/original/3X/b/a/bad8898258f8604d8460eee5e87c8c5ad5c73b52.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1200/1%2ANnEiB2eaEID3P3pknf5MFw.png)

Misconfigured manifests can lead to:

* unauthorized component access
* privilege escalation paths
* inter-application attacks

---

## 🧠 Source Code Reconstruction & Manual Analysis

Using `jadx`, the application is reconstructed into readable Java/Kotlin code.

```bash
jadx-gui target.apk
```

Focus areas:

* authentication flows
* API calls
* hidden features
* debug logic

**Figure 3 — Decompiled Java/Kotlin code inside JADX**

![Image](https://user-images.githubusercontent.com/118523/142730720-839f017e-38db-423e-b53f-39f5f0a0316f.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1400/1%2Ad-PaO0ladfaFXjWtLLRZqQ.png)

![Image](https://appsecsanta.com/images/tools/jadx/jadx-gui.webp)

Manual analysis provides context that automated tools cannot detect.

---

## 🔑 Hardcoded Secrets & Sensitive Data Discovery

One of the most critical vulnerabilities in mobile apps is **hardcoded secrets**.

Detection techniques:

```bash
strings target.apk | grep -Ei "key|token|secret|password"
```

Common findings:

* API keys
* JWT tokens
* database URLs
* private endpoints

**Figure 4 — Extracted API keys and endpoints from APK**


![Image](https://i.sstatic.net/cWOSEmpg.png)

![Image](https://www.security.com/_next/image?q=75\&url=https%3A%2F%2Fwww.security.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fblogs_inline_medium%2Fpublic%2F2024-10%2Ffig2-5146.png.webp%3Fitok%3DpzcklJ1X+1x\&w=828)

Impact:

➡️ Direct backend compromise without authentication

---

## 🚩 Practical Analysis — Injured Android (Flags 1–4)

The **Injured Android** lab demonstrates real-world vulnerable patterns.

Through static analysis:

* flags were identified inside application logic
* insecure implementations were mapped
* hidden vulnerabilities were uncovered

This reinforces how real applications leak sensitive data through poor coding practices.

---

## ☁️ Cloud Infrastructure Enumeration

Static analysis often reveals backend infrastructure.

---

### AWS S3 Bucket Enumeration

Discovered bucket references can be tested:

```bash
aws s3 ls s3://target-bucket
```

**Figure 5 — Public AWS S3 bucket exposure**

![Image](https://blogs.perficient.com/files/2019/08/awscli-30.png)

![Image](https://miro.medium.com/v2/resize%3Afit%3A1286/0%2A7zR8o6FiVcAMlXfi.png)

Risks:

* data leakage
* file exposure
* sensitive asset disclosure

---

### Firebase Database Enumeration

Firebase endpoints are often embedded:

```bash
curl https://target.firebaseio.com/.json
```

**Figure 6 — Firebase database exposed data**

![Image](https://i.sstatic.net/ljcse.png)


![Image](https://firebase.google.com/static/docs/rules/images/playground-test.png)

Risks:

* full database access
* user data exposure
* write permissions exploitation

---

## ⚙️ Automated Analysis with MobSF

MobSF automates large parts of static analysis.

```bash
docker run -it -p 8000:8000 mobsf/mobsf
```

**Figure 7 — MobSF analysis dashboard**

![Image](https://user-images.githubusercontent.com/4301109/76472502-1f6df700-63cc-11ea-9ac0-fca99327e47d.png)





Capabilities:

* vulnerability classification
* permission analysis
* API discovery
* security scoring

---

## 🔥 Full Attack Surface Chain

1. APK extraction
2. Manifest analysis
3. Code reconstruction
4. Secret discovery
5. Cloud endpoint enumeration
6. Automated validation

➡️ Result: Full visibility into application + backend exposure

---

## 🧠 What This Module Teaches

* Static analysis methodology for Android apps
* Identifying vulnerabilities without execution
* Extracting sensitive data from binaries
* Mapping backend infrastructure from client-side artifacts
* Combining manual and automated analysis techniques

This builds a strong foundation for:

* Android pentesting
* mobile bug bounty hunting
* reverse engineering workflows

---

## 🎓 Module Completion

After completing all labs and analysis stages, the **Android Static Analysis module** was successfully completed.

This directly contributes to:

* Mobile Security expertise
* Android vulnerability research
* Real-world application analysis skills

---

## 📌 Conclusion

Android applications often expose critical weaknesses before execution.

Static analysis enables security professionals to:

* understand application logic
* identify vulnerabilities early
* uncover backend infrastructure

This module reinforces a key principle:

> **If you can read the app, you can break the app.**
![disclaimer](assets/badges/fuzzraiders-disclaimer.svg)


![owner](assets/badges/fuzzraiders-Ownership.svg)