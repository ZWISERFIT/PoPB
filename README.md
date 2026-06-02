# PoPB — Proof of Physical Behavior

> *"What TCP/IP did for the internet, PoPB does for human physical behavior data."*

**PoPB (Proof of Physical Behavior)** is an open, hardware-anchored protocol for cryptographically verifiable human physical activity data. It bridges the gap between real-world human movement and on-chain verifiable proofs — enabling decentralized identity (DID), actuarial science, health analytics, and behavior-based value exchange while preserving user privacy and data sovereignty.

---

## 🎯 Why PoPB? — Model 5

In March 2026, Multicoin Capital published a landmark thesis: **["RWAs Are Just Built Different"](https://multicoin.capital/2026/03/19/rwas-are-just-built-different/)** (2026.03.19), identifying four models of Real World Assets on-chain:

```
┌──────────────────────────────────────────────────────────────────┐
│  Multicoin's RWA Taxonomy (2026)                                  │
│                                                                   │
│  Model 1: Tokenized Securities   — Stocks, bonds on-chain        │
│  Model 2: Tokenized Commodities  — Gold, oil, carbon credits     │
│  Model 3: Tokenized Real Estate  — Property fractionalization    │
│  Model 4: Tokenized IP/Creative  — Royalties, patents, brands    │
│                                                                   │
│  ❓  What's missing?                                              │
│                                                                   │
│  Model 5: Tokenized HUMAN BEHAVIOR — Your body, your data,       │
│           your value. The only RWA that grows with every move.   │
│                                                                   │
│  PoPB is Model 5.                                                 │
└──────────────────────────────────────────────────────────────────┘
```

**The four models tokenize static assets. PoPB tokenizes the one asset that compounds:** ***you, moving.** *  Every squat, every heartbeat, every calorie burned becomes a cryptographically verifiable, privacy-preserving proof — the fifth category Multicoin's framework didn't account for.

---

## 🏗️ Architecture — Five-Layer Protocol Stack

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 5: APPLICATION LAYER                                  │
│  DID Verification · Insurance Actuarial · Behavior Exchange │
├─────────────────────────────────────────────────────────────┤
│  Layer 4: VERIFICATION LAYER                                 │
│  Proof Aggregation · Validator Network · Slashing           │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: PRIVACY LAYER                                      │
│  MPC Data Sharding · Zero-Knowledge Proofs · DID Sovereignty│
├─────────────────────────────────────────────────────────────┤
│  Layer 2: DATA CAPTURE LAYER                                 │
│  15-Dimensional Sensor Fusion · Signal Processing Pipeline  │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: HARDWARE TRUST ROOT                                │
│  Gate Firmware · Secure Boot · TEE · Device Attestation     │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Name | Core Function | Why It Can't Be Bypassed |
|-------|------|---------------|--------------------------|
| **L1** | Hardware Trust Root | Device identity + TEE-based attestation | Device private key never leaves secure element. No hardware = no valid proof. |
| **L2** | Data Capture | 15-dimensional sensor fusion (IMU, BIA, ECG, ToF, IR...) | Cross-modal consistency across 15 sensor dimensions is computationally infeasible to simulate. |
| **L3** | Privacy | MPC data sharding + ZK-proof wrapping | Raw data is MPC-sharded across independent parties. ZWF holds < K shares — structurally cannot read user data. |
| **L4** | Verification | Decentralized validator network with staking/slashing | Trustless verification. Any node can independently validate proofs. |
| **L5** | Application | DID credentials, insurance, behavior marketplace | Applications consume *verified* proofs only. No backdoor. |

---

## 🔐 The Moat: Why PoPB Cannot Be Copied

PoPB's competitive advantage is **structural**, not executional:

```
Hardware Trust Root × Time Uncompressible × Verification Network Effect
= Unbypassable Competitive Moat
```

| Attack Vector | Cost | Time | PoPB Defense |
|---------------|------|------|-------------|
| Write a software clone | ~$50K | 3 months | **❌ Protocol-level invalid** (no hardware root = no valid proof) |
| Deploy 500+ gyms + custom hardware | ~$50M+ | **7+ years** | Time is uncompressible |
| AI-generate synthetic behavior data | ~$500K | 6 months | **15-dim sensor fusion consistency check** catches AI fakes |
| Build alternative verification standard | ~$10M | 2 years | **Network effect + switching costs** exceed build costs |

> **Investor thesis:** This isn't "we do it better." This is "you *cannot* do it without 7 years of real sensor data and deployed hardware."

---

## 📜 License — Open Protocol, Dual License

| Component | License | Rationale |
|-----------|---------|-----------|
| **Protocol Specification** (`spec/`) | [MIT](LICENSE) | Anyone can implement, extend, or fork. Maximum openness. |
| **Reference Implementation** (`verifier/`) | [Apache 2.0](LICENSE) | Patent grant included. Protects ecosystem from patent lawsuits. |
| **Hardware Design Files** | CERN OHL v2 (Permissive) | Open hardware, attribution required. |

**Patent Non-Assertion Pledge:** ZWISERFIT pledges not to assert patents against conformant implementations of the PoPB protocol.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/ZWISERFIT/PoPB.git
cd PoPB

# Read the specification
cat spec/PoPB-v1.0.0.md

# Run the attestation verifier (proof-of-concept)
cd verifier
pip install -r requirements.txt
python popb_verify.py --proof example_proof.json
```

---

## 📂 Repository Structure

```
PoPB/
├── README.md                    # This file
├── LICENSE                      # MIT (spec) + Apache 2.0 (ref impl)
├── spec/
│   └── PoPB-v1.0.0.md          # Full protocol specification v1.0.0
└── verifier/
    ├── README.md                # Attestation Verifier documentation
    ├── popb_verify.py           # CLI verifier (minimal PoC)
    ├── requirements.txt         # Python dependencies
    └── example_proof.json       # Demo proof with simulated device signature
```

---

## 🌐 Protocol Status

| Version | Date | Status |
|---------|------|--------|
| **v1.0.0** | 2026-06-02 | ✅ Published — Spec + Reference Verifier |
| v1.1 | 2026-Q3 | 🔨 ZK-circuit v1 (Groth16), Private testnet |
| v2.0 | 2027-Q1 | 📋 Mainnet validator network, EigenLayer AVS |

---

## 🔗 References

- [Full Protocol Specification v1.0.0](spec/PoPB-v1.0.0.md)
- [Multicoin Capital — "RWAs Are Just Built Different" (2026.03.19)](https://multicoin.capital/2026/03/19/rwas-are-just-built-different/)
- [W3C Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/)
- [EigenLayer Whitepaper](https://docs.eigenlayer.xyz/)

---

> **PoPB v1.0 — Published 2026-06-02**
>
> *An open protocol. A shared language. A trustless bridge between the physical and the digital.*
>
> — ZWISERFIT / PoPB Protocol Authors
