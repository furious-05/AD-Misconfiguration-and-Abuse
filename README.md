# 🛡️ Active Directory Misconfiguration and Abuse

This repository provides a comprehensive lab-based walkthrough of various **Active Directory (AD)** misconfigurations and abuses. It demonstrates how specific weaknesses can be exploited in real-world enterprise environments, especially in **red teaming**, **penetration testing**, and **defensive security research**.

---

## 🏁 Lab Overview

- **Domain Name:** `furious.local`
- **Domain Controller (DC):** `DC01-FURIOUS5.furious.local`
- **Common User Used:** `jack` with password `complex1@`

##  Certificate Authority

- **Certificate Server**: `CA-FURIOUS.local`

All techniques are demonstrated in a lab setup with appropriate misconfigurations for safe testing and learning.

---

## 📚 Table of Contents

> Click on any section below to explore it. Each folder contains explanations, images, and steps to replicate or understand the attack.

## 🛠️ [Setting HomeLab](./Setting%20Homelab)

This section contains a detailed guide for creating your own Active Directory lab using Windows Server 2022, Windows 11, and Kali Linux. It includes:

- Hardware & virtualization requirements
- Operating system downloads
- Lab topology and machine roles
- Network setup
- Optional Defender configuration for offensive testing

### 🔐 [Active Directory Concepts](./ActiveDirectory%20Concept/TomeStoned)
- **[Tombstoned Object Abuse](./ActiveDirectory%20Concept/TomeStoned)**
- **[Timeroasting](./ActiveDirectory%20Concept/Timeroasting)**
  
### 🎓 [ADCS Abuse (Active Directory Certificate Services)](./ADCS)
- **[ESC1](./ADCS/ADCS-ESC1)**
- **[ESC2](./ADCS/ADCS-ESC2)**
- **[ESC3](./ADCS/ADCS-ESC3)**
- **[ESC4](./ADCS/ADCS-ESC4)**
- **[ESC6](./ADCS/ADCS-ESC6)**
- **[ESC10](./ADCS/ADCS-ESC10)**
- **[ESC14](./ADCS/ADCS-ESC14)**
- **[ESC15](./ADCS/ADCS-ESC15)**
- **[ESC16](./ADCS/ADCS-ESC16)**

### 🛠️ [DACL Abuse (Discretionary ACL)](./DACL%20abuse)
- **[ForceChangePassword](./DACL%20abuse/ForceChangePassword)**
- **[GenericAll](./DACL%20abuse/GenericAll)**
- **[ReadLAPSPassword](./DACL%20abuse/ReadLAPSPassword)**
- **[WriteDACL](./DACL%20abuse/WriteDACL)**
- **[WriteOwner](./DACL%20abuse/WriteOwner)**
- **[WriteScriptPath](./DACL%20abuse/WriteScriptPath/)**

### 🧠 [GPO Abuse (Group Policy Objects)](./GPO%20Abuse)
- **[GPO Misuse Techniques](./GPO%20Abuse)**

### 🦸 [Kerberos Attacks](./Kerbrose)
- **[ASREPRoasting](./Kerbrose/ASREProasting)**
- **[Kerberoasting](./Kerbrose/Kerbroasting)**
- **[Silver Ticket](./Kerbrose/SilverTicket)**
- **[Shadow Credential](./Kerbrose/ShadowCredential)**

### 🔄 [NTLM Attacks](./NTLM)
- **[Pass the Hash](./NTLM/PassTheHash)**
- **[Responder-based Attacks](./NTLM/Responder)**

### 🏠 [RBCD (Resource-Based Constrained Delegation)](./RBCD)
- **[RBCD Abuse](./RBCD)**


---

## 🗂️ Folder Structure

```

ActiveDirectory Misconfiguration and Abuse/
├── Setting Homelab/
├── ActiveDirectory Concept/
├── ADCS/
├── DACL abuse/
├── GPO Abuse/
├── Kerbrose/
├── NTLM/
└── RBCD/

```

---

## 🤝 Contributing

Feel free to submit issues or pull requests if you want to expand or correct any of the techniques or folder structures.

---

## ⚠️ Disclaimer

This content is for **educational and research purposes** only. Do not use any techniques described here on systems you do not own or have explicit permission to test.

---

