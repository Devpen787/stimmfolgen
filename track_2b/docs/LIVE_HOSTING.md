# Live serving and hosting decision — 15 October 2026

## User constraints

- Visitors use a web browser on phone or computer, with no model installation.
- The user's Mac is private, only for their own use/testing. Never expose/tunnel it for visitors.
- No owner or visitor payments. Do not activate paid products, attach payment methods or present a finite credit allowance as perpetual free service.
- Swiss sovereign deployment is the target architecture; moving a demonstration outside Switzerland needs a clearly disclosed decision.

## What exists

A local browser-to-real-Apertus path is implemented and observed. It is bounded to reviewed historical AHV facts, and live quality work remains. Default `make run` still serves the reviewed case honestly when inference is not configured. A limited public URL now exists; see the dated continuation below.

The optional `deploy/compose.yml` + Caddy configuration is a prepared **paid-provider alternative, not activated or currently selected under the zero-payment requirement**. It hosts the app on a Swiss VPS and uses Infomaniak's Swiss-hosted Apertus v1.5 70B API. Provider-reported IDs are checked; this does not attest the provider's weight bytes, exact revision or quantization. Hosted generation has not been tested without credentials. Private state stays in the browser; only explicit public questions go to inference.

## Verified provider facts and trade-offs

Checked 15 October 2026, primary sources:

- [Infomaniak AI Services prices](https://www.infomaniak.com/en/hosting/ai-services/prices): Apertus v1.5 70B CHF 0.70/million input tokens, CHF 2.50/million output tokens. [VPS Lite](https://www.infomaniak.com/en/hosting/vps-lite): 2 vCPU/4 GB/60 GB tier CHF 7.20/month equivalent, **annual commitment paid upfront (CHF 86.40)**; final taxes/checkout require review. This is not free. [AI Services getting started](https://www.infomaniak.com/en/support/faq/2845/getting-started-guide-ai-services-sovereign-ai-services) requires a credit card and offers spending limits.
- [Public AI](https://publicai.ch/): free browser chat, API billed separately. [Developer portal](https://platform.publicai.co/docs) provides $2 starter credit; finite, not recurring free hosting. Website/API/model route data residency must be checked for the actual chosen endpoint; do not infer it from the model's Swiss origin.
- [Euria](https://news.infomaniak.com/en/euria-sovereign-ai-assistant/): free consumer browser service, Switzerland hosted. [Apertus selection guide](https://www.infomaniak.com/en/support/faq/2924/discover-euria-and-the-apertus-model). Consumer chat is not an integration API; do not automate it as an undocumented free backend.
- [Hack Apertus resources](https://hackapertus.notion.site/resources-tools), read through the actual browser: new CSCS API key requests closed 6 October, 18:40 CEST; new Phoeniqs compute applications closed 4 October, 20:30 CEST. Hugging Face $10 credits sign-up is listed. Existing allocated access may still work; none is configured here. Credits and availability after the event are not established permanent hosting.
- [Riserbo](https://devpost.com/software/riserbo): another Track 2B entrant describes local llama.cpp/Docker, offline execution and a recorded demo; this does not establish a public SaaS.
- [Apertus Azure example](https://github.com/francesco-sodano/aca-apertus1.5-8B): separate browser application/private GPU inference, subscription/quota requirements; paid infrastructure, not free Swiss hosting.

## Original access decision (superseded by the continuation below)

First use any already-allocated organiser access, if the owner has it. Otherwise, a zero-charge limited demo needs free compute/credits and a provider-approved integration. A free non-Swiss host must be disclosed separately from Swiss-deployable architecture. Sustainable zero-payment Swiss-only hosting needs sponsorship or donated infrastructure; none is confirmed. No public deployment can be marked complete until an actual host and inference credential exist and the full remote journey passes.

## Optional Infomaniak deployment (inactive)

Only after an explicit paid-service decision: provide a VPS with Docker/Compose and SSH key access, DNS hostname with A/AAAA pointing to it, restricted AI Services product ID/token, and a provider spending limit. Never put tokens in chat, Git or browser code.

Place the token in `/opt/stimmfolgen-secrets/infomaniak_token`, owned by UID 10001, mode 0400. Copy `track_2b/deploy/env.example` to ignored `.local/deploy.env` and set hostname, product ID and token-file path. Run from root:

```sh
docker compose --env-file .local/deploy.env -f track_2b/deploy/compose.yml up -d --build
```

Only Caddy publishes ports 80/443. It replaces the client-IP header; backend proxy trust is enabled only in this closed Compose network. Do not publish app port 8770 when proxy trust is enabled. Caddy obtains a normal public certificate; never bypass browser certificate warnings. No access log is enabled. Persistent aggregate daily quotas cap questions (default 200/day); keyed per-network buckets live for five minutes in memory; provider spending limit remains the billing control. The backend has no voter account or question database. This configuration still requires actual deployment, HTTPS, provider, restart and phone verification.

## Local-only reproduction

Start the already-installed MLX v1.5 model on `127.0.0.1:8766`, then:

```sh
.venv/bin/python track_2b/src/app/backend.py \
  --source-pdf .local/gate0/release-booklet.pdf \
  --local-model-dir .local/models/apertus-v1.5-8b-mlx-4bit --port 8780
```

Open `http://127.0.0.1:8780/`. This is for the owner's testing only. It is not public hosting or a phone-access URL on another device.

Direct browser check on 15 October: `https://euria.infomaniak.com/` presented an anonymous question form. Its model selector listed Fast, Expert and **Apertus 1.5**; selecting Apertus returned to the form with Apertus selected, while Sign up/Log in remained optional controls. No message was submitted or terms accepted. `https://chat.publicai.co/` redirected to its sign-in page with Continue with Public AI. These observations establish the consumer access UI, not an integration API, SLA or tested response.

## Selected and deployed - 15 October continuation

Public URL: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/ . The user approved the seven-day Public AI key and scoped official Wrangler authorization. The key is stored outside Git and as a Worker secret. No paid plan, card, top-up or custom-domain DNS was configured. The automatically allocated workers.dev hostname is the demo address.

**Cost:** Cloudflare Free within its included quotas plus existing Public AI starter credits. Actual advertised v1.5 8B pricing: USD 0.10/million input tokens and USD 0.20/million output tokens. The demo caps 200 shared reservations for its lifetime, 80/day, six per five minutes per network and one active inference pair. Each call has a 16,000-byte prompt bound; output caps are 850+200 tokens. Approximately USD 0.70 is a conservative total-token ceiling for 200 pairs at these prices, including prompt overhead; other wallet use/provider policy may exhaust credit sooner. Price changes fail closed. Reservations include failed requests and are not refunded; no auto-reset on deployment. The seven-day key is an additional availability limit.

**Trade-off:** Cloudflare is globally hosted and Public AI processing/residency is not attested here. This is explicitly NOT Swiss-sovereign hosting. On-premise deployability is provided by the separately tested loopback-only local mode. The inactive paid Swiss configuration remains an alternative, not the selected demo.

**Model selection:** real 70B requests returned upstream 429s five times; 8B is actually available and was selected explicitly, not silently substituted per request. Strict model ID and bounded-price checks run before each pair. Raw surviving failures and all current trials are retained. See [proof](evidence/hosted-local-2026-10-15/REVIEW.md).

To reproduce the hosted build: authenticate the source, run `python track_2b/tools/export_hosted.py --source-pdf /path/to/booklet.pdf --check`, then `npm ci --ignore-scripts --prefix track_2b/hosted`. Run `node track_2b/hosted/prepare-assets.mjs` to stage only public web files and the hash-verified demo, then run the local Wrangler deploy command with the approved account environment and secret. Checked-in LIVE_ENABLED defaults false; only explicitly configured deployments enable it. Never commit `.dev.vars`, `.wrangler` state or secrets. Runtime application logs do not retain questions; provider/platform retention is outside this application's control.
