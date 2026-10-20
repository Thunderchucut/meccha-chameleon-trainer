# Security Policy

## Scope

The MECCHA CHAMELEON Trainer reads and writes process memory of the local
MECCHA CHAMELEON client. It does **not**:

- make outbound network requests (except the optional update check, which can
  be disabled in `config/local.yaml` via `updates.enabled: false`)
- bundle any third-party binaries
- phone home with telemetry

## Reporting

If you find a vulnerability — for example, a DLL search-order hijack in the
injector, or a privilege-escalation path in the overlay driver — please email
`security@meccha-trainer.dev` (PGP key in `docs/pgp.asc`). Do not open a public
issue.

We aim to respond within 72 hours.

## Supported versions

| Trainer | Game build      | Supported |
|---------|-----------------|-----------|
| 2.4.x   | 2026.3.x        | ✅        |
| 2.3.x   | 2026.1.x        | ⚠️ security only |
| < 2.3   | any             | ❌        |

## Known caveats

- The kernel-mode overlay driver (`drivers/chameleon_overlay.sys`) is unsigned
  and will trip HVCI on Windows 11 24H2+. Use the user-mode overlay
  (`core/overlay.py`) instead unless you know what you're doing.
- The `spoofer` module is provided for offline testing only. Do not use it on
  live servers — you will be banned.