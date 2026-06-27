<#
.SYNOPSIS
    Routine context saver for azure-ai-pantheon.
    Run this (or have Grok run it) at the end of any significant work to prevent information loss after reboots.

.DESCRIPTION
    - Updates docs/LIVE_STATE.md with latest summary and timestamp.
    - Appends a structured entry to docs/SESSION_LOG.md.
    - Stages the context files for git.
    - Prints a ready-to-use commit message.

.USAGE
    # Interactive
    .\scripts\save-context.ps1 -Summary "Finished exploring the Hermes factory Bicep modules"

    # Or from agent: use terminal command with -Summary

    # Force bypass if execution policy blocks:
    powershell -ExecutionPolicy Bypass -File .\scripts\save-context.ps1 -Summary "..."
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$Summary,

    [string]$NextSteps = "",

    [string]$FocusArea = "General progress"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$DateOnly = Get-Date -Format "yyyy-MM-dd"

Write-Host "=== Saving Context for azure-ai-pantheon ===" -ForegroundColor Cyan
Write-Host "Timestamp: $Timestamp"
Write-Host "Summary: $Summary"

# 1. Update LIVE_STATE.md
$liveStatePath = "docs\LIVE_STATE.md"
if (Test-Path $liveStatePath) {
    $content = Get-Content $liveStatePath -Raw

    # Update the Last Updated line
    $content = $content -replace '(?m)^(\*\*Last Updated\*\*:).*', "**Last Updated**: $Timestamp"

    # Replace the "What We Are Working On Right Now" section
    $newCurrent = @"
## What We Are Working On Right Now
$FocusArea

## Last Major Accomplishments
$Summary
"@

    # Simple approach: insert after the header section
    if ($content -match '## What We Are Working On Right Now') {
        # Replace the section
        $content = [regex]::Replace($content, '(?s)(## What We Are Working On Right Now).*?(?=## |$)', "$newCurrent`n`n", 1)
    }

    # Update Next Immediate Steps if provided
    if ($NextSteps) {
        $content = $content -replace '(?m)^## Next Immediate Steps.*?(?=^## |$)', "## Next Immediate Steps`n$NextSteps`n`n", 1
    }

    Set-Content -Path $liveStatePath -Value $content -NoNewline
    Write-Host "Updated: $liveStatePath" -ForegroundColor Green
}

# 2. Append to SESSION_LOG.md
$logPath = "docs\SESSION_LOG.md"
$logEntry = @"

## $Timestamp — $FocusArea
**Focus**: $FocusArea
**Key Changes**:
- $Summary
**Context Saved To**:
- docs/LIVE_STATE.md
- docs/SESSION_LOG.md
**Next Steps**:
$NextSteps

"@

Add-Content -Path $logPath -Value $logEntry
Write-Host "Appended to: $logPath" -ForegroundColor Green

# 3. Stage context files
git add AGENTS.md README.md docs/LIVE_STATE.md docs/SESSION_LOG.md docs/STATUS.md docs/DECISIONS.md 2>$null
Write-Host "Staged context files for commit." -ForegroundColor Green

# 4. Suggest commit
$commitMsg = "chore(context): $FocusArea - $Summary"
Write-Host "`n=== Recommended Git Commit ===" -ForegroundColor Yellow
Write-Host "git commit -m `"$commitMsg`""
Write-Host "`nRun the commit manually or ask the agent to do it."

Write-Host "`nContext save complete. Reboot-safe memory updated." -ForegroundColor Cyan
