# Run the verified AHV prototype

From the repository root, with Docker and make installed:

```sh
make run
```

Open http://127.0.0.1:8770. From `track_2b/`, `make run` delegates to the root. Use `make run PORT=8772` if port 8770 is occupied. Stop with Ctrl-C. `make check` independently rechecks the bounded Gate certificate in Docker.

The build retrieves the pinned official PDF and Python base/dependency packages. It fails if the PDF edition/hash differs. No credentials, model download or paid API is needed for the reviewed-case web journey. The container runs as a non-root user with a read-only filesystem, binding only to the host loopback interface. After build it requires no external network: the offline `make check` equivalent is `docker run --rm --network none --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m stimmfolgen:local python track_2b/src/app/backend.py --source-pdf /app/booklet.pdf --check`.

This is **REVIEWED_RECORDED_CASE**, not fresh inference on each click. Actual Apertus v1.5 was used to produce the archived extraction/intent candidates; authenticating those traces does not run the model again. The five published statements were separately accepted by the user. P03's five-year cost is reviewed reference context, visibly labelled.

Try the complete journey:

1. Start with empty My votes: no fabricated personal choice or history.
2. Search AHV, track the past proposal, return to My votes and Explore my vote.
3. Inspect the original passage and source dates; compare Me, Others and Switzerland. Personal CHF cost remains unknown.
4. View the separately dated October 2026 official update and related November financing proposal. Unreviewed votes say analysis is unavailable.
5. Keep a synthetic choice/note for this visit, or explicitly create a passphrase-protected local vault. Reload locks persisted data; unlock restores it.
6. Download an encrypted backup and restore it locally. The backup is not uploaded. A forgotten passphrase cannot be recovered.

For actual **new local inference**, use the existing downloaded MLX weights and compatible native Apple Silicon runtime. See the pinned model/server commands in `docs/evidence/GATE0_SPANS_2026-10-12.md`, then run the current protocol with a new output directory:

```sh
python track_2b/src/gate0/source_probe.py --out .local/gate0/source-new.json --pdf-out .local/gate0/booklet-new.pdf
python track_2b/src/gate0/local_model.py --model-dir "$APERTUS_MODEL_DIR" --base-url http://127.0.0.1:8766/v1 --out .local/gate0/identity-new.json
python track_2b/src/gate0/span_probe.py --source-report .local/gate0/source-new.json --source-pdf .local/gate0/booklet-new.pdf --local-model-report .local/gate0/identity-new.json --availability-record track_2b/docs/evidence/ahv-semantic-review-2026-10-12/publication-availability.json --public-as-of 2024-03-02T23:59:59+01:00 --out-dir .local/gate0/new-unreviewed-run
```

Here `python` must be the compatible prepared environment, not an arbitrary system interpreter. The measured Mac has M3 Pro and 18 GiB RAM; the text-only 4-bit weights occupy 4.53 GB. Fresh model outputs remain unreviewed and never replace published statements automatically. MLX cannot run inside a Linux Docker container on the Mac GPU. The on-premise design separates native model ingestion from Docker-contained reviewed publication.

Limits: one AHV development case; no second-case or unseen-ballot proof, independently audited production security, French/Italian parity, current-law answers or voting recommendations. A cold Docker pass is a replay/publication delivery check, not whole-model portability. No external hosted deployment or submission has been made.
