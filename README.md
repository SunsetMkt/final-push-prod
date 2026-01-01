# final-push

An inactivity-triggered release system powered by GitHub Actions.

This repository provides a template for automatically releasing predefined content after a prolonged period of GitHub inactivity.

It relies solely on public GitHub activity as a heartbeat signal and executes without external services.

## Configuration

1. Write your own message in `payload.md`
2. Run `utils/enc_payload.py`, get `payload.key` and `payload.enc`
3. Set content of `payload.key` as `PAYLOAD_KEY` secret in GitHub Actions
4. Upload `payload.enc` to this repository
5. **NEVER upload `payload.key` or `payload.md` to anywhere**
6. Edit `config.json`:

-   "username": GitHub username to monitor
-   "inactivity_days": int, days of inactivity to trigger, should less than 89
-   "payload_path": path of `payload.enc`, keep as `payload.enc` if you follow this guide
-   "output_path": decrypted `payload.enc` to this path, keep as `README.md` if you follow this guide
-   "one_shot": bool, whether to trigger only once
-   "handle_404": bool, whether to handle GitHub API 404 as trigger

7. Test the Actions workflow

## `payload.enc` sample for test

```pwsh
$env:PAYLOAD_KEY = "STkNThGBxPs12r308bZX1kBgu4nxAvL46FMxFjyYSUQ="
```

```plain
gAAAAABpVjXDl0UfGnlnEhlJKpoElhAf-Do2rCY6YTcF_f8K-yO22HTV_7TKXIFpKWv02j1TaYBUdYhTCKDLxByW7KwF6G3DrNtOLPEp-OBkmve9Wplw184nlgf98oWSM-g5VHnwXem7
```

## Use cases

-   Dead man's switch
-   Long-term project handoff
-   Lost-access contingency
-   Inactivity-based disclosure

## How it works

-   A scheduled GitHub Actions workflow runs daily
-   Public GitHub activity is checked via the GitHub API
-   Inactivity duration is calculated
-   If a configurable threshold is exceeded:
    -   A predefined payload is decrypted
    -   The payload is published to the repository

## Abort conditions

Any of the following will prevent or reset the trigger:

-   New GitHub activity (for example, star or unstar any repository)
-   Manual state reset

## Security design

No assumptions are made about the user's state. Only inactivity is evaluated.

Fernet is used for convenience, not for long-term archival security.
