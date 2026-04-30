# Amplified Client Security Audit — Windows
# Version: 1.0 | 15 March 2026
# Framework: client-security-framework.md
#
# Run as Administrator:
#   Right-click PowerShell → Run as Administrator
#   Set-ExecutionPolicy Bypass -Scope Process -Force
#   .\amplified-client-audit-windows.ps1

$LogFile = "$env:USERPROFILE\Desktop\amplified-security-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
$script:FixesNeeded = 0
$script:ChecksPassed = 0
$script:AmberCount = 0

function Log($msg) {
    Write-Host $msg
    Add-Content -Path $LogFile -Value $msg
}

function Status($color, $label, $detail) {
    $prefix = "[$label]"
    switch ($color) {
        "Red"    { Write-Host $prefix -ForegroundColor Red -NoNewline; Write-Host " $detail" }
        "Green"  { Write-Host $prefix -ForegroundColor Green -NoNewline; Write-Host " $detail" }
        "Yellow" { Write-Host $prefix -ForegroundColor Yellow -NoNewline; Write-Host " $detail" }
    }
    Add-Content -Path $LogFile -Value "$prefix $detail"
    if ($label -eq "RED") { $script:FixesNeeded++ }
    if ($label -eq "GREEN") { $script:ChecksPassed++ }
    if ($label -eq "AMBER") { $script:AmberCount++ }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Log "AMPLIFIED SECURITY AUDIT — Windows"
Write-Host "============================================" -ForegroundColor Cyan
Log "Date: $(Get-Date)"
Log "Host: $env:COMPUTERNAME"
Log "User: $env:USERNAME"
Log ""

# Check we're running as admin
$IsElevated = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $IsElevated) {
    Write-Host "[WARNING] Not running as Administrator — some checks may be incomplete" -ForegroundColor Yellow
    Log "[WARNING] Not running as Administrator"
    Log ""
}

# ═══════════════════════════════════════════
# TIER 1: CRITICAL
# ═══════════════════════════════════════════

Write-Host ""
Write-Host "--- TIER 1: CRITICAL (fix immediately) ---" -ForegroundColor Cyan
Log "--- TIER 1: CRITICAL ---"
Log ""

# 1. Windows version
Log "1. Operating System"
$OSInfo = Get-CimInstance Win32_OperatingSystem
$OSVersion = $OSInfo.Caption.Trim()
$OSBuild = $OSInfo.BuildNumber

if ($OSVersion -match "Windows 11") {
    Status "Green" "GREEN" "$OSVersion (Build $OSBuild) — supported"
} elseif ($OSVersion -match "Windows 10") {
    Status "Red" "RED" "$OSVersion — END OF LIFE since October 2025. Cyber Essentials automatic fail."
    Log "   FIX: Upgrade to Windows 11. Check compatibility: Settings → Windows Update → Check for updates"
} elseif ($OSVersion -match "Windows (8|7|XP|Vista)") {
    Status "Red" "RED" "$OSVersion — long out of support. Must upgrade."
} else {
    Status "Yellow" "AMBER" "$OSVersion (Build $OSBuild) — verify this version is still supported"
}

# 2. Windows Update
Log ""
Log "2. Windows Update / Patching"
try {
    # Check for pending updates
    $UpdateSession = New-Object -ComObject Microsoft.Update.Session
    $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
    $SearchResult = $UpdateSearcher.Search("IsInstalled=0 and IsHidden=0")
    $PendingCount = $SearchResult.Updates.Count

    # Count critical/important
    $CriticalCount = 0
    foreach ($Update in $SearchResult.Updates) {
        if ($Update.MsrcSeverity -match "Critical|Important") { $CriticalCount++ }
    }

    if ($PendingCount -eq 0) {
        Status "Green" "GREEN" "Windows Update: fully patched (no pending updates)"
    } elseif ($CriticalCount -gt 0) {
        Status "Red" "RED" "$PendingCount pending updates ($CriticalCount critical/important). CE requires within 14 days."
        Log "   FIX: Settings → Windows Update → Check for updates → Install all"
    } else {
        Status "Yellow" "AMBER" "$PendingCount pending updates (none critical). Install when convenient."
    }
} catch {
    Status "Yellow" "AMBER" "Could not query Windows Update — verify manually: Settings → Windows Update"
}

# Check auto-update is enabled
try {
    $AUKey = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" -Name "AUOptions" -ErrorAction Stop
    switch ($AUKey.AUOptions) {
        1 { Status "Red" "RED" "Auto-update: DISABLED. CE requires automatic updates." }
        2 { Status "Yellow" "AMBER" "Auto-update: notify only. Recommend auto-install (option 4)." }
        3 { Status "Yellow" "AMBER" "Auto-update: auto-download, manual install. Acceptable but auto-install preferred." }
        4 { Status "Green" "GREEN" "Auto-update: auto-download and auto-install" }
        default { Status "Yellow" "AMBER" "Auto-update setting: $($AUKey.AUOptions) — verify manually" }
    }
} catch {
    Status "Yellow" "AMBER" "Auto-update registry key not found — Windows likely using default (enabled)"
}

# 3. User Account Type
Log ""
Log "3. User Account Type"
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# Get local admin group members
try {
    $AdminGroup = net localgroup Administrators 2>$null
    $AdminMembers = $AdminGroup | Where-Object {
        $_ -and
        $_ -notmatch "^(Alias|Comment|Members|The command|---)" -and
        $_.Trim() -ne ""
    }
    $AdminCount = ($AdminMembers | Measure-Object).Count
} catch {
    $AdminMembers = @("Could not enumerate")
    $AdminCount = 0
}

if ($IsAdmin) {
    Status "Yellow" "AMBER" "Current session running as Administrator ($CurrentUser). Use standard account for daily work."
} else {
    Status "Green" "GREEN" "Running as standard user ($CurrentUser)"
}
Log "   Local admin accounts ($AdminCount): $($AdminMembers -join ', ')"

# 4. MFA check hint
Log ""
Log "4. Cloud Service MFA (manual verification needed)"
Status "Yellow" "AMBER" "Verify MFA is enabled on: Microsoft 365, Google Workspace, Xero, QuickBooks, and all cloud services"
Log "   This cannot be checked locally — verify in each service's admin console"

# ═══════════════════════════════════════════
# TIER 2: SAME DAY
# ═══════════════════════════════════════════

Log ""
Write-Host ""
Write-Host "--- TIER 2: FIX SAME DAY ---" -ForegroundColor Cyan
Log "--- TIER 2: SAME DAY ---"
Log ""

# 5. Firewall
Log "5. Windows Firewall"
try {
    $FWProfiles = Get-NetFirewallProfile -ErrorAction Stop
    $AllOn = $true
    foreach ($p in $FWProfiles) {
        if (-not $p.Enabled) {
            $AllOn = $false
            Status "Red" "RED" "Firewall profile '$($p.Name)' is OFF"
            Log "   FIX: Set-NetFirewallProfile -Name $($p.Name) -Enabled True"
        }
    }
    if ($AllOn) {
        Status "Green" "GREEN" "Firewall: all profiles ON (Domain, Private, Public)"
    }
} catch {
    Status "Yellow" "AMBER" "Could not check firewall — verify in Windows Security → Firewall"
}

# 6. Windows Defender / Antivirus
Log ""
Log "6. Malware Protection"
try {
    $DefenderStatus = Get-MpComputerStatus -ErrorAction Stop
    $RealTime = $DefenderStatus.RealTimeProtectionEnabled
    $SigAge = $DefenderStatus.AntivirusSignatureAge
    $EngineVer = $DefenderStatus.AMEngineVersion
    $SigVer = $DefenderStatus.AntivirusSignatureVersion

    if ($RealTime) {
        Status "Green" "GREEN" "Windows Defender: real-time protection ON"
    } else {
        Status "Red" "RED" "Windows Defender: real-time protection OFF"
        Log "   FIX: Windows Security → Virus & threat protection → Real-time protection → ON"
    }

    if ($SigAge -le 1) {
        Status "Green" "GREEN" "Virus definitions: current ($SigAge day old, v$SigVer)"
    } elseif ($SigAge -le 7) {
        Status "Yellow" "AMBER" "Virus definitions: $SigAge days old (CE+ requires within 1 day)"
    } else {
        Status "Red" "RED" "Virus definitions: $SigAge days old — severely outdated"
        Log "   FIX: Windows Security → Virus & threat protection → Protection updates → Check for updates"
    }

    # Cloud protection
    if ($DefenderStatus.IoavProtectionEnabled) {
        Status "Green" "GREEN" "Cloud-delivered protection: ON"
    } else {
        Status "Yellow" "AMBER" "Cloud-delivered protection: OFF — enable for better detection"
    }

    # Tamper protection
    if ($DefenderStatus.IsTamperProtected) {
        Status "Green" "GREEN" "Tamper protection: ON"
    } else {
        Status "Yellow" "AMBER" "Tamper protection: OFF — prevents malware from disabling Defender"
    }
} catch {
    # Check for third-party AV
    try {
        $AV = Get-CimInstance -Namespace "root/SecurityCenter2" -ClassName AntiVirusProduct -ErrorAction Stop
        $AVNames = ($AV | ForEach-Object { $_.displayName }) -join ", "
        Status "Yellow" "AMBER" "Third-party AV detected: $AVNames. Verify it's current and actively scanning."
    } catch {
        Status "Red" "RED" "No antivirus detected. Cyber Essentials requires AV on all Windows devices."
    }
}

# 7. Disk Encryption
Log ""
Log "7. Disk Encryption (BitLocker / Device Encryption)"
try {
    $BL = Get-BitLockerVolume -MountPoint "C:" -ErrorAction Stop
    if ($BL.ProtectionStatus -eq "On") {
        $Method = $BL.EncryptionMethod
        Status "Green" "GREEN" "BitLocker: ON (C: drive, $Method)"
    } else {
        Status "Red" "RED" "BitLocker: OFF on C: drive — stolen device = data breach"
        Log "   FIX (Pro): manage-bde -on C: -RecoveryPassword"
        Log "   FIX (Home): Settings → Privacy & security → Device encryption → Turn ON"
    }
} catch {
    # Try Device Encryption for Home edition
    try {
        $DEStatus = Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\BitLocker" -ErrorAction Stop
        if ($DEStatus.DeviceEncryptionStatus -eq 1) {
            Status "Green" "GREEN" "Device Encryption: ON"
        } else {
            Status "Yellow" "AMBER" "Disk encryption status unclear — check Settings → Privacy & security → Device encryption"
        }
    } catch {
        Status "Yellow" "AMBER" "Could not determine disk encryption status — may be Windows Home without hardware support"
        Log "   Windows 11 Home supports Device Encryption if hardware TPM 2.0 present"
    }
}

# 8. Screen Lock
Log ""
Log "8. Screen Lock / Power Settings"
try {
    # Check screen timeout (AC power)
    $PowerCfg = powercfg /query SCHEME_CURRENT SUB_VIDEO VIDEOIDLE 2>$null
    $ACTimeout = ($PowerCfg | Select-String "Current AC Power Setting Index" | ForEach-Object { $_.Line -replace '.*0x', '' }) -replace '^0*', ''
    if ($ACTimeout) {
        $ACTimeoutSec = [Convert]::ToInt32($ACTimeout, 16)
        $ACTimeoutMin = [math]::Round($ACTimeoutSec / 60)
        if ($ACTimeoutSec -eq 0) {
            Status "Red" "RED" "Screen timeout: NEVER (AC power). CE requires ≤15 min."
            Log "   FIX: Settings → System → Power & battery → Screen → Turn off after 5 minutes"
        } elseif ($ACTimeoutMin -le 15) {
            Status "Green" "GREEN" "Screen timeout: $ACTimeoutMin minutes (AC power)"
        } else {
            Status "Red" "RED" "Screen timeout: $ACTimeoutMin minutes (AC power). CE requires ≤15 min."
        }
    }
} catch {
    Status "Yellow" "AMBER" "Could not check screen timeout — verify in Settings → System → Power"
}

# Check password on wake
$PassOnWake = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Power\PowerSettings\0e796bdb-100d-47d6-a2d5-f7d2daa51f51" -Name "ACSettingIndex" -ErrorAction SilentlyContinue).ACSettingIndex
if ($null -ne $PassOnWake -and $PassOnWake -eq 1) {
    Status "Green" "GREEN" "Password required on wake: YES"
} else {
    Status "Yellow" "AMBER" "Password on wake — verify: Settings → Accounts → Sign-in options → require sign-in"
}

# 9. Office Macros
Log ""
Log "9. Microsoft Office Macro Security"
$OfficeApps = @("Word", "Excel", "PowerPoint")
$MacrosChecked = $false
foreach ($app in $OfficeApps) {
    # Check Office 2016/2019/365 (version 16.0)
    $MacroKey = "HKCU:\Software\Microsoft\Office\16.0\$app\Security"
    if (Test-Path $MacroKey) {
        $MacrosChecked = $true
        $VBAWarnings = (Get-ItemProperty -Path $MacroKey -Name "VBAWarnings" -ErrorAction SilentlyContinue).VBAWarnings
        if ($null -eq $VBAWarnings) {
            Status "Yellow" "AMBER" "$app macros: using default setting — verify: File → Options → Trust Center → Macro Settings"
        } elseif ($VBAWarnings -ge 4) {
            Status "Green" "GREEN" "$app macros: disabled without notification"
        } elseif ($VBAWarnings -ge 3) {
            Status "Green" "GREEN" "$app macros: disabled except digitally signed"
        } elseif ($VBAWarnings -ge 2) {
            Status "Yellow" "AMBER" "$app macros: disabled with notification — acceptable but could be tighter"
        } else {
            Status "Red" "RED" "$app macros: ALL ENABLED — CE requires disabled unless business-critical"
        }
    }
}
if (-not $MacrosChecked) {
    Status "Green" "GREEN" "Office macro registry keys not found — Office may not be installed or using defaults"
}

# 10. AutoRun / AutoPlay
Log ""
Log "10. AutoRun / AutoPlay"
$AutoRunVal = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "NoDriveTypeAutoRun" -ErrorAction SilentlyContinue).NoDriveTypeAutoRun
if ($AutoRunVal -eq 255) {
    Status "Green" "GREEN" "AutoRun: disabled for all drive types"
} elseif ($null -eq $AutoRunVal) {
    Status "Yellow" "AMBER" "AutoRun policy not explicitly set — check Settings → Bluetooth & devices → AutoPlay"
} else {
    Status "Yellow" "AMBER" "AutoRun: partially configured (value=$AutoRunVal). Recommend disabling for all (255)."
}

# ═══════════════════════════════════════════
# SOFTWARE INVENTORY
# ═══════════════════════════════════════════

Log ""
Write-Host ""
Write-Host "--- SOFTWARE INVENTORY ---" -ForegroundColor Cyan
Log "--- SOFTWARE INVENTORY ---"
Log ""

# Collect installed software from registry
$InstalledSoftware = @()
$RegistryPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

foreach ($path in $RegistryPaths) {
    $InstalledSoftware += Get-ItemProperty $path -ErrorAction SilentlyContinue |
        Where-Object { $_.DisplayName -and $_.DisplayName.Trim() -ne "" } |
        Select-Object DisplayName, DisplayVersion, Publisher
}

# Deduplicate
$InstalledSoftware = $InstalledSoftware | Sort-Object DisplayName -Unique
Log "Total installed applications: $($InstalledSoftware.Count)"

Write-Host ""
Write-Host "--- KNOWN-RISK SOFTWARE CHECK ---" -ForegroundColor Cyan
Log ""
Log "--- KNOWN-RISK SOFTWARE CHECK ---"
Log ""

# WinRAR (CVE-2023-38831 — actively exploited)
$WinRAR = $InstalledSoftware | Where-Object { $_.DisplayName -match "WinRAR" }
if ($WinRAR) {
    $WRVer = $WinRAR.DisplayVersion
    if ($WRVer -and [version]$WRVer -lt [version]"6.24") {
        Status "Red" "RED" "WinRAR $WRVer — VULNERABLE (CVE-2023-38831). Update to 6.24+ or replace with 7-Zip."
    } else {
        Status "Yellow" "AMBER" "WinRAR $WRVer — verify it's current. Consider free 7-Zip as alternative."
    }
}

# CCleaner
$CCleaner = $InstalledSoftware | Where-Object { $_.DisplayName -match "CCleaner" }
if ($CCleaner) {
    Status "Red" "RED" "CCleaner $($CCleaner.DisplayVersion) — supply chain attack history (2017). Recommend removing."
    Log "   Windows built-in Disk Cleanup does the same job safely."
}

# Java Runtime
$Java = $InstalledSoftware | Where-Object { $_.DisplayName -match "^Java\s" -or $_.DisplayName -match "Java.*Runtime" -or $_.DisplayName -match "^Java\(TM\)" }
if ($Java) {
    $JavaNames = ($Java | ForEach-Object { "$($_.DisplayName) v$($_.DisplayVersion)" }) -join ", "
    Status "Yellow" "AMBER" "Java detected: $JavaNames. Remove if not needed — large attack surface."
}

# Adobe Reader/Acrobat
$Adobe = $InstalledSoftware | Where-Object { $_.DisplayName -match "Adobe (Acrobat|Reader)" }
if ($Adobe) {
    Status "Yellow" "AMBER" "Adobe: $($Adobe.DisplayName) v$($Adobe.DisplayVersion). Verify auto-update ON, JavaScript OFF."
}

# Old Office versions
$OldOffice = $InstalledSoftware | Where-Object { $_.DisplayName -match "Microsoft Office (Professional|Home|Standard|Business).*(2010|2013|2016|2019)" }
if ($OldOffice) {
    Status "Red" "RED" "Old Office detected: $($OldOffice.DisplayName). End of support = CE fail. Upgrade to Microsoft 365."
}

# Google Chrome
$Chrome = $InstalledSoftware | Where-Object { $_.DisplayName -match "Google Chrome" }
if ($Chrome) {
    Status "Green" "GREEN" "Google Chrome v$($Chrome.DisplayVersion) — verify auto-update: chrome://settings/help"
}

# Firefox
$Firefox = $InstalledSoftware | Where-Object { $_.DisplayName -match "Mozilla Firefox" }
if ($Firefox) {
    Status "Yellow" "AMBER" "Firefox v$($Firefox.DisplayVersion) — verify auto-update in Settings → General"
}

# Zoom
$Zoom = $InstalledSoftware | Where-Object { $_.DisplayName -match "Zoom" }
if ($Zoom) {
    Status "Yellow" "AMBER" "Zoom v$($Zoom.DisplayVersion) — verify auto-update in Settings → General"
}

# Flash Player (should be gone but occasionally found)
$Flash = $InstalledSoftware | Where-Object { $_.DisplayName -match "Flash Player|Adobe Flash" }
if ($Flash) {
    Status "Red" "RED" "Adobe Flash Player detected — dead since 2020. REMOVE IMMEDIATELY."
}

# VLC
$VLC = $InstalledSoftware | Where-Object { $_.DisplayName -match "VLC" }
if ($VLC) {
    Status "Yellow" "AMBER" "VLC v$($VLC.DisplayVersion) — verify it's current (Help → Check for Updates)"
}

# 7-Zip
$SevenZip = $InstalledSoftware | Where-Object { $_.DisplayName -match "7-Zip" }
if ($SevenZip) {
    Status "Green" "GREEN" "7-Zip v$($SevenZip.DisplayVersion)"
}

# ─── FULL SOFTWARE LIST ───

Log ""
Log "--- FULL SOFTWARE LIST ---"
$InstalledSoftware | ForEach-Object {
    Log "  $($_.DisplayName) | v$($_.DisplayVersion) | $($_.Publisher)"
}

# ═══════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════

Log ""
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Log "============================================"
Log "SUMMARY"
Log "============================================"

$Total = $script:ChecksPassed + $script:FixesNeeded + $script:AmberCount
if ($Total -gt 0) {
    $PassPct = [math]::Round(($script:ChecksPassed / $Total) * 100)
} else {
    $PassPct = 100
}

Log "Total checks: $Total"
Log "Passed (GREEN): $script:ChecksPassed ($PassPct%)"
Log "Needs attention (AMBER): $script:AmberCount"
Log "Must fix (RED): $script:FixesNeeded"
Log ""

if ($script:FixesNeeded -eq 0) {
    Write-Host "ALL CLEAR — No critical fixes needed. $PassPct% already good." -ForegroundColor Green
    Log "ALL CLEAR — No critical fixes needed. $PassPct% already good."
} else {
    Write-Host "$($script:FixesNeeded) items need fixing — see RED items above" -ForegroundColor Red
    Log "$($script:FixesNeeded) items need fixing — see RED items above"
}

Log ""
Log "Full log saved to: $LogFile"
Log "============================================"

Write-Host ""
Write-Host "Log saved to: $LogFile" -ForegroundColor Cyan
Write-Host ""
