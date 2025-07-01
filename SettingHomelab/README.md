# 🏗️ Home Active Directory Lab Setup

This guide outlines how to build a home-based Active Directory (AD) lab for simulating misconfigurations, attacks, and defenses. In this setup, we use **Windows Server 2022** as the Domain Controller and a single **Windows 11** desktop as the client.

Running both systems alongside a virtualized attacker machine (like Kali Linux) is possible on a 16 GB RAM system, but performance may vary.

- ✅ If you are only running **Windows Server + Kali Linux**, 16 GB RAM is generally sufficient.
- ⚠️ If you run **Windows Server + Windows 11 + Kali Linux** in parallel, especially with your host OS also active, performance may degrade.
- 🧠 Tip: For lightweight operation, keep only the **Domain Controller** and **Kali machine** running during most simulations.

---

## 💻 What You Need to Set Up a Home AD Lab

### 1. **System Requirements (Host Machine)**

| Resource | Recommended              |
| -------- | ------------------------ |
| RAM      | 16 GB minimum            |
| CPU      | 4 cores minimum          |
| Disk     | 100–150 GB SSD           |
| OS       | Windows, Linux, or macOS |

---

### 2. **Virtualization Platform**

Choose any one of the following:

- 🔹 [**VMware Workstation Player** (Free)](https://www.vmware.com/products/workstation-player.html) — Recommended for Windows
- 🔹 [**VirtualBox** (Free)](https://www.virtualbox.org/) — Cross-platform
- 🔹 [**Proxmox** (Free hypervisor)](https://www.proxmox.com/) — For advanced users and dedicated lab machines

---

### 3. **ISOs / Operating Systems**

Download the following:

| Role              | OS                          | Source                                                                                                         |
| ----------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------- |
| Domain Controller | Windows Server 2019 or 2022 | [Window Server 2022](https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022)         |
| Client Machine    | Windows 10 or 11            | [Microsoft Developer VMs](https://www.microsoft.com/en-us/software-download/windows11)          |
| Attacker Machine  | Kali Linux or Parrot OS     | [Kali Linux](https://www.kali.org/get-kali/) or [Parrot OS](https://www.parrotsec.org/)                        |

---

### 4. **Lab Structure**

Below is the logical layout of your AD lab network:

```

\[ Kali Linux ] <-- same virtual network --> \[ Windows 11 Client ] <-- domain-joined --> \[ Windows Server 2022 DC ]

````

- All machines should be configured on the **same internal or host-only network**
- The **Domain Controller** should act as DNS for all systems

---

## ⚙️ Step-by-Step Setup Guide

To simplify the setup process, you can follow this excellent video guide by **Jim Schultz**:

[![Watch the setup video](https://img.youtube.com/vi/aqA6bktFHoY/0.jpg)](https://youtu.be/aqA6bktFHoY)

🎥 **[How to Set Up an Active Directory Home Lab – Jim Schultz](https://youtu.be/aqA6bktFHoY?si=0i3Fo3pSMD3RZsWm)**

This video walks through VM creation, Windows Server configuration, domain promotion, and domain join processes.

---

## 🔒 Optional: Disable Windows Defender (for testing)

While this is not required for AD setup, some offensive tools (e.g., `PsExec`, `Mimikatz`, etc.) may be flagged or blocked by Windows Defender. You can disable real-time protection temporarily:

```powershell
Set-MpPreference -DisableRealtimeMonitoring $true
````

To re-enable it:

```powershell
Set-MpPreference -DisableRealtimeMonitoring $false
```

---

This setup provides a solid foundation for exploring the attacks documented throughout this repository.


