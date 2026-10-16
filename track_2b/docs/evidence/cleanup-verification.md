# Repository cleanup verification — 16 October 2026

This cleanup changes documentation, evidence organisation, obsolete authoring tools and repository checks. App source, web assets, model contracts and reviewed source data remain unchanged. It does not deploy or merge anything.

## Preservation

- Submitted commit: `9e1c60845c64bbe2b810a08be67fe39d47e96904`; pre-cleanup head: `b49291721afb0f24ddcc4fea324acc3b0caf2625`.
- A full Git bundle and tracked-tree archive were saved outside the public checkout with private filesystem permissions. Bundle validation and both archive SHA-256 checks passed before committing this cleanup.
- [Preserved-file manifest](preserved-files.json): 160 original Gate/source-review files plus the submitted report Markdown/PDF, two video cuts and original captions. All 165 hashes passed. Both report files were also compared directly with the submitted Git object.
- [Selected-trace provenance](local-hosted-verification/trace-provenance.json): 92 already-redacted records retain their exact contents, including failed attempts. Original archives remain in the immutable history and private backup.
- Planning documents, superseded working logs and media production files were removed from the current branch tree. Frozen evidence may retain historical terminology. Original commit author metadata remains in history; new cleanup commits use a GitHub no-reply address.

## Checks after cleanup

- Docker image built successfully; 108 Python tests passed inside its dependency environment.
- 29 compiled Worker tests passed, zero skipped. Provider fixtures are synthetic.
- Actual WebCrypto vault persistence, tamper/wrong-password rejection, reload locking, concurrency and backup recovery passed.
- Offline Docker Gate replay passed; temporary invalid-evidence mutations were blocked; cold HTTP journey passed; hosted export matched authenticated native evidence and prompt contracts.
- Asset staging authenticated both unchanged video files; Wrangler dry-run compiled successfully. No deployment was performed.
- Public HTTPS index and app JavaScript matched the unchanged checked-in assets byte for byte using read-only requests. No new model requests were made.
- Repository hygiene checks passed for current tracked text, selected evidence hashes and curated documentation links. This is not an exhaustive historical secret scan, binary OCR or source-licensing clearance.

The first host-side Python attempt lacked PyMuPDF; it was replaced by the complete passing Docker run. The default Python HTTP user agent received a 403; ordinary browser-agent GETs passed and matched the assets. These environmental failures are retained in private cleanup logs rather than represented as successful tests.

Reproduce with the commands in [the root README](../../../README.md), [judge guide](../JUDGE_RUN.md) and [release workflow](../../../.github/workflows/app-release.yml). The repository hygiene workflow replaces the retired checks for an unimplemented design blueprint; actual backend and source-verification workflows remain in place.
