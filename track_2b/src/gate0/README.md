# Source authentication and Apertus Gate 0

These tools acquire the pinned official booklet, extract immutable spans, record actual model completions, and validate source and actor attribution. Mechanical validation alone does not establish semantic correctness.

The original local runs include failures. Later source-span and attribution runs, recorded human decisions and the bounded release certificate are retained unchanged in the [evidence index](../../docs/evidence/README.md). The reviewed AHV case passed the release Gate; this does not clear other votes or establish general accuracy.

`source_probe.py` authenticates source bytes; `local_model.py` authenticates the supported MLX identity; `model_probe.py` and `evaluate_local.py` record actual model attempts. Template-guided probes and same-model checks are not independent semantic review. `release_guard.py` binds the admitted case to its immutable packet, decisions and recorded trials.

Use the [run guide](../../docs/JUDGE_RUN.md) for current local setup and the [runtime contract](../../docs/APP_CONTRACT.md) for publication boundaries. Keep weights, credentials and private records outside Git. Default Docker publication replays reviewed evidence; it does not invoke a fresh model completion.
