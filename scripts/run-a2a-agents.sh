#!/usr/bin/env bash
# A2A Hackathon dev loop — see A2A.md
cat <<'EOF'
A2A Hackathon — Rho-Bank agent pair

1. copy .env.example .env  # set GOOGLE_API_KEY
2. docker compose up --build
3. Clone harness: git clone https://github.com/a2anet/a2a-hackathon.git
4. Smoke: uv run a2a-hack smoke --personal-url http://localhost:9001 --cs-url http://localhost:9002

Docs: A2A.md
EOF
