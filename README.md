# Wazuh Advanced Security Hardening & Automation 🛡️

![Wazuh](https://img.shields.io/badge/SIEM-Wazuh-blue?style=for-the-badge&logo=wazuh)
![Python](https://img.shields.io/badge/Automation-Python-yellow?style=for-the-badge&logo=python)
![Discord](https://img.shields.io/badge/Alerts-Discord-5865F2?style=for-the-badge&logo=discord)
![VirusTotal](https://img.shields.io/badge/Intelligence-VirusTotal-blueviolet?style=for-the-badge)
![Linux](https://img.shields.io/badge/Platform-Linux-lightgrey?style=for-the-badge&logo=linux)

## 📋 Project Overview

Repository ini mendokumentasikan implementasi **Advanced Threat Detection & Automated Response** menggunakan Wazuh SIEM pada lingkungan Linux Server.

Project ini berfokus pada **Defense in Depth**: menggabungkan deteksi malware (VirusTotal), pemantauan integritas file (FIM Who-Data), deteksi Rootkit (Rkhunter), serta sistem respons otomatis (Active Response) yang terintegrasi langsung dengan notifikasi **Discord**.

## 🚀 Key Features

### 1. 🔔 Real-time Discord Alerting
Sistem notifikasi instan ke channel Discord untuk insiden prioritas tinggi.
* **Mechanism:** Menggunakan integrasi webhook custom yang dikonfigurasi secara modular.
* **Benefit:** Security Engineer mendapatkan notifikasi "Ping" di HP detik itu juga saat ada serangan kritis (Level 12+), memangkas waktu respons (MTTR).

### 2. 🕵️ Insider Threat Mitigation ("Who-Data" & Kill Switch)
Mendeteksi dan menghentikan user yang mencoba memodifikasi konfigurasi krusial sistem.
* **Detection:** Menggunakan Auditd untuk menangkap *siapa* yang mengubah file `/etc/shadow`, `/etc/passwd`, atau `/etc/ssh/sshd_config`.
* **Response:** Script Python custom (`kill_user.py`) akan dieksekusi otomatis untuk **terminasi sesi user** (`loginctl`) dan **mematikan proses** (`SIGKILL`) user tersebut seketika.

### 3. 🧱 SSH Brute-Force Protection
Mencegah serangan dictionary attack pada layanan SSH.
* **Action:** Jika terdeteksi kegagalan login berulang (5x dalam 30 detik), Firewall Agent otomatis memblokir IP penyerang selama **60 detik**.

### 4. 🦠 Automated Malware Analysis (VirusTotal)
Integrasi API VirusTotal untuk memindai file baru atau file yang berubah di sistem tanpa perlu antivirus berat (Agentless).

### 5. 🐛 Rootkit & Backdoor Detection
Integrasi log **Rkhunter** dengan Wazuh Decoder & Rules custom untuk mendeteksi anomali sistem yang tersembunyi.

## 📂 Repository Structure

```text
├── active-response/       
│   └── kill_user.py         # Script Python "Doomsday" untuk terminasi user nakal
├── rules/                 
│   └── local_rules.xml      # Custom XML Rules (FIM Sensitive & Rkhunter)
├── decoders/              
│   └── local_decoder.xml    # Custom Decoder untuk parsing log Rkhunter
├── custom-integration/
│   └── custom-discord.xml   # Konfigurasi khusus Discord Webhook
└── configs/               
    ├── active_response.xml  # Snippet Config: SSH Ban & Kill User Setup
    └── virustotal.xml       # Snippet Config: VirusTotal Integration