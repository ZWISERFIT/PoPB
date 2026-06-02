# PoPB — Proof of Physical Behavior

> *The open protocol for verifiable human physical activity. What TCP/IP did for data, PoPB does for your body.*

---

## The Problem

100 squats in a gym at 08:00 UTC. Who proves they happened?

Not the gym owner — they have an incentive to inflate. Not the app — your data is their ML training set. Not a DAO oracle — they can't sense the physical world.

**Physical human behavior has no cryptographic truth anchor.** Every sensor data stream today is one SQL UPDATE away from being rewritten. This is not a security bug. It's an architectural gap.

---

## Multicoin's Four Models — And What They Missed

In March 2026, Multicoin Capital published a landmark thesis — **["RWAs Are Just Built Different"](https://multicoin.capital/2026/03/19/rwas-are-just-built-different/)** — defining four ways to bring real-world assets on-chain:

```
        MULTICOIN'S RWA TAXONOMY (2026)
  ┌────────────────────────────────────────────┐
  │ Model 1: Tokenized Securities              │
  │ Model 2: Tokenized Commodities             │
  │ Model 3: Tokenized Real Estate             │
  │ Model 4: Tokenized IP & Creative Works     │
  ├────────────────────────────────────────────┤
  │ ❓ What's missing?                          │
  │                                            │
  │ Human behavior never sits still long       │
  │ enough to be "tokenized." It must be       │
  │ *proven at the moment it happens.*          │
  └────────────────────────────────────────────┘
```

Every model assumes: **"the asset exists before the proof."** A stock exists before you wrap it. Real estate exists before you fractionalize it.

Physical behavior breaks this assumption. 100 squats exist **only** at the moment they happen. There is no "underlying" to cache, no custodian to hold, no price oracle to report.

**The missing category: Model 5 — Physical-Native RWA.** Assets born on-chain because they're born in the physical world, proven by hardware, at the moment of occurrence.

**PoPB is Model 5.**

---

## What PoPB Does — 30 Seconds

```
HUMAN    ═▶  HARDWARE SENSOR  ═▶  PROOF  ═▶  CHAIN
│                                                
│  ⚡ NFC tap triggers capture                    
│  📡 15 sensors: IMU · BIA · ECG · ToF · IR     
│  🔐 Secure Element signs at the moment          
│  🛡️ MPC shards raw data, ZK wraps identity      
│  ✅ Proof committed — the proof IS the asset     
│                                                 
└── No issuer. No custodian. No oracle.          
```

One takeaway: **the proof is the asset.** There is no tokenization step. No custody handoff. The cryptographic attestation from the hardware trust root *is* the asset on-chain.

---

## Architecture at a Glance

```
┌──────────────────────────────────────────────────────────────────┐
│                     PoPB PROTOCOL STACK                            │
│                                                                    │
│  L5 ┌──────────────────┐                                          │
│     │  APPLICATION     │  DID · Insurance · Behavior Marketplace   │
│     └──────┬───────────┘                                          │
│  L4 ┌──────┴───────────┐                                          │
│     │  VERIFICATION    │  Validator Network · Slashing · Consensus │
│     └──────┬───────────┘                                          │
│  L3 ┌──────┴───────────┐                                          │
│     │  PRIVACY         │  MPC Sharding · ZK Proofs · DID Control  │
│     └──────┬───────────┘                                          │
│  L2 ┌──────┴───────────┐                                          │
│     │  DATA CAPTURE    │  15-Dim Sensor Fusion · Signal Pipeline  │
│     └──────┬───────────┘                                          │
│  L1 ┌──────┴───────────┐                                          │
│     │  HARDWARE TRUST  │  TEE · Secure Element · Device Keypair  │
│     └──────────────────┘                                          │
│                                                                    │
│  Each layer has a structural defense:                              │
│  L1 — Device private key never leaves silicon                      │
│  L2 — 15-dim fusion infeasible to simulate                         │
│  L3 — ZWF holds <K shares, structurally cannot read user data     │
│  L4 — Any node can independently verify                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Why This Can't Be Forked

| Attack | Cost | Time | Why It Fails |
|--------|:----:|:----:|-------------|
| Software clone | ~$50K | 3mo | ❌ **Protocol-invalid** — no hardware trust root = no valid proof |
| Deploy competitive hardware | ~$50M+ | 7+yr | ⏳ **Time-uncompressible** — PoPB has 7 years of real sensor data |
| AI-fake behavior streams | ~$500K | 6mo | ❌ **15-dim cross-sensor consistency check** catches fakes |
| Fork the open spec | $0 | 1 day | ✅ You can — but the *network* runs on attestations from deployed hardware |

> **Structural moat:** It's not "we do it better." It's "you cannot do it without 7 years of deployed hardware and real sensor data."

---

## Quick Start

```bash
git clone https://github.com/ZWISERFIT/PoPB.git
cd PoPB

# Read the spec
cat spec/PoPB-v1.0.0.md

# Run the attestation verifier
cd verifier
pip install -r requirements.txt
python popb_verify.py --proof example_proof.json
```

---

## Contribute

- **Read the protocol spec:** [`spec/PoPB-v1.0.0.md`](spec/PoPB-v1.0.0.md)
- **Join the discussion:** [GitHub Discussions](https://github.com/ZWISERFIT/PoPB/discussions)
- **Submit a proposal:** Open a [PoPB Improvement Proposal](https://github.com/ZWISERFIT/PoPB/issues/new/choose)
- **Find a task:** [`good first issue`](https://github.com/ZWISERFIT/PoPB/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) labeled issues

---

## License

| Component | License |
|-----------|---------|
| Protocol Specification (`spec/`) | [MIT](LICENSE) |
| Reference Implementation (`verifier/`) | [Apache 2.0](LICENSE) |
| Hardware Design Files | CERN OHL v2 (Permissive) |

**Patent Non-Assertion Pledge:** ZWISERFIT will not assert patents against conformant implementations.

---

## ⭐ Star · Contribute · Discuss

If this makes you think — **"finally, a way to prove my body's work is real"** — star the repo and join a Discussion. The protocol is open. The verifier runs on your laptop. The hardware runs in Dongguan.

[![Star on GitHub](https://img.shields.io/github/stars/ZWISERFIT/PoPB?style=social)](https://github.com/ZWISERFIT/PoPB/stargazers)
[![Discussions](https://img.shields.io/github/discussions/ZWISERFIT/PoPB?style=social)](https://github.com/ZWISERFIT/PoPB/discussions)

---

> **PoPB v1.0.0 — Published 2026-06-02**
>
> *An open protocol. A shared standard. A trustless bridge between the physical world and the digital.*
>
> — [ZWISERFIT](https://github.com/ZWISERFIT/ZWISERFIT) · Dongguan · 2026
