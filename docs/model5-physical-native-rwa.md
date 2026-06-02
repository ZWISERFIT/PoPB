# Model 5: Physical-Native RWA — A Response to Multicoin Capital's "RWAs Are Just Built Different"

**Document Type:** Open Academic Response / Protocol Positioning
**Version:** 1.0
**Date:** 2026-06-02
**Authors:** Zeus, on behalf of ZWISERFIT
**Target Publication:** ZWISERFIT GitHub / Mirror.xyz / X (Twitter)
**License:** CC BY 4.0

---

## Abstract

On March 19, 2026, Multicoin Capital published "RWAs Are Just Built Different" — a landmark framework defining four models for bringing real-world assets on-chain. The paper is comprehensive in its coverage of financial RWAs: synthetic derivatives, wrapped custody assets, collateralized borrowing, and primary on-chain issuance. But the four models share a hidden assumption: **the asset exists independently of the proof that attests to it.** A stock exists before you tokenize it. A treasury bill exists before you wrap it. Real estate exists before you borrow against it.

What if the proof **is** the asset?

This article introduces **Model 5: Physical-Native RWA** — a category of on-chain assets where the asset is **generated** (not issued) by human physical behavior, and the cryptographic proof of that behavior **is** the asset itself. No tokenization required. No custodian. No price oracle.

ZWISERFIT has built the protocol for this: **Proof of Physical Behavior (PoPB)**. The specification is open-source and published today.

---

## 1. The Hidden Assumption in Multicoin's Four Models

Multicoin's paper defines four RWA models with characteristic clarity:

| Model | Definition | Core Mechanism |
|-------|-----------|----------------|
| **Model 1: Synthetic Derivatives** | Tokenized exposure to off-chain assets via price feeds | Oracle-dependent price tracking |
| **Model 2: Wrapped Assets (Custody)** | Off-chain asset held by custodian, token issued on-chain | Trusted custodian + 1:1 backing |
| **Model 3: Collateralized Borrowing** | Borrow stablecoins against off-chain collateral | Over-collateralization + liquidation |
| **Model 4: Primary Onchain Issuance** | Assets natively issued on-chain with legal enforceability | SEC-registered or exempt on-chain securities |

Multicoin describes Model 4 as "the purest version of crypto-native RWAs and the industry's north star." We agree — within the framework of **financial assets**. But every one of these models assumes:

> *"There is an off-chain asset that needs to be represented on-chain."*

Physical human behavior does not satisfy this assumption. A person doing 100 squats in a gym is not an "asset" that exists independently waiting to be tokenized. The behavior **is** the value-generating event. The proof **is** the asset.

This is not a limitation of Multicoin's framework — it's a limitation of the **asset ontology** the framework was built to handle. Model 5 is not a correction. It's an extension into a category of assets that Model 1-4 were never designed for.

---

## 2. Why Physical Behavior Data Fits None of the Four Models

Let's apply each model to the question: "How would you bring a person's verified gym workout data on-chain?"

### Model 1: Synthetic Derivatives
> Requires a price feed for the underlying asset.

**Why it fails:** There is no "market price" for "100 squats completed at 08:00 UTC by a verified human." Behavior data does not have a spot price that an oracle can report. The data **is** the asset — not a derivative of something with a market price.

### Model 2: Wrapped Assets (Custody)
> Requires a custodian to hold the asset and issue tokens.

**Why it fails:** Behavior data does not need a "custodian." It is proven by hardware trust root (the gym gate sensor's secure element) at the moment of generation. There is no "underlying" to hold — the proof is native to the event. A custodian would add trust assumptions to a process that is already cryptographically trustless.

### Model 3: Collateralized Borrowing
> Requires collateral that can be liquidated.

**Why it fails:** Behavior data is not collateral. You don't "borrow against" your workout history. The data itself carries actuarial and analytical value — it is a **primary asset**, not a **secondary claim** on something else.

### Model 4: Primary Onchain Issuance
> Requires legal issuance of a security.

**Why it fails (or comes closest):** Model 4 is the closest fit — but it still assumes the asset is "issued" by an issuer. Behavior data is not "issued" — it is **generated**. The gym goer is not an "issuer." The hardware sensor is not an "issuer." The data comes into existence through physical action and is simultaneously proven. There is no gap between "asset creation" and "asset proof" — they are the same event.

---

## 3. Model 5: Physical-Native RWA — Definition

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   MODEL 5: Physical-Native RWA                                  │
│                                                                 │
│   Definition: An on-chain asset whose existence is co-incident  │
│   with its cryptographic proof. The asset is a verified human   │
│   physical behavior event, generated by hardware-anchored       │
│   sensors and attested at the moment of occurrence.             │
│                                                                 │
│   Key Properties:                                               │
│   • Proof ≡ Asset (no gap between creation and attestation)     │
│   • Hardware Trust Root (not custodian Trust)                   │
│   • No Tokenization Needed (the proof IS the token)             │
│   • No Price Oracle (behavior value is actuarial, not market)   │
│   • Privacy-Preserving by Architecture (MPC + ZK, not policy)   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 How Model 5 Works

1. **Generation:** A human performs a physical behavior (e.g., 100 squats) in a sensor-equipped environment.
2. **Attestation:** 15-dimensional sensor fusion captures the event. The gate sensor's hardware secure element (TEE) signs a cryptographic proof of the event using a factory-provisioned Ed25519 key.
3. **Privacy Wrapping:** Raw sensor data is MPC-sharded across independent parties. A ZK-proof attests to event validity without revealing identity.
4. **On-Chain Settlement:** The behavior proof is committed to chain. The proof **is** the asset. No separate tokenization step.
5. **Consumption:** Applications (insurance, health analytics, DID credentials) consume verified proofs with explicit user authorization. The user controls their data via DID.

### 3.2 Why Model 5 Is More Native Than Model 4

Multicoin calls Model 4 "the purest version of crypto-native RWAs." We argue Model 5 is **more native**:

| Property | Model 4 (Primary Issuance) | Model 5 (Physical-Native) |
|----------|---------------------------|--------------------------|
| **Asset Ontology** | Asset exists before proof | Asset ≡ Proof |
| **Issuer** | Legal entity (company) | Physics + Hardware |
| **Gap** | Issuance → Registration | Generation = Attestation |
| **Regulatory** | SEC jurisdiction | Outside securities law (Arcade Token model) |
| **Trust Model** | Legal enforceability | Cryptographic verifiability |

---

## 4. The PoPB Protocol: Model 5's Technical Implementation

**Proof of Physical Behavior (PoPB)** is the open protocol that implements Model 5. It is a five-layer stack:

```
Layer 5: APPLICATION — DID · Insurance · Behavior Exchange
Layer 4: VERIFICATION — Validator Network · Consensus · Slashing
Layer 3: PRIVACY — MPC Sharding · ZK-Proofs · DID Sovereignty
Layer 2: DATA CAPTURE — 15-Dim Sensor Fusion · Signal Processing
Layer 1: HARDWARE TRUST ROOT — Secure Element · TEE · Device Attestation
```

The entire specification is open-source (MIT/Apache 2.0) and published today at:
**github.com/ZWISERFIT/PoPB**

### 4.1 Why Layer 1 Makes Model 5 Unforgeable

The critical innovation is the **Hardware Trust Root**. Every ZWISERFIT gate sensor is factory-provisioned with a unique Ed25519 keypair sealed in a secure element. All behavior proofs must contain a valid `device_attestation` — a cryptographic quote from the hardware TEE.

A pure software implementation of the PoPB protocol can generate syntactically valid JSON. It **cannot** produce a valid attestation. This is not a policy boundary. It is a mathematical boundary.

### 4.2 Why the Protocol Is Open (Despite the Hardware Moat)

The PoPB protocol specification is fully open. Anyone can:
- Read and audit the full protocol specification
- Implement a compatible verifier
- Build applications that consume PoPB proofs
- Propose protocol improvements (PoPB Improvement Proposals)

What they **cannot** do without physically deployed hardware:
- Generate valid behavior proofs

This is the same asymmetry that makes TCP/IP work: the standard is open, but the infrastructure to produce valid data on the network requires physical deployment. The openness of the protocol is what makes it a standard. The hardware trust root is what makes it a moat.

---

## 5. Why Multicoin Should Care

Multicoin Capital's investment thesis has traced a four-year arc:

```
2022.04: Proof of Physical Work
         → "Tokens create opportunities for capital formation that
            extend beyond the digital world and into the physical."

2026.03.10: Internet Labor Markets
            → "There are only two ways to onboard to crypto:
               you buy in or you earn in."
            → Physical work = verifiable tasks on crypto rails

2026.03.19: RWAs Are Just Built Different
            → Four models for RWAs on-chain
            → "The purest version of crypto-native RWAs"
```

The trajectory is clear: **Multicoin is moving toward the physical world.** From Proof of Physical Work (conceptual, 2022) to Internet Labor Markets (task-based, March 2026) to RWA taxonomy (asset-based, March 2026). The next logical step is the asset class at the intersection of all three: **physical human behavior as a native on-chain asset.**

Model 5 completes the arc. It is the missing row in the RWA taxonomy — the asset class that Protocol of Physical Work envisioned, that Internet Labor Markets operationalized, and that "RWAs Are Just Built Different" left room for.

---

## 6. What We're Publishing Today

| Asset | Description | License |
|-------|-------------|---------|
| **PoPB Protocol Spec v1.0** | Full five-layer protocol specification | MIT |
| **PoPB Moat Argument** | Structural competitive defense analysis | Internal |
| **This Response (Model 5)** | Academic response to Multicoin RWA paper | CC BY 4.0 |
| **PoPB Attestation Verifier** | Minimal reference implementation | Apache 2.0 |
| **Hardware Capability Statement** | Non-confidential hardware deployment proof | Public |

All public assets available at: **github.com/ZWISERFIT/PoPB**

---

## 7. Call to Action (Not a Pitch)

To the Multicoin team — Spencer, Shayon, Tushar, Kyle:

You wrote that Model 4 is "the purest version of crypto-native RWAs and the industry's north star." We agree — for financial RWAs. But there is a category of assets more native than anything that requires an issuer: **assets that are born on-chain because they are born in the physical world, proven by hardware.**

Model 5 is not a competitor to your framework. It is a completion of it.

The protocol specification is open. The verifier is public. The hardware is deployed and has been running for seven years in Dongguan, China — in the hardest possible market for fitness penetration, proving the lower bound of the model's viability.

We didn't build this to pitch you. We built it because your own papers described a gap and we filled it. If it interests you, the spec is at github.com/ZWISERFIT/PoPB.

---

> *"The purest version of crypto-native RWAs" — Multicoin Capital, March 2026*
> *Model 5 is purer. Here's the spec.*

---

**ZWISERFIT · Dongguan, Guangdong**
**Contact:** [founder contact placeholder]
**PoPB Protocol:** github.com/ZWISERFIT/PoPB
**Date:** June 2, 2026
