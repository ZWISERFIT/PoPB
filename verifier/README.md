# PoPB Attestation Verifier — Minimal Proof-of-Concept

A minimal, auditable reference implementation of the PoPB attestation verification logic.

**Status:** Proof-of-Concept (v1.0.0)  
**Language:** Python 3.10+  
**License:** Apache 2.0  

---

## Philosophy

This verifier demonstrates the **core security invariant** of the PoPB protocol:

> **No hardware key → no valid proof.**

Every Behavior Proof is signed by a device's Ed25519 private key — a key that is generated inside a secure element at the factory and **never leaves the hardware**. This verifier shows the logical structure: if you have a proof, you can verify its signature. But if you don't have the device's private key, you cannot *produce* a valid proof.

---

## Architecture

```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  proof.json      │────▶│  popb_verify.py  │────▶│  ✅ VALID         │
│  (device-signed  │     │  (signature      │     │  or               │
│   behavior proof)│     │   verification   │     │  ❌ INVALID       │
│                  │     │   + schema       │     │  + reason         │
└──────────────────┘     │   validation)    │     └──────────────────┘
                         └──────────────────┘
```

### Verification Pipeline

1. **Parse proof.json** → Validate against PoPB proof schema
2. **Extract device public key** → From known device registry (or inline for demo)
3. **Verify Ed25519 signature** → `signature` field must match signed payload
4. **Validate timestamp** → Proof timestamp must be sane (not future, not before device issuance)
5. **Check device registration** → Device ID must be in known-good registry  
6. **Output result** → `✅ VALID` or `❌ INVALID: <reason>`

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Verify the example proof
python popb_verify.py --proof example_proof.json

# Expected output:
# ✅ VALID — Proof verified successfully
#    Device:  ZWF-GATE-A1B2C3D4E5F6
#    Exercise: squat
#    Reps:     100
#    Quality:  0.94
```

To see what happens with an **invalid** proof (tampered or forged), try:

```bash
# This proof has a broken signature
python popb_verify.py --proof test_invalid_proof.json
# ❌ INVALID: Signature verification failed
```

---

## File Structure

```
verifier/
├── README.md               # This file
├── requirements.txt         # Python dependencies (pynacl)
├── popb_verify.py           # Main CLI verifier
├── example_proof.json       # Example valid proof (with simulated device key)
└── test_invalid_proof.json  # Example invalid proof (tampered signature)
```

---

## Security Model

| Component | Real Deployment | This PoC |
|-----------|----------------|----------|
| **Device key storage** | ATECC608B Secure Element (never leaves hardware) | Ed25519 keypair generated in-memory for demo |
| **Signature algorithm** | Ed25519 (RFC 8032) | Ed25519 via PyNaCl |
| **Device registry** | On-chain registry (Ethereum L2) | Inline `KNOWN_DEVICES` dict |
| **ZK proof verification** | Groth16 verifier (bellman/arkworks) | Placeholder (skipped in PoC) |
| **Timestamp validation** | TEE-sourced clock + NTP consensus | System clock comparison |

**This PoC is NOT production-ready.** It demonstrates the protocol's logical structure and security invariant. Production deployment requires hardware-backed key storage, on-chain device registry, and full ZK proof verification.

---

## Why This Matters

A competitor can:

- ✅ Fork this repository
- ✅ Read the specification
- ✅ Write a software-only implementation
- ✅ Generate synthetically plausible sensor data

But they **cannot**:

- ❌ Produce a valid behavior proof (no hardware root key)
- ❌ Have their proof accepted by the verifier network (no device registry entry)
- ❌ Reproduce the 15-dimensional sensor fusion fingerprint

This verifier makes the **logical impossibility** visible and auditable.

---

## Dependencies

- **Python 3.10+**
- **PyNaCl** — Ed25519 signature operations (libsodium bindings)

---

> *"The verifier is the protocol's enforcement mechanism. If you can't produce a valid proof, you can't participate. That's the moat."*
>
> — PoPB Protocol Authors
