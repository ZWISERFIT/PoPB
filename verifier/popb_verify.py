#!/usr/bin/env python3
"""
PoPB Attestation Verifier — Minimal Proof-of-Concept

Verifies a PoPB Behavior Proof against the protocol's core security invariant:
"No hardware key → no valid proof."

Usage:
    python popb_verify.py --proof example_proof.json
    python popb_verify.py --proof test_invalid_proof.json

Returns exit code 0 for VALID, 1 for INVALID.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Optional, Tuple

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.exceptions import InvalidSignature


# ============================================================================
# Known Device Registry (simulated — production uses on-chain registry)
# ============================================================================

KNOWN_DEVICES = {
    "ZWF-GATE-A1B2C3D4E5F6": {
        "public_key_hex": "9c0d5c0fc4ee636f6ac9c59ac648482d6c6bb9400c654f9d4d5c6c1d4475e31e",
        "model": "Gate-Sensor-Gen2",
        "manufacturer": "ZWISERFIT",
        "registered_at": "2026-01-01T00:00:00Z",
        "status": "active",
    },
}


# ============================================================================
# Schema Validation
# ============================================================================

REQUIRED_TOP_KEYS = [
    "proof_id", "protocol_version", "device_attestation",
    "behavior_claim", "zk_proof", "timestamp", "signature"
]

REQUIRED_DEVICE_KEYS = ["device_id", "quote", "challenge"]
REQUIRED_CLAIM_KEYS = ["exercise_type", "repetition_count", "duration_ms", "form_quality_score"]
REQUIRED_ZK_KEYS = ["proof_system", "proof_data", "public_inputs"]

VALID_EXERCISE_TYPES = {
    "squat", "push_up", "lunge", "plank", "jumping_jack", "burpee", "custom"
}

MAX_CLOCK_DRIFT_SECONDS = 300  # 5 minutes


def validate_schema(proof: dict) -> Optional[str]:
    """Validate proof against PoPB schema. Returns error message or None."""
    # Top-level required keys
    for key in REQUIRED_TOP_KEYS:
        if key not in proof:
            return f"Missing required top-level key: '{key}'"

    # Device attestation
    da = proof["device_attestation"]
    for key in REQUIRED_DEVICE_KEYS:
        if key not in da:
            return f"Missing required device_attestation key: '{key}'"

    # Behavior claim
    bc = proof["behavior_claim"]
    for key in REQUIRED_CLAIM_KEYS:
        if key not in bc:
            return f"Missing required behavior_claim key: '{key}'"

    if bc["exercise_type"] not in VALID_EXERCISE_TYPES:
        return f"Invalid exercise_type: '{bc['exercise_type']}'"
    if not isinstance(bc["repetition_count"], int) or bc["repetition_count"] < 1:
        return "repetition_count must be a positive integer"
    if not isinstance(bc["form_quality_score"], (int, float)) or not (0.0 <= bc["form_quality_score"] <= 1.0):
        return "form_quality_score must be between 0.0 and 1.0"
    if not isinstance(bc["duration_ms"], int) or bc["duration_ms"] < 0:
        return "duration_ms must be a non-negative integer"

    # ZK proof (placeholder validation)
    zk = proof["zk_proof"]
    for key in REQUIRED_ZK_KEYS:
        if key not in zk:
            return f"Missing required zk_proof key: '{key}'"
    if zk["proof_system"] not in {"groth16", "plonk", "halo2", "nova"}:
        return f"Unknown ZK proof system: '{zk['proof_system']}'"

    return None  # valid


def canonicalize_for_signing(proof: dict) -> bytes:
    """
    Build canonical bytes that were signed.
    All top-level fields EXCEPT 'signature', in sorted key order.
    This mirrors the on-device signing procedure.
    """
    signable = {k: v for k, v in proof.items() if k != "signature"}
    return json.dumps(signable, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_signature(proof: dict, public_key_hex: str) -> Tuple[bool, str]:
    """Verify Ed25519 signature. Returns (valid, detail)."""
    try:
        sig_hex = proof["signature"]
        sig_bytes = bytes.fromhex(sig_hex)
        pk_bytes = bytes.fromhex(public_key_hex)

        if len(sig_bytes) != 64:
            return False, f"Signature length is {len(sig_bytes)} bytes, expected 64"
        if len(pk_bytes) != 32:
            return False, f"Public key length is {len(pk_bytes)} bytes, expected 32"

        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pk_bytes)
        message = canonicalize_for_signing(proof)
        public_key.verify(sig_bytes, message)

        return True, "Ed25519 signature verified"
    except InvalidSignature:
        return False, "Signature verification failed: tampered proof or forged device key"
    except ValueError as e:
        return False, f"Invalid hex encoding: {e}"
    except Exception as e:
        return False, f"Signature verification error: {e}"


def validate_timestamp(proof: dict) -> Optional[str]:
    """Validate proof timestamp. Returns error or None."""
    ts_str = proof.get("timestamp", "")
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return f"Invalid timestamp format: '{ts_str}'"

    now = datetime.now(timezone.utc)
    device_id = proof["device_attestation"]["device_id"]

    # Check future timestamp
    if ts > now:
        delta = (ts - now).total_seconds()
        if delta > MAX_CLOCK_DRIFT_SECONDS:
            return f"Timestamp is {delta:.0f}s in the future (max drift: {MAX_CLOCK_DRIFT_SECONDS}s)"

    # Check timestamp is after device registration
    if device_id in KNOWN_DEVICES:
        registered = datetime.fromisoformat(
            KNOWN_DEVICES[device_id]["registered_at"].replace("Z", "+00:00")
        )
        if ts < registered:
            return f"Timestamp {ts_str} is before device registration {KNOWN_DEVICES[device_id]['registered_at']}"

    return None


def verify_proof(proof_path: str) -> Tuple[bool, str, Optional[dict]]:
    """
    Full verification pipeline.
    Returns (valid, message, proof_dict).
    """
    # Step 0: Load JSON
    try:
        with open(proof_path, "r") as f:
            proof = json.load(f)
    except FileNotFoundError:
        return False, f"Proof file not found: {proof_path}", None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}", None

    # Step 1: Schema validation
    err = validate_schema(proof)
    if err:
        return False, f"❌ INVALID: Schema validation failed — {err}", proof

    # Step 2: Device registration check
    device_id = proof["device_attestation"]["device_id"]
    if device_id not in KNOWN_DEVICES:
        return False, f"❌ INVALID: Device '{device_id}' not in known device registry", proof

    device_info = KNOWN_DEVICES[device_id]
    if device_info["status"] != "active":
        return False, f"❌ INVALID: Device '{device_id}' status is '{device_info['status']}'", proof

    # Step 3: Signature verification (THE CORE CHECK)
    pk_hex = device_info["public_key_hex"]
    valid, detail = verify_signature(proof, pk_hex)
    if not valid:
        return False, f"❌ INVALID: {detail}", proof

    # Step 4: Timestamp sanity check
    err = validate_timestamp(proof)
    if err:
        return False, f"❌ INVALID: Timestamp check failed — {err}", proof

    # Step 5: ZK proof verification (placeholder)
    # In production, this runs a Groth16 verifier against the ZK proof data.
    # For this PoC, we acknowledge receipt.

    # All checks passed
    bc = proof["behavior_claim"]
    return True, (
        f"✅ VALID — Proof verified successfully\n"
        f"   Proof ID:     {proof['proof_id']}\n"
        f"   Device:       {device_id} ({device_info['model']})\n"
        f"   Exercise:     {bc['exercise_type']}\n"
        f"   Reps:         {bc['repetition_count']}\n"
        f"   Duration:     {bc['duration_ms']}ms\n"
        f"   Form Quality: {bc['form_quality_score']}\n"
        f"   Timestamp:    {proof['timestamp']}\n"
        f"   Sig:          {detail}"
    ), proof


def main():
    parser = argparse.ArgumentParser(
        description="PoPB Attestation Verifier — Minimal Proof-of-Concept",
        epilog="Returns exit code 0 for VALID, 1 for INVALID.",
    )
    parser.add_argument(
        "--proof", "-p",
        required=True,
        help="Path to Behavior Proof JSON file",
    )
    args = parser.parse_args()

    valid, message, _ = verify_proof(args.proof)
    print(message)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
