"""Inspect cached MLX weights and bind the known MLX default alias to loopback.

Download metadata is local provenance, not an authenticated remote attestation.
Only explicitly inspected, digest-pinned conversions are supported.
"""
import argparse
import hashlib
import json
import re
import struct
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

MODEL_ID = "mlx-community/Apertus-8B-Instruct-2509-4bit"
CHECKPOINT = "swiss-ai/Apertus-8B-Instruct-2509"
REVISION = "c5e6ae2e52c4149f36cb8e47b7ab1489ef885fed"
WEIGHTS_SHA256 = "bcde62001035dd38e9a8b2642f29e0d7b98ef7a6e69b50a6e55be26a8b1c0a9a"
SUPPORTED = {
    CHECKPOINT: {"model_id": MODEL_ID, "revision": REVISION, "weights_sha256": WEIGHTS_SHA256,
                 "heading": f"# {MODEL_ID}", "v1_5": False, "max_position_embeddings": 65536},
    "swiss-ai/Apertus-v1.5-8B": {
        "model_id": "tokimoa/apertus-v1.5-8b-mlx-4bit",
        "revision": "f08ed532a657bef7d322bd0cbca43dac13a9d0a3",
        "weights_sha256": "d0478edeb06bf18e5f4f7b50db77d89b839730b2d16cb1020015e6099e42074b",
        "heading": "# Apertus-v1.5-8B (MLX 4bit, text LM)", "v1_5": True,
        "max_position_embeddings": 262144,
        "declared_upstream_revision": "a411d838600baf0e3635a3daf66fb7c55fc97bb6",
    },
}

def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def endpoint_url(base_url):
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Expected an HTTP(S) endpoint")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("Endpoint must not contain credentials, query or fragment")
    if parsed.path not in {"", "/", "/v1", "/v1/"}:
        raise ValueError("Expected endpoint root or /v1")
    return f"{parsed.scheme}://{parsed.netloc}/v1"

def is_loopback(base_url):
    return urlsplit(endpoint_url(base_url)).hostname in {"127.0.0.1", "localhost", "::1"}

def inspect(model_dir, base_url):
    directory = Path(model_dir).expanduser().resolve(strict=True)
    endpoint = endpoint_url(base_url)
    if not is_loopback(endpoint):
        raise ValueError("Local model evidence requires a literal loopback host")
    config = json.loads((directory / "config.json").read_text())
    card = (directory / "README.md").read_text()
    matches = [checkpoint for checkpoint in SUPPORTED if re.search(
        r"^base_model:\s*" + re.escape(checkpoint) + r"\s*$", card, re.M)]
    if len(matches) != 1:
        raise ValueError("Cached model card does not identify the supported Apertus checkpoint")
    checkpoint = matches[0]
    profile = SUPPORTED[checkpoint]
    if (profile["heading"] not in card or config.get("model_type") != "apertus" or
        config.get("max_position_embeddings") != profile["max_position_embeddings"]):
        raise ValueError("Model card/config identity mismatch")
    if config.get("quantization") != {"group_size": 64, "bits": 4, "mode": "affine"}:
        raise ValueError("Expected the inspected 4-bit MLX conversion")
    metadata = (directory / ".cache/huggingface/download/model.safetensors.metadata").read_text().splitlines()
    if metadata[:2] != [profile["revision"], profile["weights_sha256"]]:
        raise ValueError("Conversion download revision/weight digest mismatch")
    artifacts = {}
    names = ["README.md", "config.json", "model.safetensors", "model.safetensors.index.json", "tokenizer.json", "tokenizer_config.json"]
    names += [name for name in ("chat_template.jinja", "generation_config.json", "special_tokens_map.json") if (directory / name).exists()]
    for name in names:
        path = directory / name
        artifacts[name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    if artifacts["model.safetensors"]["sha256"] != profile["weights_sha256"]:
        raise ValueError("Weight bytes do not match the pinned conversion")
    with (directory / "model.safetensors").open("rb") as source:
        size = struct.unpack("<Q", source.read(8))[0]
        if size > 16 * 1024 * 1024:
            raise ValueError("Unexpected safetensors header size")
        header = json.loads(source.read(size))
    if header.get("__metadata__", {}).get("format") != "mlx":
        raise ValueError("Weights are not in MLX safetensors format")
    with urllib.request.urlopen(endpoint + "/models", timeout=10) as response:
        models = json.load(response)
    if str(directory) not in {item.get("id") for item in models.get("data", [])}:
        raise ValueError("MLX endpoint does not advertise the inspected local path")
    return {
        "evidence_class": "LOCAL_MODEL_INSPECTION", "observed_at_utc": datetime.now(timezone.utc).isoformat(),
        "model_id": profile["model_id"], "backing_checkpoint": checkpoint,
        "source_revision": profile["revision"], "declared_upstream_revision": profile.get("declared_upstream_revision"),
        "served_alias": "default_model", "base_url": endpoint,
        "model_dir": str(directory), "format": "MLX safetensors", "quantization": config["quantization"],
        "artifacts": artifacts, "tensor_count": len(header) - 1,
        "v1_5_verified": profile["v1_5"],
        "alias_binding": "mlx_lm.server --model path; /v1/models advertises resolved path; MLX default_model mapping",
        "provenance_limit": "Pinned locally downloaded conversion with publisher-declared base model; no independent conversion-equivalence test or signed runtime attestation",
    }

def validate_identity(identity, model_id, base_url):
    if not is_loopback(base_url):
        raise RuntimeError("Verified local aliases require a loopback endpoint")
    profile = SUPPORTED.get(identity.get("backing_checkpoint"))
    if profile is None:
        raise RuntimeError("Local alias backing checkpoint is not pinned")
    expected = {
        "evidence_class": "LOCAL_MODEL_INSPECTION", "model_id": profile["model_id"],
        "source_revision": profile["revision"], "served_alias": model_id,
        "base_url": endpoint_url(base_url), "v1_5_verified": profile["v1_5"],
    }
    if model_id != "default_model" or any(identity.get(k) != v for k, v in expected.items()):
        raise RuntimeError("Local alias provenance/endpoint mismatch")
    if identity.get("artifacts", {}).get("model.safetensors", {}).get("sha256") != profile["weights_sha256"]:
        raise RuntimeError("Local alias requires pinned Apertus weights")
    # Recheck current local bytes and endpoint binding; a stale JSON manifest is insufficient.
    current = inspect(identity["model_dir"], base_url)
    if current["artifacts"] != identity.get("artifacts"):
        raise RuntimeError("Local artifacts changed since inspection")
    return current

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = inspect(args.model_dir, args.base_url)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("model_id", "source_revision", "format", "quantization", "v1_5_verified")}, indent=2))

if __name__ == "__main__":
    main()
