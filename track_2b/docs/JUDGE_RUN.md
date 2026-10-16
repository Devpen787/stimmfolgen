# Run StimmFolgen

## Live public app

Open https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/ on a phone or computer. No account, payment or model download is required. Search AHV, track it, open Explore my vote and ask about pension recipients or the source of the taxes/spending-cuts argument. The answer resolves to immutable source wording. Open Source and dates, compare perspectives, then save a synthetic private note. Saving after reload requires your own passphrase. Tracked votes and notes are never attached to a model request.

This is a finite-credit global Cloudflare/Public AI demo, not exclusively Swiss hosting or permanently free infrastructure. Shared limits: 200 lifetime reservations, 80/day, six per five minutes per network, one active question. Counts persist across deployments. The temporary API credential needs renewal. No owner's Mac hosts public visitors.

## Actual local inference with a Docker app

Apple Silicon Mac with Docker Desktop, Python 3.11+ and make; tested on M3 Pro, 18 GiB RAM. Allow disk for 4.53 GB weights, Python packages and Docker images. From a new clone, check out the PR branch until main is reviewed:

```sh
git clone https://github.com/Devpen787/stimmfolgen.git
cd stimmfolgen
git checkout codex/local-apertus-gate0-evidence
make onprem-setup
make local-download
make run ONPREM=1 APP_PORT=8784
```

If you already have the pinned MLX directory, skip the download and pass its path to both setup and run using MODEL_DIR. Open http://127.0.0.1:8784/. The launcher verifies the model SHA and served identity, starts native MLX on literal loopback port 8768, builds the authenticated Docker app and binds it only to host loopback. It uses Docker Desktop's host bridge; Mac GPU inference is native, not inside Linux Docker. Ctrl-C stops only processes/containers owned by this launch. Occupied ports fail without stopping an existing service. There is no hosted fallback or API key.

Setup/build require internet; this is on-premise, not an air-gap proof. The actual fresh-clone proof used a new Python environment and no-cache Docker app builds, reusing an APFS copy of already downloaded pinned model bytes. It was on the same Mac, not another physical device or a fresh remote model download. See [installation evidence](evidence/local-hosted-verification/README.md).

## Hardware-free source replay

```sh
make run PORT=8772
make check
```

Open http://127.0.0.1:8772/. Default make run provides the authenticated reviewed explanation without fresh model inference. It needs no model or credentials. The image downloads and hashes the original source during build; the certificate can then be replayed offline. Do not describe this route as a live model run.

## Scope and reproduction

The catalogue contains six selected votes. AHV has accepted analysis and separate later official updates. Homeownership tax reform (28 September 2025) has verified official information and a source-bound four-statement candidate. **Its explanation remains pending the user's wording review and is not in the public registry.** A private localhost preview exercised both cases without admitting the candidate. Its booklet editorial cutoff is not an exact-byte pre-vote availability witness.

Original AHV Gate evidence remains under docs/evidence/gate0-release-2026-10-14. The new known matching evaluations cover 20 local questions (16 questions invoke the real model; four application-policy refusals) and 45 hosted questions. Candidate evaluation is not publication approval. No held-out accuracy, physical phone test, multilingual parity or independent usability study is claimed. Raw failures and successful traces are preserved in the new evidence packet.

Use a public, non-personal question. Explore What it means, Source and dates, Updates, Related votes and Me/Others/Switzerland. Ask for a voting recommendation to observe a deliberate refusal. Track without recording a Yes/No choice. Test encrypted save, reload lock, incorrect passphrase, correct unlock, backup and recovery using synthetic data. Recovery replaces only that browser's vault; forgotten passphrases cannot be recovered. Ordinary screens contain source/uncertainty information; detailed engineering evidence is linked separately from About this demo.

The submitted snapshot is commit `9e1c60845c64bbe2b810a08be67fe39d47e96904`. This branch contains later cleanup and a disclosed post-deadline narration revision; the original submission files remain available. See the [evidence index](evidence/README.md) and [video provenance](../demo/README.md). Main has not been merged. This guide does not attest organiser acceptance of later changes.
