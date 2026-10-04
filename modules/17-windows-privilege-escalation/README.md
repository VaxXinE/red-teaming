# Module 17 - Windows Privilege Escalation

**Red Team Learning Path - Omarchy / Arch Linux Edition**

Module ini membangun methodology privilege escalation Windows dari **manual enumeration -> hypothesis -> controlled proof -> evidence -> cleanup -> remediation**.

> [!IMPORTANT]
> Gunakan hanya pada Windows VM milik sendiri, intentionally vulnerable lab, CTF, atau target yang secara eksplisit mengizinkan pengujian. Local lab bundled bersifat reversible dan tidak mendaftarkan service/scheduled-task persistence nyata.

## Learning outcomes

- Memahami access token, SID, privileges, integrity level, UAC, Administrator dan LocalSystem.
- Menganalisis DACL/ACE pada file, directory, Registry dan Windows services.
- Mengidentifikasi weak service configuration, privileged scheduled-task action, autorun path dan execution-path trust issues.
- Menggunakan `whoami`, PowerShell, `icacls`, `Get-Acl`, CIM/WMI, AccessChk, Autoruns, Process Monitor dan WinPEAS secara metodologis.
- Menilai credential/config exposure tanpa melakukan indiscriminate credential dumping.
- Melakukan minimum sufficient proof, cleanup, detection-aware analysis dan remediation.

## Files

```text
17-windows-privilege-escalation/
├── README.md
├── docx/
│   └── Red-Team-Module-17-Windows-Privilege-Escalation-Omarchy.docx
├── pdf/
│   └── Red-Team-Module-17-Windows-Privilege-Escalation-Omarchy.pdf
└── labs/
    ├── README.txt
    ├── workspace-init.ps1
    ├── token-report.ps1
    ├── manual-enum.ps1
    ├── acl-audit.ps1
    ├── service-audit.ps1
    ├── task-audit.ps1
    ├── autorun-audit.ps1
    ├── config-secret-audit.ps1
    ├── lab-sim.ps1
    ├── evidence-manifest.ps1
    └── finding-note.ps1
```

## Local lab

`lab-sim.ps1` membuat trust-boundary simulation di `C:\ProgramData\RedTeamLab17`. Normal user dapat memodifikasi training script, sedangkan elevated terminal secara manual mensimulasikan privileged consumer. Lab **tidak** membuat real vulnerable Windows service, scheduled task, local user, persistence, atau outbound callback.

```powershell
# Elevated PowerShell
.\labs\lab-sim.ps1 -Action setup

# Normal PowerShell
.\labs\lab-sim.ps1 -Action status

# Elevated terminal only when the exercise asks for the trigger
.\labs\lab-sim.ps1 -Action run-elevated

# Cleanup
.\labs\lab-sim.ps1 -Action cleanup
```

## Key references

- Microsoft Learn - Access Tokens
- Microsoft Learn - Mandatory Integrity Control
- Microsoft Learn - DACLs and ACEs / icacls
- Microsoft Learn - Service Security and Access Rights
- Microsoft Learn - Task Scheduler security contexts
- Microsoft Sysinternals - AccessChk, Autoruns, Process Monitor
- PEASS-ng - WinPEAS
- Omarchy Manual - Windows VM

See the PDF/DOCX for the complete references and lab instructions.
