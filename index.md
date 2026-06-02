# Proof of Physical Behavior (PoPB) Protocol

> **Status:** v1.0.0 — Request for Comments
> **License:** MIT (spec) / Apache 2.0 (implementation)

**PoPB** is an open, hardware-anchored protocol for generating verifiable proofs of human physical behavior — capturing real-world movement as native on-chain assets.

---

## Quick Links

| Document | Description |
|----------|-------------|
| [Protocol Specification (v0.1)](spec-v0.1.md) | The full five-layer protocol spec |
| [Attestation Flow](attestation-flow.md) | How hardware-anchored proofs are generated |
| [Standards & RFC](standards/) | PoPB improvement proposals |
| [Trust & Audit](trust/) | Chain-of-custody and verification |
| [ROOT HASH](ROOT-HASH.md) | Immutable audit trail anchor |

---

## Abstract

PoPB establishes a cryptographically secure bridge between real-world human movement and on-chain verifiable proofs. Each proof is:

1. **Hardware-Anchored** — signed by a factory-provisioned secure element at the moment of occurrence
2. **Privacy-Preserving** — MPC-sharded raw data with ZK-proofs, user-controlled DID
3. **Open-Source** — MIT/Apache 2.0, fully auditable
4. **Model 5: Physical-Native RWA** — the proof IS the asset, no tokenization needed

---

## Protocol Layers

```
Layer 5: APPLICATION  — DID · Insurance · Behavior Exchange
Layer 4: VERIFICATION — Validator Network · Consensus
Layer 3: PRIVACY      — MPC Sharding · ZK-Proofs · DID
Layer 2: DATA CAPTURE — 15-Dim Sensor Fusion
Layer 1: HARDWARE TRUST ROOT — Secure Element · TEE
```

---

*[ZWISERFIT](https://github.com/ZWISERFIT/ZWISERFIT) · Dongguan · 2026*
