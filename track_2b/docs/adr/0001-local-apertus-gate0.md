# ADR 0001 — use verified local Apertus without relaxing the checkpoint gate

Date: 2026-10-12. Status: adopted for the Gate 0 diagnostic, not product release.

The Mac has an existing 4-bit MLX Apertus-8B-Instruct-2509 conversion and a compatible runtime. It has no observed v1.5 weights. The source/model probe rejected MLX's genuine `default_model` alias, while its name-prefix guard could accept invented Apertus identifiers.

Use a dedicated loopback MLX server with the existing runtime and local weights. Admit its alias only after checking the supported conversion's pinned weight digest, metadata/configuration and advertised runtime path. Recheck local artifacts before requests. Keep AutoBots and its registries/state read only. Require original pinned PDF bytes to authenticate source-report excerpts.

The 2509 checkpoint runs only under explicit legacy diagnostic mode. It cannot pass the v1.5 gate, regardless of output quality. Preserve failed raw responses and mechanical findings; matching quotes do not prove meaning. Keep outputs candidate/unreviewed or withheld, and require human semantic review. Do not build the frontend on this evidence.

After inspecting the existing assets and hardware, a feasible pinned v1.5 text-only MLX conversion was downloaded and its complete weight digest/runtime binding verified. The explicit permission condition for a hardware-infeasible replacement did not apply. Independent equivalence to the official BF16 checkpoint remains untested. Actual v1.5 trials still fail Gate 0. This preserves the distinction between local inference proof, source grounding, checkpoint qualification and product readiness.

Evidence: [observed report](../evidence/GATE0_APERTUS_V15_2026-10-12.md).
