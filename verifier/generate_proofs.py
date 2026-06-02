#!/usr/bin/env python3
"""Generate example PoPB proof files with real Ed25519 signatures."""
import json
import hashlib
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

# 1. Generate a device keypair (simulated factory-provisioned key)
device_sk = ed25519.Ed25519PrivateKey.generate()
device_pk = device_sk.public_key()

# Serialize raw bytes
pk_bytes = device_pk.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)
sk_bytes = device_sk.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)

device_pk_hex = pk_bytes.hex()
device_sk_hex = sk_bytes.hex()

print(f"DEVICE_PUBLIC_KEY_HEX={device_pk_hex}")
print(f"DEVICE_SECRET_KEY_HEX={device_sk_hex}")

# 2. Build the proof (sans signature)
proof = {
    "proof_id": "018f9e2a-7b3c-4d5e-a1f2-b3c4d5e6f7a8",
    "protocol_version": "1.0.0",
    "device_attestation": {
        "device_id": "ZWF-GATE-A1B2C3D4E5F6",
        "quote": "QU9XRVNPTUUgVEVFIE1FQVNVUkVEIEJPT1QgUVVPVEUgREVNTyBEQVRB",
        "challenge": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
        "measured_boot_hash": hashlib.sha256(b"demo-measured-boot-v1.0.0-20260602").hexdigest()
    },
    "behavior_claim": {
        "exercise_type": "squat",
        "repetition_count": 100,
        "duration_ms": 180000,
        "form_quality_score": 0.94,
        "heart_rate_avg": 142,
        "calories_estimate": 45.2,
        "sensor_fusion_hash": hashlib.sha256(
            b"squat-100-reps-15dim-sensor-stream-20260602"
        ).hexdigest()
    },
    "zk_proof": {
        "proof_system": "groth16",
        "proof_data": "R1JPVEgxNiBaSyBQUk9PRiBERU1PIEVOQ09ERUQgREFUQQ==",
        "public_inputs": [
            hashlib.sha256(b"squat").hexdigest()[:32],
            "100",
            "0.94"
        ],
        "verification_key_hash": hashlib.sha256(b"groth16-vk-demo").hexdigest()
    },
    "timestamp": "2026-06-02T03:00:00Z",
    "mpc_commitment": {
        "shard_count": 5,
        "threshold": 3,
        "shard_hashes": [
            hashlib.sha256(b"mpc-shard-0").hexdigest(),
            hashlib.sha256(b"mpc-shard-1").hexdigest(),
            hashlib.sha256(b"mpc-shard-2").hexdigest(),
            hashlib.sha256(b"mpc-shard-3").hexdigest(),
            hashlib.sha256(b"mpc-shard-4").hexdigest(),
        ],
        "storage_parties": [
            "did:popb:storage:ipfs-node-1",
            "did:popb:storage:arweave-node-1",
            "did:popb:storage:filecoin-node-1",
            "did:popb:storage:ipfs-node-2",
            "did:popb:storage:arweave-node-2",
        ]
    },
    "did_anchor": {
        "subject_did": "did:popb:0x7a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b",
        "credential_type": "PoPBBehaviorCredential"
    }
}

# 3. Canonicalize and sign
signable = {k: v for k, v in proof.items()}
message = json.dumps(signable, sort_keys=True, separators=(",", ":")).encode("utf-8")
sig = device_sk.sign(message)
sig_hex = sig.hex()

proof["signature"] = sig_hex

# 4. Write valid proof
with open("example_proof.json", "w") as f:
    json.dump(proof, f, indent=2)
    f.write("\n")

# 5. Write invalid proof (tampered — signature won't match)
tampered = json.loads(json.dumps(proof))
tampered["behavior_claim"]["repetition_count"] = 999  # Tampered!
# Keep the original signature — it will fail verification
with open("test_invalid_proof.json", "w") as f:
    json.dump(tampered, f, indent=2)
    f.write("\n")

print("Generated: example_proof.json, test_invalid_proof.json")
print("Done.")
