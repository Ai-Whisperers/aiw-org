**SUBJECT: Hermes remote gateway fully down on both Host A and Host B — server-side restore required**

**TL;DR — three independent server-side blockers, none fixable from the client.**
1. Traefik on Host A (`paragu-ai` / public `38.9.96.179`) is serving `CN=TRAEFIK DEFAULT CERT` for `hermes.paragu-ai.com` and 404s every path — no router + no Let's Encrypt cert for that hostname.
2. The actual Hermes gateway service on Host B (`100.78.180.49:8642`) is **not listening** — TCP probe from the client closed, repeated 3× over the session.
3. `webui.paragu-ai.com` (Cloudflare-fronted, valid cert) also 404s on `/api/status` with the same bearer — confirms the gateway service behind it is down/un-routed too.

**CLIENT IS FULLY READY** — `connection.json` is correctly pointing at `https://hermes.paragu-ai.com/p/kiki/v1` with the right `kiki` bearer (`encoding: plain`), desktop restart confirms it dials the right URL, Tailscale is up (`luana-pc` 100.97.67.105). Stop suggesting client changes; every safe local option is exhausted.

---

### 1. Environment

- **Client:** Windows 11, Hermes Desktop (Electron win-unpacked, build `05cbddc01234` from `main`), `HERMES_HOME=C:\Users\Luana\AppData\Local\hermes`.
- **Tailnet:** `weissvanderpol.ivan@`. Client is `luana-pc` (100.97.67.105). Server nodes seen as online: `hermes` (100.78.180.49) and `paragu-ai` (100.79.181.37).
- **Target gateway:** `https://hermes.paragu-ai.com/p/kiki/v1`, bearer-token auth, profile `kiki`.
- **Bearer (SENSITIVE — owner-issued, do not log):** `abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016`

### 2. Diagnostic evidence (captured from client, all fresh)

```
TCP hermes.paragu-ai.com:443           -> reachable
DNS  hermes.paragu-ai.com              -> 38.9.96.179 (raw origin, NOT CF-proxied)
CERT subject/issuer (port 443)         -> CN=TRAEFIK DEFAULT CERT (self-signed, expires 2027-08-20)
                                        SAN does NOT include hermes.paragu-ai.com
GET /p/kiki/v1/api/status  (strict)    -> TLS handshake rejected (Unable to verify first certificate)
GET /p/kiki/v1/api/status  (curl -k)   -> HTTP 404 "404 page not found"
GET webui.paragu-ai.com/api/status     -> HTTP 404 (CF cert valid, app behind it down)
TCP 100.78.180.49:8642  (Host B gw)    -> CLOSED (3× attempts)
SSH weissvanderpol.ivan@100.78.180.49  -> "tailnet policy does not permit you to SSH as user weissvanderpol.ivan"
SSH weissvanderpol.ivan@100.79.181.37  -> same denial
```

### 3. Required server-side actions (in this order)

**(a) Bring up the gateway service on Host B.**
```bash
# on 100.78.180.49 (or whatever node actually hosts it):
ss -ltnp | grep -E ':(8642|64204|3000|8080|8081|8443)\b' || echo "no listener"
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' | grep -i hermes || echo "no hermes container"
# Start it; confirm it listens on the agreed port (likely 8642):
systemctl status hermes-gateway || docker compose -f /opt/hermes/docker-compose.yml up -d
curl -sS http://127.0.0.1:<port>/api/status   # must return JSON, not 404
```

**(b) Add Traefik router + Let's Encrypt cert on Host A (`paragu-ai`).**
```yaml
# on the gateway container / compose file:
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.hermes.rule=Host(`hermes.paragu-ai.com`) && PathPrefix(`/p/kiki`)"
  - "traefik.http.routers.hermes.entrypoints=websecure"
  - "traefik.http.routers.hermes.tls.certresolver=le"
  - "traefik.http.services.hermes.loadbalancer.server.port=<internal-port>"
  # Host B is reachable over Tailscale (100.78.180.49) — use that as server URL:
  - "traefik.http.services.hermes.loadbalancer.server.url=http://100.78.180.49:8642"
```
Traefik static config must have a working `certificatesResolvers.le.acme` (HTTP-01 or DNS-01; Cloudflare DNS-01 recommended since you already use CF). Reload Traefik and watch for cert issuance in its logs.

**(c) Restore `webui.paragu-ai.com` route.** Same root cause — gateway service is un-routed behind CF. Fix while you're in there.

**(d) Fix the chat-routing bug.** `kiki` profile currently routes to a model with depleted credits. Switch the `kiki` profile's primary chain to a model with available quota. Working models from the prior config: `nvidia-llama-8b`, `zai-glm-4-flash`, `fast`, `vision`. Confirm with the chat-completion curl below.

**(e) (Optional but recommended) Allow `luana-pc` to SSH into the tailnet boxes for future debug.** Right now policy denies SSH for `weissvanderpol.ivan` user — if that's wrong, fix the ACL so authorized clients can remote-debug without you in the loop.

### 4. Acceptance checks (run these and paste output verbatim)

```bash
# 1. Gateway status
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" \
  https://hermes.paragu-ai.com/p/kiki/v1/api/status

# 2. Cert subject/issuer (must NOT be TRAEFIK DEFAULT CERT)
echo | openssl s_client -servername hermes.paragu-ai.com -connect hermes.paragu-ai.com:443 2>/dev/null \
  | openssl x509 -noout -subject -issuer

# 3. Same over tailnet (Host B direct via Traefik on Host A)
curl --resolve hermes.paragu-ai.com:443:100.79.181.37 -sk \
  -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" \
  https://hermes.paragu-ai.com/p/kiki/v1/api/status

# 4. webui route
curl -sS -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" \
  https://webui.paragu-ai.com/api/status

# 5. Chat completion (kiki profile)
curl -sS -m 30 -X POST https://hermes.paragu-ai.com/p/kiki/v1/chat/completions \
  -H "Authorization: Bearer abc936e1e166700d017121a1ea72f4446fce95ece24ede40df7123a81e870016" \
  -H "Content-Type: application/json" \
  -d '{"model":"nvidia-llama-8b","messages":[{"role":"user","content":"ping"}],"max_tokens":20}'

# 6. Tailnet SSH allowed
ssh -o BatchMode=yes weissvanderpol.ivan@100.78.180.49 "hostname && uname -a"
```

Pass criteria: `1,3,4` → 200; `2` → issuer contains `Let's Encrypt` (R10/R11/R12/E1/E5/E6) and subject is `hermes.paragu-ai.com`; `5` → JSON with `choices[].message.content` (no 402/429); `6` → connects.

### 5. Client-side acceptance (run after server checks pass)

- Hermes Desktop `desktop.log` shows `[boot] Remote Hermes backend is ready` and **no** subsequent `failed liveness probe` / `unable to verify first certificate` lines.
- Hermes Desktop UI shows profile `kiki`, renders model list, chat returns a real completion with no error toast.
- No more `Uncaught Exception / EPIPE` dialogs from the renderer.

### 6. Hard constraints (do NOT violate)

- **Do NOT** ask the client to set `NODE_TLS_REJECT_UNAUTHORIZED=0` — bearer must travel over a validated channel.
- **Do NOT** regenerate the bearer. It is `kiki`'s `API_SERVER_KEY`. The client has it in `%APPDATA%\Hermes\connection.json`.
- **Do NOT** pin to a self-signed CA long-term. The Traefik default cert's SAN (`*.traefik.default`) does not include `hermes.paragu-ai.com`, so cert pinning cannot work here without hostname bypass, which is forbidden.
- **Do NOT** tell the client to switch `connection.json` to `mode: "local"` — kiki's provider keys are server-side; local mode = no chat for kiki.

### 7. Once you're done

Paste the actual outputs of checks 1–6 above (don't summarize). The client will retry on next Hermes Desktop restart; no client-side changes needed.
