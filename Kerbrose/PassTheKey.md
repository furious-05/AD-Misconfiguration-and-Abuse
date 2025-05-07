# 🔐 Pass-the-Key Attack Guide

## Overview
Pass-the-Key (PtK) is an attack technique in Active Directory (AD) environments that exploits the Kerberos authentication protocol. By obtaining a user's cryptographic key (DES, RC4, AES-128, or AES-256), an attacker can request a Ticket Granting Ticket (TGT) without needing the user's password. This TGT can then be used to obtain Service Tickets (STs) for accessing resources, enabling user impersonation.

## How It Works
1. **Kerberos Pre-Authentication**:
   - Kerberos requires users to provide a secret key (derived from their password) during pre-authentication to obtain a TGT.
   - If an attacker has this key, they can request a TGT from the Key Distribution Center (KDC) without the password.
2. **Key Types**:
   - Kerberos supports DES, RC4, AES-128, and AES-256 keys.
   - RC4 key is equivalent to the NTLM hash (NT hash) when RC4 is enabled.
3. **Requesting a TGT**:
   - Tools like Impacket's `getTGT.py` can use a key (e.g., NT hash or AES key) to request a TGT.
   - The TGT is saved as a `.ccache` file for use in further attacks (e.g., pass-the-ticket).
4. **Accessing Resources**:
   - The TGT is used to obtain STs for accessing services, allowing the attacker to impersonate the user.

## Pass-the-Key vs. Pass-the-Hash
- **Pass-the-Hash (PtH)**:
  - Uses the NT hash (RC4 key) to request a TGT, known as "overpass-the-hash."
  - Limited to environments where RC4 encryption is enabled.
- **Pass-the-Key (PtK)**:
  - Uses any Kerberos key type (DES, RC4, AES-128, AES-256).
  - Works even if RC4 is disabled, making it more versatile.
  - "Overpass-the-hash" is a subset of PtK when using the RC4 key.
- **Key Difference**:
  - PtH relies on the NT hash; PtK can use any Kerberos key.
  - PtK is applicable in modern AD environments with stronger encryption (AES).

## Practical Examples
Using Impacket's `getTGT.py` to request a TGT:
```bash
# Pass-the-Hash (using NT hash)
getTGT.py -hashes :NThash $DOMAIN/$USER@$TARGET

# Pass-the-Key (using AES key)
getTGT.py -aesKey KerberosKey $DOMAIN/$USER@$TARGET
```

