#!/usr/bin/env pwsh
# PhamaSafety A2A dev loop
$ErrorActionPreference = "Stop"

Write-Host "PhamaSafety — tri-agent A2A system" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Configure:" -ForegroundColor Green
Write-Host "   copy .env.example .env"
Write-Host "   # Set GOOGLE_API_KEY / GEMINI_API_KEY (Vertex AQ.* or AI Studio key)"
Write-Host ""
Write-Host "2. Start agents + Redis:" -ForegroundColor Green
Write-Host "   docker compose up --build"
Write-Host ""
Write-Host "3. Start Generative UI (optional Track 2):" -ForegroundColor Green
Write-Host "   pnpm dev"
Write-Host ""
Write-Host "4. Smoke test (requires a2a-hackathon CLI):" -ForegroundColor Green
Write-Host "   uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002"
Write-Host ""
Write-Host "Docs: README.md" -ForegroundColor Yellow
