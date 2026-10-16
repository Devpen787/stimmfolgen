# Finite hosted demonstration

Actual public app: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/ . Video: https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/demo . No model download needed. Public AI v1.5 8B is fixed and provider-reported, not weight-attested. Cloudflare globally hosts this demonstration; it is not Swiss-sovereign. The optional native local package supplies the tested on-premise route.

Zero payments were activated. Existing starter credit and a seven-day credential are finite. Server-side limits are 200 lifetime reservations, 80/day and six per five minutes per network, with one active pair. Restarts preserve aggregate counts, not questions/IPs. A price change, wrong model, invalid output or failed meaning check fails closed. The audit uses the same model and is not independent review. No model result automatically changes the human-reviewed overview.

From repository root, with Node 24 and PyMuPDF available, first authenticate and export the public evidence:

```sh
python track_2b/tools/export_hosted.py --source-pdf /absolute/booklet.pdf --check
npm ci --ignore-scripts --prefix track_2b/hosted
node track_2b/hosted/prepare-assets.mjs
track_2b/hosted/node_modules/.bin/wrangler deploy --dry-run --config track_2b/hosted/wrangler.jsonc --outdir /tmp/stimmfolgen-worker
WORKER_BUILD=/tmp/stimmfolgen-worker/worker.js node --test track_2b/hosted/test/*.test.mjs
```

CI authenticates the bundle against the native Gate and exact prompt contract; changing both a JSON file and hash does not bypass that comparison. The fixture provider in tests is synthetic and never implies actual inference. Staging copies only public web assets and the hash-verified MP4/captions. Private local state, runtime and credentials are excluded from Git, Docker context and public assets.

For a separately authorised free-account deployment, sign into official Wrangler with account read, user read, Workers scripts write and background access. Create your own provider key without payment/top-up, save it privately outside Git, and install it using `wrangler secret put PUBLICAI_TOKEN --config track_2b/hosted/wrangler.jsonc` via stdin. Set `CLOUDFLARE_ACCOUNT_ID` for the intended account. `npm --prefix track_2b/hosted run deploy -- --var LIVE_ENABLED:true` stages the assets and deploys. The checked-in default is disabled; an unconfigured deployment serves reviewed sources and an honest unavailable state. No custom domain is required.

Never paste credentials into chat, source files or browser JS. Do not enable a paid plan or use this demo on a user's Mac as a public model server. See [actual evidence and unresolved limits](../docs/evidence/local-hosted-verification/README.md).
