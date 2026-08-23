# OpenCode Handoff — Luana-PC Client-Side Analysis & Fix

## Context

You are running on **Luana-PC** (Windows 11, joined to the Tailscale tailnet `weissvanderpol.ivan@` as node `luana-pc`, Tailscale IP `100.97.67.105`).

Hermes Desktop (Electron win-unpacked, build stamp `05cbddc01234` from `main`) is installed at HERMES_HOME=`C:\Users\Luana\AppData\Local\hermes`.

**Mission:** Analyze the Luana-PC side of the Hermes remote-gateway connection. Diagnose why Hermes Desktop cannot reach `https://hermes.paragu-ai.com/p/kiki/v1`, fix any client-side issues you find, and confirm end-to-end connectivity once the server-side fix lands.

---

## Section 1 — Target (already configured on server side, in progress)

- **Gateway URL:** `https://hermes.paragu-ai.com/p/kiki/v1`
- **Auth:** Bearer token (kiki profile)
- **Bearer (sensitive — do not log):** `abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016`

The bearer IS the right value for kiki — it is kiki's `API_SERVER_KEY`. **Do NOT regenerate it.** The client already has it in `%APPDATA%\Hermes\connection.json`.

DNS for `hermes.paragu-ai.com` resolves to `38.9.96.179` (Host A, paragu-ai, raw origin — NOT Cloudflare-proxied). Host A runs Traefik v3.7. The server team is adding a Traefik router + service that proxies to the Hermes gateway on Host B (Tailscale IP `100.78.180.49:8642`) and issues a real Let's Encrypt cert (replacing the current `TRAEFIK DEFAULT CERT` self-signed).

---

## Section 2 — Client config that is ALREADY done (do NOT undo)

These client-side fixes have been applied and verified. Do not re-edit unless something is clearly wrong:

- `%APPDATA%\Hermes\connection.json` rewritten: URL → `https://hermes.paragu-ai.com/p/kiki/v1`, `authMode: token`, bearer stored, `"encoding": "plain"` (supported by `decryptDesktopSecret` in `main.cjs:4700`).
- Old URL `https://webui.paragu-ai.com` was removed.
- Hermes Desktop restarted; `desktop.log` confirms it now dials the correct URL.
- Old error "could not read served dashboard token: 404" was expected (headless `hermes serve` has web UI disabled; client falls through to remote) and is gone.

If you see "could not read served dashboard token" again, it's a regression — re-check `connection.json`.

---

## Section 3 — Remaining client-side error (current symptom)

**TLS handshake fails with `unable to verify the first certificate`** (Node TLS validation rejecting the server's cert).

This is NOT a client config issue. The fix is server-side (real LE cert). However, until that lands, the client cannot complete the handshake.

**Two acceptable paths:**

**PATH A (preferred, what we're working toward on the server):**
Server issues a real LE cert for `hermes.paragu-ai.com` → Desktop validates against system CA → handshake succeeds → **NO client-side workaround needed.**

**PATH B (temporary, ONLY if you must validate the client pipeline before the server cert is live):**
Pin the cert in Hermes Desktop's TLS layer. Allowed ONLY as a temporary measure during the rollout window. **Do NOT do this long-term** — the bearer travels over a validated channel only.

**NEVER use any of these:**
- `NODE_TLS_REJECT_UNAUTHORIZED=0`
- `--use-system-ca` quirks
- Self-signed CA pinning to a private cert

If the server cert is live and you STILL see "unable to verify the first certificate", that's a real bug — investigate SNI mismatch or chain issues. Diagnose via:
```
openssl s_client -servername hermes.paragu-ai.com -connect hermes.paragu-ai.com:443
curl -v https://hermes.paragu-ai.com/p/kiki/v1/api/status -H "Authorization: Bearer <bearer>"
```

---

## Section 4 — Files to inspect (do this first, in order)

1. **`C:\Users\Luana\AppData\Roaming\Hermes\connection.json`** — confirm URL, bearer, authMode are exactly as in Section 1; confirm `"encoding": "plain"`.

2. **`C:\Users\Luana\AppData\Local\hermes\logs\desktop.log`** — look for `[boot] Remote Hermes backend is ready`. Look for `failed liveness probe` or `unable to verify the first certificate`. If you see `ENOTFOUND` or `ECONNREFUSED`, that's a network issue (firewall blocking outbound 443 or DNS not resolving). Tail the last 200 lines.

3. **`C:\Users\Luana\AppData\Local\hermes\main.cjs`**:
   - **Line ~4700:** `decryptDesktopSecret(bearer, encoding)` — confirm `"plain"` encoding is supported.
   - **Line ~3935:** `waitForHermes` — remote probe lives here. If timeout/retry/backoff is tight, the client may give up before the server is reachable.
   - **Line ~5543:** `replyWithError` — `EPIPE → Electron dialog originates here`. Dialog loop will resolve itself once server is reachable.

4. **Tailscale state** — typically `C:\Users\Luana\AppData\Roaming\Hermes\Tailscale\state` or wherever Tailscale stores it. Confirm tailscaled is connected and luana-pc has 100.97.67.105. From PowerShell: `tailscale status`. Ping test: `ping 100.78.180.49` (Host B tailnet IP — should respond). If tailscale is not running, public internet fallback to `hermes.paragu-ai.com` should still work once LE cert is live.

5. **Windows Firewall rules** — confirm outbound 443 is allowed:
   ```
   Get-NetFirewallRule | Where-Object {$_.Enabled -eq 'True' -and $_.Direction -eq 'Outbound' -and $_.Action -eq 'Allow'} | Select-Object DisplayName, Profile
   ```

---

## Section 5 — Diagnostic commands (run on Luana-PC, in PowerShell as user)

```powershell
# 1. Confirm URL reachable
Test-NetConnection -ComputerName hermes.paragu-ai.com -Port 443

# 2. Confirm DNS resolution
Resolve-DnsName hermes.paragu-ai.com

# 3. TLS handshake + cert (THE diagnostic for the cert issue)
openssl s_client -servername hermes.paragu-ai.com -connect hermes.paragu-ai.com:443 | openssl x509 -noout -subject -issuer

# 4. Auth path end-to-end
curl -v https://hermes.paragu-ai.com/p/kiki/v1/api/status -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016"

# 5. Chat path end-to-end
curl -sS -m 30 -X POST https://hermes.paragu-ai.com/p/kiki/v1/chat/completions `
  -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" `
  -H "Content-Type: application/json" `
  -d '{"model":"nvidia-llama-8b","messages":[{"role":"user","content":"ping"}],"max_tokens":20}'

# 6. Tailscale health
tailscale status
ping 100.78.180.49

# 7. Local firewall
Test-NetConnection -ComputerName hermes.paragu-ai.com -Port 443 -InformationLevel Detailed

# 8. DNS cache flush (if DNS stale)
ipconfig /flushdns
Resolve-DnsName hermes.paragu-ai.com
```

**Expected responses:**
- **Test 1:** `TcpTestSucceeded=True`
- **Test 2:** returns `38.9.96.179` (raw origin) — NOT a Cloudflare IP
- **Test 3:** `subject=CN=hermes.paragu-ai.com`, `issuer=CN=R10/R11/etc` (Let's Encrypt) — **NOT "TRAEFIK DEFAULT CERT"**
- **Test 4:** HTTP 200, JSON with `version`, `served_profiles` including `kiki`
- **Test 5:** HTTP 200, JSON with `choices[].message.content` (no 402/429)
- **Test 6:** `100.97.67.105 luana-pc, active; direct`. Tailscale IP confirmed.
- **Test 7:** outbound 443 allowed (no `Blocking` action)
- **Test 8:** same as Test 2 after flush

If Test 3 returns "TRAEFIK DEFAULT CERT", the server-side cert has NOT been issued yet — wait and retry. If Test 5 returns 401, the bearer doesn't match kiki's `API_SERVER_KEY` — escalate.

---

## Section 6 — Acceptance checks (once server is fully fixed)

User's stated acceptance criteria. Run all six and report actual output (don't summarize):

```powershell
# Check 1: /p/kiki/v1/api/status with bearer → 200 with JSON
curl -sS -o /dev/null -w '%{http_code}\n' https://hermes.paragu-ai.com/p/kiki/v1/api/status -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016"

# Check 2: cert subject CN=hermes.paragu-ai.com, issuer NOT "TRAEFIK DEFAULT CERT"
echo | openssl s_client -servername hermes.paragu-ai.com -connect hermes.paragu-ai.com:443 2>$null | openssl x509 -noout -subject -issuer

# Check 3: same over tailnet
curl --resolve hermes.paragu-ai.com:443:100.79.181.37 -sk -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" https://hermes.paragu-ai.com/p/kiki/v1/api/status

# Check 4: webui.paragu-ai.com /api/status with bearer → 200
curl -sS -o /dev/null -w '%{http_code}\n' https://webui.paragu-ai.com/api/status -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016"

# Check 5: desktop.log shows [boot] Remote Hermes backend is ready, NO failed liveness probe lines.
Get-Content "$env:LOCALAPPDATA\hermes\logs\desktop.log" -Tail 200 | Select-String -Pattern "Remote Hermes backend|failed liveness probe|unable to verify"

# Check 6: Hermes Desktop UI loads, shows kiki profile, renders model list, chat returns a real completion.
```

**Pass criteria:**
- Checks 1, 3, 4 → HTTP 200
- Check 2 → subject `CN=hermes.paragu-ai.com`, issuer contains `Let's Encrypt` (R10/R11/R12/E1/E5/E6)
- Check 5 → `[boot] Remote Hermes backend is ready` present, NO `failed liveness probe` lines
- Check 6 → UI loads, profile = `kiki`, model list non-empty, chat test returns real completion

---

## Section 7 — EPIPE / Dialog loop (if client is in crash loop)

**Symptom:** Hermes Desktop repeatedly shows `Uncaught Exception` / EPIPE dialog even though underlying issue is the server.

**Root cause:** Five `Hermes.exe` processes from a 15:18 restart batch never connected to any backend. Renderer fires `hermes:api` IPC → main process catches failure → tries to reply → renderer's pipe is closed → EPIPE → Electron surfaces as Uncaught Exception → dialog.

**This resolves itself when the server is reachable.** While waiting:

- **Option 1:** Wait for server fix. Click OK each dialog. Restart Hermes Desktop after server is up.
- **Option 2:** Kill all Hermes processes via Task Manager → silence dialog loop → reopen after server up.
- **Option 3 (NOT recommended):** Switch `connection.json` to mode `"local"`. Local backend uses default keys, NOT kiki's. Kiki's API keys are server-side, so local mode = no chat at all for kiki. **Only do this as last resort with explicit user consent.**

---

## Section 8 — Tailscale / network troubleshooting

If `Test-NetConnection` fails or DNS doesn't resolve, the issue is local:

**Tailscale status:**
```
tailscale status
```
Confirm: `100.97.67.105 luana-pc, active; direct`. If `offline`, daemon not running — start it from Start Menu or `C:\Program Files\Tailscale\tailscale.exe status`. **Old expired key warning:** `ai-whisperers-server` key expired Aug 9 2026 — re-auth via login link if needed.

**Windows Firewall blocking outbound 443:**
```
Test-NetConnection -ComputerName hermes.paragu-ai.com -Port 443 -InformationLevel Detailed
```
If blocked, allow via Windows Defender Firewall with Advanced Security.

**DNS cache stale:**
```
ipconfig /flushdns
Resolve-DnsName hermes.paragu-ai.com
```

**ISP/CGNAT issue:** Try phone hotspot. If that works, issue is local network.

---

## Section 9 — What you must NOT do

- **Do NOT modify server-side files** (Host A or Host B). That's a parallel agent.
- **Do NOT regenerate the bearer.** It is kiki's profile `API_SERVER_KEY`.
- **Do NOT switch to `NODE_TLS_REJECT_UNAUTHORIZED=0`** — bearer must travel over a validated channel.
- **Do NOT pin to a self-signed CA long-term.** Only as a temporary measure during cert rollout, and only with explicit user consent.
- **Do NOT modify `main.cjs` asar** unless you've confirmed the issue is in main.cjs and not the server cert (asar is read-only and re-stamping requires re-signing the installer).
- **Do NOT switch `connection.json` to mode `"local"`** unless explicitly asked. Kiki's profile API keys are server-side; local mode = no chat for kiki.

---

## Section 10 — Report back

When done, report:

(a) Confirmation that all six acceptance checks pass with actual curl/openssl/PowerShell output (paste outputs, don't summarize).

(b) Anything that needed fixing on the client side and how you fixed it.

(c) Status of chat-routing-bug verification: did Test 5 return a real completion or 402? If 402, escalate — that's the litellm `primary` model chain being out of credits (Cerebras/Mistral 402, OpenRouter free tier 429). Working models currently: `nvidia-llama-8b`, `zai-glm-4-flash`, `fast`, `vision`.

(d) Any follow-up needed on the server side that's beyond your scope.

---

## Quick reference — bearer & URLs

| Item | Value |
|---|---|
| Gateway URL | `https://hermes.paragu-ai.com/p/kiki/v1` |
| Bearer (kiki) | `abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016` |
| DNS | `hermes.paragu-ai.com → 38.9.96.179` (raw origin) |
| Host A (paragu-ai) | `38.9.96.179` / Tailscale `100.79.181.37` |
| Host B (hermes) | `38.9.96.180` / Tailscale `100.78.180.49` |
| Gateway port | `8642` (loopback on Host B until fixed) |
| WebUI URL | `https://webui.paragu-ai.com/api/status` |
| HERMES_HOME | `C:\Users\Luana\AppData\Local\hermes` |
| Connection config | `%APPDATA%\Hermes\connection.json` |
| Desktop log | `%LOCALAPPDATA%\hermes\logs\desktop.log` |
