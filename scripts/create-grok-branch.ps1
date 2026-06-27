<#
.SYNOPSIS
    Creates a new feature branch with the required 'grok/' prefix.

.DESCRIPTION
    All feature branches in this repo must use the 'grok/' prefix.
    This script enforces the convention: grok/<your-feature-name>

.EXAMPLE
    .\scripts\create-grok-branch.ps1 add-maf-orchestrator

    Creates branch: grok/add-maf-orchestrator

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\scripts\create-grok-branch.ps1 "hermes-agent-wrapper-improvements"
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$FeatureName,

    [switch]$NoCheckout
)

$ErrorActionPreference = "Stop"

# Normalize the name: lowercase, replace spaces/underscores with hyphens, remove invalid chars
$slug = $FeatureName.ToLower() `
    -replace '\s+', '-' `
    -replace '_+', '-' `
    -replace '[^a-z0-9-]', '' `
    -replace '-+', '-' `
    -replace '^-|-$', ''

if ([string]::IsNullOrWhiteSpace($slug)) {
    Write-Error "Feature name must result in a valid slug after normalization."
    exit 1
}

$branchName = "grok/$slug"

Write-Host "Creating feature branch with required 'grok/' prefix..." -ForegroundColor Cyan
Write-Host "  Requested: $FeatureName"
Write-Host "  Normalized: $slug"
Write-Host "  Branch:     $branchName" -ForegroundColor Green

# Check if branch already exists
$existing = git branch --list $branchName 2>$null
if ($existing) {
    Write-Warning "Branch '$branchName' already exists locally."
    git checkout $branchName
    exit 0
}

# Create the branch
if ($NoCheckout) {
    git branch $branchName
    Write-Host "Branch '$branchName' created (not checked out)." -ForegroundColor Yellow
} else {
    git checkout -b $branchName
    Write-Host "Switched to new branch '$branchName'" -ForegroundColor Green
}

Write-Host ""
Write-Host "Remember: All feature work must live under the 'grok/' prefix." -ForegroundColor Cyan
Write-Host "When done, push with: git push -u origin $branchName" -ForegroundColor Cyan
