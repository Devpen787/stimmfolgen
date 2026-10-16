# StimmFolgen

Follow selected Swiss votes, inspect dated sources and keep your own reflections private. Search, My votes and Upcoming votes lead to explanations, official updates, related votes, perspectives and optional encrypted notes. StimmFolgen gives no voting recommendation.

[Open the live app](https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/) · [Video](https://stimmfolgen-demo.stimmfolgen-hosted.workers.dev/demo) · [Technical report](track_2b/StimmFolgen_Report.pdf)

## Run with Docker

```sh
make run
```

Open http://127.0.0.1:8770. Use `make run PORT=8772` for another port. This route authenticates and serves the reviewed AHV explanation without new model inference. Build requires internet to fetch the pinned official source; the resulting evidence check can run offline. The container is non-root and read-only, bound to host loopback.

## Run Apertus locally

Apple Silicon Mac, Docker Desktop, Python 3.11+ and disk space for the 4.53 GB model, Python environment and images. Tested on M3 Pro with 18 GiB RAM.

```sh
make local-download
make run ONPREM=1 APP_PORT=8784
```

Open http://127.0.0.1:8784. Existing pinned weights can be reused with `make onprem-setup MODEL_DIR=/path/to/model` and the same MODEL_DIR on run. Native MLX uses the Mac GPU; the Docker app reaches it through Docker Desktop's host bridge. No inference API credential or hosted fallback is used. Setup/build require internet; this is not an air-gap claim. [Installation and reproduction](track_2b/docs/JUDGE_RUN.md).

## Online service and privacy

The public demo calls Public AI Apertus v1.5 8B through Cloudflare. Visitors need no model download. This is a temporary, finite-credit global service, not exclusively Swiss hosting or permanently free infrastructure. Persistent limits are 200 lifetime reservations, 80/day, six per five minutes per network and one active question. The local Mac is not exposed to visitors.

Only the explicitly submitted public question goes to inference. Tracked votes, choices, notes, search and selected perspectives stay on the device. Persistent notes require an optional passphrase-encrypted browser vault; reload locks it. There is no account, sync or passphrase recovery. [Runtime contract](track_2b/docs/APP_CONTRACT.md) · [Privacy threat model](track_2b/docs/PRIVATE_TRACKER_THREAT_MODEL.md).

## Verification and limits

One human-reviewed historical AHV analysis is published. The six-entry catalogue is incomplete. A second real homeownership-tax booklet has source-bound candidates and engineering tests, but its analysis remains unpublished pending human review.

Recorded known development sets passed 20/20 locally (16 questions invoke Apertus; four application refusals) and 45/45 hosted. These are inspected development cases, not held-out accuracy. The fresh local installation reused verified downloaded weights on the same Mac. Browser checks are agent-operated responsive tests, not physical-phone or independent-user research. [Verification index and preserved failures](track_2b/docs/evidence/README.md).

```sh
python -m unittest discover -s track_2b/tests -p 'test*.py'
node track_2b/tests/test_private_vault.mjs
node --test track_2b/hosted/test/*.test.mjs
python track_2b/tools/check_repository.py
make check
```

The hosted suite's workerd test additionally needs a compiled Worker; the CI workflow builds it and runs that test without a skip. Synthetic-provider tests prove application boundaries, not model inference.

## Submission and repository scope

This project follows the [Track 2B template requirements](track_2b/README.md). The submitted source is immutable commit [9e1c608](https://github.com/Devpen787/stimmfolgen/tree/9e1c60845c64bbe2b810a08be67fe39d47e96904). Its five-page PDF and Markdown are retained unchanged. The current PR removes working/planning documents and redundant media; the complete original history and evidence also have a verified private backup. The current branch contains the implementation; default main is not yet updated.

The video page retains the original submitted 115-second synthetic-narration cut alongside a 119.5-second participant-audio revision published after the deadline. Organiser acceptance of the later revision is not established. This cleanup makes no new submission or accuracy claim and does not alter the submitted commit.

Code is Apache-2.0; third-party material has separate terms. [Licence](LICENSE) · [Third-party notices and unresolved source-image redistribution basis](THIRD_PARTY_NOTICES.md).
