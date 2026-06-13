#!/usr/bin/env pwsh
# One-time Application Default Credentials (ADC) setup for Vertex AI / Agent Platform.
# Use this when your org blocks API keys ("API keys are disallowed").
#
# After this script: leave GOOGLE_API_KEY empty in .env — agents use ADC instead.

$ErrorActionPreference = "Stop"

function Find-Gcloud {
    $cmd = Get-Command gcloud -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $candidates = @(
        "$env:ProgramFiles\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd",
        "$env:LocalAppData\Google\Cloud SDK\google-cloud-sdk\bin\gcloud.cmd"
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }
    return $null
}

Write-Host ""
Write-Host "=== Vertex AI — Application Default Credentials (ADC) ===" -ForegroundColor Cyan
Write-Host "Your org disallows API keys. ADC is the supported auth path." -ForegroundColor Yellow
Write-Host ""

$gcloud = Find-Gcloud
if (-not $gcloud) {
    Write-Host "Google Cloud SDK (gcloud) not found." -ForegroundColor Red
    Write-Host "Install it, then re-run this script:" -ForegroundColor Yellow
    Write-Host "  winget install Google.CloudSDK"
    Write-Host ""
    Write-Host "Or download: https://cloud.google.com/sdk/docs/install"
    exit 1
}

Write-Host "Using: $gcloud" -ForegroundColor Green
Write-Host ""

# Step 1: sign in (opens browser)
Write-Host "Step 1/3 — Sign in to Google Cloud (browser will open)..." -ForegroundColor Cyan
& $gcloud auth login --update-adc
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Step 2: application default credentials
Write-Host ""
Write-Host "Step 2/3 — Create Application Default Credentials..." -ForegroundColor Cyan
& $gcloud auth application-default login
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# Step 3: project + quota project
Write-Host ""
Write-Host "Step 3/3 — Set GCP project..." -ForegroundColor Cyan
$project = Read-Host "Enter your GOOGLE_CLOUD_PROJECT id (from GCP console)"
if ($project) {
    & $gcloud config set project $project
    & $gcloud auth application-default set-quota-project $project
}

$adcPath = Join-Path $env:APPDATA "gcloud\application_default_credentials.json"
if (-not (Test-Path $adcPath)) {
    Write-Host "ADC file not found at $adcPath" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "ADC ready: $adcPath" -ForegroundColor Green

# Patch .env if present
$envFile = Join-Path (Split-Path $PSScriptRoot -Parent) ".env"
if (Test-Path $envFile) {
    $content = Get-Content $envFile -Raw
    if ($project -and $content -notmatch "GOOGLE_CLOUD_PROJECT=") {
        Add-Content $envFile "`nGOOGLE_CLOUD_PROJECT=$project"
    } elseif ($project) {
        $content = $content -replace "GOOGLE_CLOUD_PROJECT=.*", "GOOGLE_CLOUD_PROJECT=$project"
        Set-Content $envFile $content -NoNewline
    }
    Write-Host "Updated .env — ensure GOOGLE_API_KEY stays empty." -ForegroundColor Green
} else {
    Write-Host "Copy .env.example to .env and set:" -ForegroundColor Yellow
    Write-Host "  GOOGLE_GENAI_USE_VERTEXAI=true"
    Write-Host "  GOOGLE_CLOUD_PROJECT=$project"
    Write-Host "  GOOGLE_CLOUD_LOCATION=us-central1"
    Write-Host "  GOOGLE_API_KEY=   (leave empty)"
}

Write-Host ""
Write-Host "Next:" -ForegroundColor Cyan
Write-Host "  docker compose up --build"
Write-Host "  # or run agents locally with the same env vars"
Write-Host ""
