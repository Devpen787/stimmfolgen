# ADR 0003 — compare extracted actors before answering attribution requests

Date: 2026-10-12. Status: adopted for the bounded Gate 0 diagnostic; frontend blocked.

The v3 model selected authentic committee passages for a government forecast. A v4 neutral extraction correctly found the government forecast, but a subsequent model answer still changed its speaker to the requested committee. Source-first prompt reordering also regressed the cost units. Both failures are retained.

For attribution tasks, separate neutral source discovery from parsing the requested attribution. Apertus independently selects the forecast spans and their source actor without the user's speaker premise, then parses the requested speaker from the question without source evidence. Mechanically validate both strict outputs. The application compares the two extracted actors: equality produces `SUPPORTED`, inequality produces `SOURCE_CONFLICT`; malformed, ambiguous or unsupported actor references are withheld. Preserve the actual extracted actor and span IDs unchanged. Neither step nor the comparator receives the semantic oracle, expected actor, expected outcome or a fixed source ID.

This replaces a vulnerable generative answer step with an explicit policy boundary. It is not a corrected or silently rewritten model response. The composed attribution result is marked `POLICY_COMPARISON_OF_TWO_ACTUAL_MODEL_COMPLETIONS`; both raw responses and their hashes remain available. A separate unchanged primary-source oracle still checks that the chosen spans actually support the forecast; actor matching alone cannot establish meaning. Synthetic tests cover both actors in all four equal/unequal combinations and reject unrelated citations. Six non-attribution prompts remain byte-identical to v3.

Two unchanged final local Apertus v1.5 suites pass all seven bounded trials and the three-response happy-path aggregate. The attribution outcome is application-computed, not an LLM-generated refusal. This single AHV development case, targeted retrieval and coding-agent-authored reference do not prove generalisation or human semantic review. Publication availability and human review remain outstanding; frontend work stays blocked.

Evidence: [attribution continuation](../evidence/GATE0_ATTRIBUTION_2026-10-12.md). Earlier [failed spans](../evidence/GATE0_SPANS_2026-10-12.md) remain unchanged.
