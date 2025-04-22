
Using Poker_Capstone
====================

Features
--------

Sprint 1: Core Game Engine & Web Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Poker logic classes (Card, Deck, Hand, Table, Pot) with full round‑robin play
- 5–7‑card hand evaluation and winner determination via `evaluate_hand`
- Web endpoints: `run_game()` view, dynamic strategy discovery
- Bot upload UI for `.py` files, local

Sprint 2: Tournament Management & Persistent Storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- `run_tournament()` for batch games and score aggregation
- Django models: `StudentBot`, `BaseBot`, `TournamentData`, `Tournament`
- Student/Admin profile pages, tournament history with “Closed By” reporting
- Cloud SQL (MySQL) integration, zero‑downtime migrations


Sprint 3: Authentication, Deployment & Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Azure AD OAuth2 via `microsoft_auth`
- Per‑bot timeouts using `ThreadPoolExecutor` and `BotTimeout
- Security: CSRF trusted origins, session settings on App Engine
- App Engine Standard deployment: `app.yaml`, static files via WhiteNoise/GCS
- CI/CD: Cloud SQL Auth Proxy, Docker parity, `gcloud app deploy`
- Sphinx + ReadTheDocs: installation, usage, API reference
- Dockerized local dev: Django + MySQL with docker‑compose, `.env` config

