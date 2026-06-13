#!/usr/bin/env pwsh
# A2A Hackathon dev loop — see A2A.md for full instructions.
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

Write-Host "A2A Hackathon — Rho-Bank agent pair" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure:" -ForegroundColor Green
Write-Host "   copy .env.example .env"
Write-Host "   # Set GOOGLE_API_KEY (Vertex AI key from GCP)"
Write-Host ""
Write-Host "2. Start agents + Redis:" -ForegroundColor Green
Write-Host "   docker compose up --build"
Write-Host ""
Write-Host "3. Clone harness (once, parent folder):" -ForegroundColor Green
Write-Host "   cd ..; git clone https://github.com/a2anet/a2a-hackathon.git"
Write-Host ""
Write-Host "4. Smoke test (from a2a-hackathon repo):" -ForegroundColor Green
Write-Host '   $env:GOOGLE_API_KEY = "your-key"'
Write-Host "   uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002"
Write-Host ""
Write-Host "Docs: A2A.md" -ForegroundColor Yellow
