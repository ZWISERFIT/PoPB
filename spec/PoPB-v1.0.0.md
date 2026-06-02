# PoPB Protocol Specification v1.0

**Status:** Draft / Request for Comments  
**Version:** 1.0.0  
**Date:** 2026-06-02  
**Authors:** Zeus (on behalf of ZWF / ZWISERFIT)  
**License:** MIT (protocol specification) / Apache 2.0 (reference implementation)  
**Language:** English (中文注释以 `//` 标注)

---

## Abstract

This document defines **Proof of Physical Behavior (PoPB)** — an open, hardware-anchored protocol for verifiable human physical behavior data. PoPB establishes a cryptographically secure bridge between real-world human movement and on-chain verifiable proofs, enabling applications in decentralized identity (DID), actuarial science, health analytics, and behavior-based value exchange without sacrificing user privacy or data sovereignty.

> **中文摘要**: PoPB是一个开放、硬件锚定的物理行为验证协议，在真实世界人类运动和链上可验证证明之间建立密码学安全桥梁，支持去中心化身份(DID)、保险精算、健康分析和基于行为的价值交换，同时保障用户隐私和数据主权。

---

## 1. Protocol Overview

### 1.1 Definition

**Proof of Physical Behavior (PoPB)** is a layered protocol that generates tamper-evident, hardware-attested cryptographic proofs of human physical activity. Each proof cryptographically binds a specific behavior event (e.g., "completed 100 squats at 08:00 UTC on 2026-06-02") to:

1. A **hardware trust root** (device identity + measured boot state)
2. A **multi-sensor data stream** (15-dimensional sensor fusion)
3. A **privacy-preserving verifiable credential** (ZK-proof wrapper)
4. An **immutable audit trail** (on-chain or L2 settlement)

### 1.2 Protocol Analogy

```
TCP/IP : Internet :: PoPB : Human Physical Behavior Data
```

Just as TCP/IP standardized how computers communicate across heterogeneous networks, PoPB standardizes how human physical behavior is captured, attested, transmitted, verified, and monetized — across heterogeneous hardware, jurisdictions, and application domains.

### 1.3 Design Goals

| Goal | Description | Threat Model |
|------|-------------|-------------|
| **Unforgeable** (`不可伪造`) | Every proof is rooted in a hardware-bound cryptographic identity; synthetic/AI-generated data cannot produce valid attestations | Sybil attacks, AI-generated fakes, replay attacks |
| **Privacy-Preserving** (`隐私保护`) | Proofs reveal _what happened_ without revealing _who did it_, unless the data subject explicitly authorizes deanonymization | Surveillance capitalism, data breaches, unauthorized profiling |
| **Hardware-Anchored** (`硬件锚定`) | Proof validity depends on a physically deployed sensor device with a unique factory-provisioned key; pure-software implementations are invalid by protocol design | "Write a compatible client in Python" attacks |
| **Open-Source Auditable** (`开源可审计`) | Protocol specification, reference implementation, and verification logic are fully open-source; any party can verify proofs independently | Opaque algorithms, centralized trust assumptions |

### 1.4 Terminology

| Term | Definition |
|------|-----------|
| **Behavior Event** | A discrete physical activity session (e.g., one workout, one biometric reading) |
| **Behavior Proof (BP)** | The cryptographically signed output of a Behavior Event, ready for transmission and verification |
| **Device Identity (DID-device)** | A unique Ed25519 keypair burned into each gate sensor device at manufacturing |
| **Verifier Node** | A network participant that validates Behavior Proofs and participates in consensus |
| **Data Subject** | The human whose physical behavior is being captured |
| **Data Consumer** | An application, service, or smart contract that consumes verified Behavior Proofs |
| **Trusted Execution Environment (TEE)** | Hardware-isolated compute region where critical signing operations occur |
| **Multi-Party Computation (MPC)** | Cryptographic protocol that distributes raw sensor data across multiple parties such that no single party can reconstruct it |

---

## 2. Architecture — Five-Layer Protocol Stack

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

### 2.1 Layer 1: Hardware Trust Root

**Responsibility:** Establish a physically-anchored, unforgeable device identity and ensure the execution environment is tamper-free before any data is captured.

**Input:** Factory-provisioned device keypair, signed firmware image  
**Output:** Attested device state (Quote), session-bound ephemeral signing key  
**Why it cannot be bypassed:** Without a hardware-bound identity, the protocol has no anchor to distinguish a real sensor from a software simulation. The device key never leaves the TEE and cannot be extracted or cloned.

> **Layer 1 is the foundational moat.** See Section 3 for full specification.

### 2.2 Layer 2: Data Capture Layer

**Responsibility:** Capture, timestamp, and preprocess multi-modal sensor data from the physical world.

**Input:** Raw sensor streams (IMU, bioimpedance, pressure, ToF, IR, etc.)  
**Output:** Time-synchronized, filtered, normalized multi-dimensional data frames  
**Why it cannot be bypassed:** The 15-dimensional sensor fusion creates a data complexity that is infeasible to simulate with temporal and cross-modal consistency. A software simulation cannot reproduce the physical cross-talk, noise patterns, and micro-timing of real hardware.

### 2.3 Layer 3: Privacy Layer

**Responsibility:** Ensure that raw behavioral data is never exposed to any single party, while still enabling verifiable claims about that data.

**Input:** Normalized sensor data frames (from Layer 2)  
**Output:** MPC-sharded data, ZK-wrapped behavior proof, DID-anchored verifiable credential  
**Why it cannot be bypassed:** Even ZWF (as the protocol developer) cannot access raw user data — it is MPC-sharded across independent parties. This is a structural privacy guarantee, not a policy promise.

### 2.4 Layer 4: Verification Layer

**Responsibility:** Provide a decentralized network of validators that independently verify Behavior Proofs and reach consensus on their validity.

**Input:** ZK-wrapped Behavior Proof (from Layer 3)  
**Output:** Consensus verification result, slashing events for invalid proofs  
**Why it cannot be bypassed:** Proof verification is trustless — any node can verify independently. No centralized authority can unilaterally accept or reject proofs.

### 2.5 Layer 5: Application Layer

**Responsibility:** Enable end-user applications to consume verified Behavior Proofs for domain-specific use cases.

**Input:** Verified Behavior Proof + user authorization  
**Output:** Application-specific outcomes (DID credential issuance, insurance premium calculation, behavior token minting)  
**Why it cannot be bypassed:** Applications consume _verified_ proofs, not raw claims. An application cannot fabricate a proof without going through Layers 1-4.

---

## 3. Hardware Trust Root (Layer 1) — Full Specification

> **中文提示**: 这是PoPB协议最关键的壁垒层。以下每个子组件构成不可绕过的硬件信任锚。

### 3.1 Device Attestation

Every ZWISERFIT gate sensor device is provisioned at the factory with a unique device identity:

```
DeviceIdentity {
    device_id: UUIDv7
    manufacturer: "ZWISERFIT"
    model: string          // e.g., "Gate-Sensor-Gen2"
    hardware_revision: string
    factory_timestamp: ISO8601
    public_key: Ed25519    // device_public_key
    certificate_chain: X.509[]  // signed by ZWF Root CA → Intermediate CA → Device
}
```

The device private key is generated **inside a secure element** (ATECC608B or equivalent) and **never leaves the hardware**. The certificate chain anchors to a ZWF Root CA whose public key is published in the protocol genesis block.

**Attestation flow:**
1. Verifier sends challenge (random nonce) to device
2. Device TEE signs `{challenge, device_quote, timestamp}` with device key
3. Verifier validates signature against on-chain device registry
4. Verifier validates device_quote (measured boot state) against known-good values

### 3.2 Secure Boot Chain

```
ROM Bootloader (immutable)
  → Verify Stage-1 Bootloader signature
    → Stage-1: Verify OS Kernel signature
      → Kernel: Verify Application firmware signature
        → Application: Verify sensor calibration data integrity
```

Each stage cryptographically verifies the next before execution. Any modification to firmware results in a different measurement hash, which is reflected in the device quote and causes attestation to fail.

**Firmware update policy:**
- Updates are signed by ZWF release keys (offline, air-gapped HSM)
- Rollback protection: firmware version counter in secure element, monotonic
- Anti-downgrade: devices reject firmware with version < current version

### 3.3 Trusted Execution Environment (TEE)

Critical operations execute in a hardware-isolated TEE (ARM TrustZone or equivalent):

| Operation | Execution Environment | Rationale |
|-----------|----------------------|-----------|
| Device key operations (sign/decrypt) | Secure Element | Key never exposed to rich OS |
| Behavior proof signing | TEE | Protects signing logic from tampering |
| Sensor data timestamping | TEE | Prevents timestamp manipulation |
| MPC secret sharing | TEE | Raw data split before leaving secure boundary |
| Normal OS operations (network, logging) | Rich OS | Non-critical; compromise does not break attestation |

### 3.4 Tamper-Evident Logging

All security-relevant events are logged to a tamper-evident append-only log:

```
TamperLog {
    event_id: uint64           // monotonic counter
    event_type: enum           // BOOT | ATTESTATION | FIRMWARE_UPDATE | PROOF_SIGN | ANOMALY
    timestamp: uint64          // TEE-sourced clock
    device_quote: hash         // measured boot state at time of event
    payload_hash: hash         // hash of event-specific data
    signature: Ed25519         // signed by device key
    prev_entry_hash: hash      // chained hash (blockchain-style integrity)
}
```

The log is periodically synced to a decentralized storage layer (IPFS/Arweave) for long-term auditability.

### 3.5 15-Dimensional Sensor Fusion

The gate sensor device captures a multi-modal sensor stream with the following dimensions:

| # | Sensor | Data Type | Sampling Rate | Purpose |
|---|--------|-----------|---------------|---------|
| 1 | **Bioimpedance (BIA)** | Complex Z (Ω + phase) | 50 Hz | Body composition, muscle activation detection |
| 2 | **Pressure (strain gauge)** | Force (N), 4-zone | 200 Hz | Weight distribution, balance, rep counting |
| 3 | **IMU Accelerometer** | 3-axis (m/s²) | 200 Hz | Motion trajectory, impact detection |
| 4 | **IMU Gyroscope** | 3-axis (rad/s) | 200 Hz | Angular velocity, rotation patterns |
| 5 | **IMU Magnetometer** | 3-axis (μT) | 100 Hz | Orientation reference |
| 6 | **ToF Depth Sensor** | Distance (mm), 8×8 grid | 30 Hz | Body posture, proximity detection |
| 7 | **IR Thermal Array** | Temperature (°C), 8×8 grid | 10 Hz | Body heat signature, presence detection |
| 8 | **Capacitive Touch** | Capacitance delta, 12-zone | 100 Hz | Foot placement, contact quality |
| 9 | **ECG (single-lead)** | Voltage (μV) | 500 Hz | Heart rate, HRV, biometric identity |
| 10 | **PPG (photoplethysmogram)** | Light absorption | 100 Hz | Heart rate, SpO2 |
| 11 | **Microphone** | Audio (16-bit PCM) | 16 kHz | Breathing patterns, effort vocalization |
| 12 | **Ambient Light** | Lux | 10 Hz | Environment context |
| 13 | **Ambient Temperature** | °C | 1 Hz | Environment context |
| 14 | **Humidity** | %RH | 1 Hz | Environment context |
| 15 | **Barometric Pressure** | hPa | 1 Hz | Altitude/floor detection |

**Fusion rationale:** The cross-modal consistency requirement makes synthetic data generation computationally infeasible. A deepfake would need to simultaneously satisfy physical constraints across all 15 dimensions with correct temporal dynamics, sensor noise characteristics, and cross-modal correlations — a problem significantly harder than generating plausible video or audio alone.

---

## 4. Behavior Proof Generation (Layers 2-3)

### 4.1 Proof Generation Pipeline

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│ EXERCISE │ →  │ SENSOR ARRAY │ →  │ SIGNAL PROC  │ →  │ FEATURE EXTR│
│ SESSION  │    │ (15-dim raw) │    │ (filter/norm)│    │ (rep count, │
└──────────┘    └──────────────┘    └──────────────┘    │ form quality)│
                                                        └──────┬───────┘
                                                               ↓
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│ VERIFIED │ ←  │ ZK-PROOF     │ ←  │ MPC SHARDING │ ←  │ CRYPTO      │
│ BP       │    │ GENERATION   │    │ (privacy)    │    │ SIGNING     │
└──────────┘    └──────────────┘    └──────────────┘    └─────────────┘
```

**Step-by-step:**

1. **Session Initiation:** User steps on gate sensor. Device attestation completes. Session-bound ephemeral key generated in TEE.

2. **Raw Data Capture:** 15-dimensional sensor stream recorded at native sampling rates for the duration of the exercise session.

3. **Signal Processing:** On-device DSP pipeline (in TEE):
   - Anti-aliasing filters
   - Sensor calibration correction
   - Cross-modal time synchronization (to μs precision)
   - Motion artifact removal (adaptive filtering)

4. **Feature Extraction:** ML inference on processed signals:
   - Exercise type classification
   - Repetition counting with confidence score
   - Form quality assessment (deviation from ideal trajectory)
   - Biometric consistency check (same person throughout session)

5. **MPC Sharding:** Raw sensor data is split into N shares via Shamir's Secret Sharing (or additive secret sharing) with threshold K < N. Shares are distributed to independent storage parties. No single party can reconstruct the original data. ZWF holds ≤K-1 shares.

6. **ZK-Proof Generation:** A zero-knowledge proof is generated that asserts:
   - "A valid behavior event occurred on device D at time T"
   - "The event involved exercise type E with R repetitions"
   - "The form quality score meets threshold Q"
   - WITHOUT revealing: the raw sensor data, the user's identity, or biometric features

7. **Proof Assembly:** The final Behavior Proof is assembled and signed by the device's TEE-resident key.

### 4.2 Behavior Proof JSON Schema

```json
{
  "$schema": "https://popb.zwf.io/schemas/behavior-proof-v1.json",
  "type": "object",
  "required": ["proof_id", "protocol_version", "device_attestation", "behavior_claim", "zk_proof", "timestamp", "signature"],
  "properties": {
    "proof_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique proof identifier (UUIDv7, time-sortable)"
    },
    "protocol_version": {
      "type": "string",
      "pattern": "^\\d+\\.\\d+\\.\\d+$",
      "description": "PoPB protocol version (semver)"
    },
    "device_attestation": {
      "type": "object",
      "required": ["device_id", "quote", "challenge"],
      "properties": {
        "device_id": {"type": "string"},
        "quote": {"type": "string", "description": "TEE attestation quote (base64)"},
        "challenge": {"type": "string", "description": "Verifier challenge nonce"},
        "measured_boot_hash": {"type": "string", "description": "SHA-256 of measured boot log"}
      }
    },
    "behavior_claim": {
      "type": "object",
      "required": ["exercise_type", "repetition_count", "duration_ms", "form_quality_score"],
      "properties": {
        "exercise_type": {
          "type": "string",
          "enum": ["squat", "push_up", "lunge", "plank", "jumping_jack", "burpee", "custom"]
        },
        "repetition_count": {"type": "integer", "minimum": 1},
        "duration_ms": {"type": "integer", "minimum": 0},
        "form_quality_score": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "heart_rate_avg": {"type": "integer", "minimum": 30, "maximum": 250},
        "calories_estimate": {"type": "number", "minimum": 0},
        "sensor_fusion_hash": {"type": "string", "description": "Merkle root of sensor data chunks"}
      }
    },
    "zk_proof": {
      "type": "object",
      "required": ["proof_system", "proof_data", "public_inputs"],
      "properties": {
        "proof_system": {
          "type": "string",
          "enum": ["groth16", "plonk", "halo2", "nova"],
          "description": "ZK proof system used"
        },
        "proof_data": {"type": "string", "description": "Serialized ZK proof (base64)"},
        "public_inputs": {
          "type": "array",
          "items": {"type": "string"},
          "description": "Public inputs to the ZK circuit"
        },
        "verification_key_hash": {"type": "string", "description": "Hash of the ZK verification key"}
      }
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp from device TEE clock"
    },
    "mpc_commitment": {
      "type": "object",
      "description": "Commitments to MPC-sharded raw data",
      "properties": {
        "shard_count": {"type": "integer", "minimum": 3},
        "threshold": {"type": "integer", "minimum": 2},
        "shard_hashes": {
          "type": "array",
          "items": {"type": "string"},
          "description": "SHA-256 hash of each shard"
        },
        "storage_parties": {
          "type": "array",
          "items": {"type": "string"},
          "description": "DIDs of MPC storage parties"
        }
      }
    },
    "did_anchor": {
      "type": "object",
      "properties": {
        "subject_did": {"type": "string", "description": "User DID (pseudonymous)"},
        "credential_type": {"type": "string", "description": "W3C Verifiable Credential type"}
      }
    },
    "signature": {
      "type": "string",
      "description": "Ed25519 signature over all fields above, by device TEE key"
    }
  }
}
```

### 4.3 Zero-Knowledge Proof Integration

The ZK circuit for PoPB proves the following statement:

```
I know a device attestation quote Q, sensor data D, and feature vector F such that:

1. Q is a valid attestation from a registered device
2. F = f_sensor_fusion(D) where f_sensor_fusion is the agreed-upon feature extraction algorithm
3. F.exercise_type = CLAIMED_TYPE
4. F.repetition_count >= CLAIMED_REPS
5. F.form_quality_score >= CLAIMED_QUALITY_THRESHOLD
6. F.biometric_hash = h(D.biometric_features)  // optional biometric binding

Without revealing: D, F, or the user's identity
```

**Key property:** The verifier learns that a real device observed a real behavior, but learns nothing about the user. This enables **anonymous reputation**: a user can accumulate verified behavior history without linking it to their real-world identity.

**Circuit implementation options:**
- **Groth16** (current recommendation): Smallest proof size (~200 bytes), fastest verification, requires trusted setup
- **PLONK**: Universal trusted setup, larger proofs (~1KB), good for frequent circuit updates
- **Nova** (future): Recursive proof composition, enables proof aggregation across sessions

### 4.4 MPC Privacy Architecture

```
               ┌─────────────┐
               │  USER DEVICE │
               │  (TEE)       │
               └──────┬───────┘
                      │ Raw sensor data
                      │ Shamir(3,5) secret sharing
          ┌───────────┼───────────┐
          ↓           ↓           ↓
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ SHARD 1  │ │ SHARD 2  │ │ SHARD 3  │  ...
    │ (Party A)│ │ (Party B)│ │ (Party C)│
    │ IPFS pin │ │ Arweave  │ │ Filecoin │
    └──────────┘ └──────────┘ └──────────┘
          │           │           │
          └───────────┼───────────┘
                      │ Only with K≥3 shards can data be reconstructed
                      │ ZWF holds ≤2 shards → cannot unilaterally read data
```

**Privacy guarantees:**
- ZWF (protocol developer) **cannot** reconstruct raw user data (holds < K shares)
- Data consumers only receive ZK proofs, never raw data
- Users can authorize specific data consumers to access their data by releasing decryption keys
- Authorizations are time-bound and revocable (via DID-based capability system)

---

## 5. Verification Layer (Layer 4)

### 5.1 Validator Network Architecture

The PoPB verification network is a permissionless, stake-weighted validator set that independently verifies Behavior Proofs.

```
┌──────────────────────────────────────────────────────┐
│                   VERIFIER NETWORK                    │
│                                                      │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐            │
│  │Validator│   │Validator│   │Validator│  ...N      │
│  │  Node 1 │   │  Node 2 │   │  Node 3 │            │
│  │ (stake) │   │ (stake) │   │ (stake) │            │
│  └────┬────┘   └────┬────┘   └────┬────┘            │
│       │             │             │                  │
│       └─────────────┼─────────────┘                  │
│                     │                                │
│              ┌──────┴──────┐                         │
│              │ CONSENSUS   │                         │
│              │ (BFT-style) │                         │
│              └──────┬──────┘                         │
│                     │                                │
│              ┌──────┴──────┐                         │
│              │ PROOF STATE │                         │
│              │ (Merkle Tree│                         │
│              │  on L2)     │                         │
│              └─────────────┘                         │
└──────────────────────────────────────────────────────┘
```

### 5.2 Proof Validation Algorithm

Each validator independently executes the following verification steps:

```
function validateBehaviorProof(bp: BehaviorProof) → ValidationResult:
    // Step 1: Device attestation check
    if not verifyDeviceAttestation(bp.device_attestation):
        return INVALID_DEVICE

    // Step 2: Signature verification
    if not verifySignature(bp, bp.device_attestation.device_id):
        return INVALID_SIGNATURE

    // Step 3: ZK proof verification
    if not verifyZKProof(bp.zk_proof):
        return INVALID_ZK_PROOF

    // Step 4: Timestamp sanity check
    if bp.timestamp > now() + MAX_CLOCK_DRIFT:
        return FUTURE_TIMESTAMP
    if bp.timestamp < bp.device_attestation.quote.issued_at:
        return TIMESTAMP_BEFORE_ATTESTATION

    // Step 5: Replay check
    if proofRegistry.exists(bp.proof_id):
        return DUPLICATE_PROOF

    // Step 6: Device registration check
    if not deviceRegistry.isActive(bp.device_attestation.device_id):
        return DEVICE_NOT_REGISTERED

    return VALID
```

Consensus requires **≥2/3 of stake-weighted validators** to agree on validity within a validation window (target: 2-5 seconds).

### 5.3 Slashing Conditions

Validators must stake tokens (PoPB native token or restaked ETH via EigenLayer) as collateral. The following conditions result in slashing:

| Slashing Condition | Severity | Penalty | Description |
|--------------------|----------|---------|-------------|
| **Double-voting** | Critical | 100% slash | Voting for two conflicting validation results for the same proof |
| **Invalid validation** | High | 50% slash | Signing a validation result that the supermajority disagrees with (repeated offenses) |
| **Liveness failure** | Medium | 5% slash | Failing to participate in consensus for N consecutive epochs |
| **Collusion** | Critical | 100% slash + ban | Coordinated acceptance of invalid proofs (detected via statistical anomaly) |

### 5.4 EigenLayer / Restaking Integration

PoPB can leverage EigenLayer's restaking infrastructure to bootstrap validator security:

```
┌────────────────────────────────────────┐
│           EIGENLAYER (ETH L1)          │
│  ┌──────────────────────────────────┐  │
│  │  ETH Validators restake to PoPB  │  │
│  │  → Inherit ETH economic security │  │
│  └──────────────┬───────────────────┘  │
│                 │                       │
│  ┌──────────────┴───────────────────┐  │
│  │  PoPB AVS (Actively Validated    │  │
│  │  Service) on EigenLayer          │  │
│  │  → PoPB-specific slashing rules  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

**Benefits:**
- Bootstraps validator security from day one (no need to build token value organically)
- ETH stakers earn additional yield by validating PoPB proofs
- PoPB inherits Ethereum's economic security guarantees

---

## 6. DID + Data Sovereignty (Layer 5)

### 6.1 User DID Architecture

Each PoPB user is represented by a Decentralized Identifier (DID) following the W3C DID Core specification:

```
did:popb:0x7a3b...c4f1
```

**DID Document structure:**
- `id`: The DID itself
- `verificationMethod`: Ed25519 public key for authentication
- `service`: MPC shard locator endpoints
- `capability`: Data authorization tokens (time-bound, revocable)

### 6.2 Data Authorization Model

The user maintains **absolute sovereignty** over their behavioral data:

```
┌──────────┐         ┌──────────────┐         ┌──────────────┐
│   USER   │────────▶│ AUTHORIZATION│────────▶│    DATA      │
│  (DID)   │ grants  │   TOKEN      │ enables │  CONSUMER    │
└──────────┘         │ (time-bound, │         └──────────────┘
                     │  revocable)  │
                     └──────────────┘
```

**Authorization flow:**
1. Data consumer requests access to user's behavior data
2. User signs an authorization token specifying: scope, duration, consumer DID
3. Authorization token is recorded on-chain or in a verifiable data registry
4. MPC storage parties verify the token and release decrypted shards to the consumer
5. Authorization automatically expires at the specified time
6. User can revoke authorization at any time

**Key principle:** ZWF cannot access user data without explicit user authorization. By protocol design, ZWF holds only a subset of MPC shards — insufficient for reconstruction.

### 6.3 Regulatory Compliance

| Regulation | PoPB Compliance Mechanism |
|------------|--------------------------|
| **GDPR (EU)** | User DID = data controller; ZWF = data processor (by design, cannot read data); Right to erasure: revoke authorization → data becomes unreconstructable |
| **HIPAA (US)** | Raw health data never leaves TEE in identifiable form; ZK proofs reveal only aggregated statistics; Audit trail maintained in tamper-evident log |
| **中国《个人信息保护法》(PIPL)** | 数据本地化: MPC shards可配置在中国境内存储; 单独同意: 每次数据授权需用户显式签名; 最小必要: ZK证明仅暴露聚合统计量,不暴露原始数据 |

---

## 7. Protocol Governance

### 7.1 PoPB Improvement Proposal (PIP) Process

The protocol evolves through a formal RFC-style proposal process:

| Stage | Name | Description |
|-------|------|-------------|
| **PIP-0** | Idea | Informal discussion on PoPB forum/discord |
| **PIP-1** | Draft | Formal proposal document following PIP template |
| **PIP-2** | Review | Technical review by protocol maintainers |
| **PIP-3** | Last Call | Community review period (minimum 2 weeks) |
| **PIP-4** | Accepted | Merged into protocol specification |
| **PIP-5** | Deployed | Implemented in reference implementation & testnet |
| **PIP-X** | Rejected/Withdrawn | Proposal did not reach consensus |

### 7.2 Multi-Stakeholder Governance

Governance power is distributed across four stakeholder groups:

| Stakeholder | Representation | Voting Power | Role |
|-------------|---------------|--------------|------|
| **Device Manufacturers** | Hardware Working Group | 25% | Hardware spec evolution, sensor standards |
| **Validators** | Validator DAO | 25% | Network parameters, slashing conditions |
| **Users (Data Subjects)** | User Council | 25% | Privacy parameters, data sovereignty rules |
| **Developers** | Protocol Guild | 25% | Technical direction, reference implementation |

**Veto mechanism:** Any single stakeholder group can veto a protocol change that threatens their fundamental interests (e.g., users can veto any change that weakens privacy guarantees).

### 7.3 Licensing

- **Protocol Specification:** MIT License — anyone can implement, extend, or fork
- **Reference Implementation:** Apache 2.0 — patent grant included, protects against patent lawsuits
- **Hardware Design Files:** CERN OHL v2 (Permissive) — open hardware, attribution required
- **Patent Non-Assertion Pledge:** ZWF pledges not to assert patents against conformant implementations of the PoPB protocol

---

## 8. Roadmap

### 8.1 Version Timeline

| Version | Target Date | Key Deliverables | Status |
|---------|-------------|------------------|--------|
| **v1.0** | 2026-Q2 (now) | Protocol specification v1.0, Reference SDK (Python/Rust), Device attestation client, Test vectors for proof validation | ✅ Current |
| **v1.1** | 2026-Q3 | ZK-circuit v1 (Groth16), ZK-proof integration with reference SDK, Private testnet (5 validators), Sensor fusion benchmark suite | 🔨 In Development |
| **v2.0** | 2027-Q1 | Mainnet validator network, EigenLayer AVS integration, PoPB token economics specification, Hardware certification program, MPC storage network (5+ independent parties) | 📋 Planned |
| **v2.5** | 2027-Q3 | Cross-device federation (multi-gate gym scenarios), Behavior proof aggregation (recursive ZK), Application SDKs (mobile/web), DID registry on L2 | 📋 Planned |
| **v3.0** | 2028 | Cross-chain behavior proof bridge, PoPB→Ethereum, Solana, Polkadot, Advanced ZK (Nova folding), Formal verification of critical components, On-chain behavior marketplace | 🔮 Vision |

### 8.2 Reference Implementation Stack

```
┌─────────────────────────────────────────┐
│          APPLICATION SDKs               │
│  TypeScript · Python · Swift · Kotlin   │
├─────────────────────────────────────────┤
│          PROTOCOL LIBRARY               │
│  Rust (core) · WASM (browser)           │
│  - Behavior Proof encoding/decoding     │
│  - Verification logic                   │
│  - DID operations                       │
├─────────────────────────────────────────┤
│          DEVICE RUNTIME                 │
│  C (TEE) · Rust (sensor fusion)         │
│  - Attestation client                   │
│  - Sensor signal processing             │
│  - ZK proof generation (circuit)        │
└─────────────────────────────────────────┘
```

---

## 9. Security Considerations

### 9.1 Threat Model

| Threat | Mitigation | Residual Risk |
|--------|-----------|---------------|
| Device physical tampering | Secure element, tamper-evident seals, anomaly detection | Determined attacker with lab equipment (< 0.01%) |
| Firmware compromise | Secure boot chain, signed updates, measured boot | Supply chain attack on factory provisioning (mitigated by multi-party provisioning ceremony) |
| Sybil attacks (fake devices) | Hardware attestation, on-chain device registry | Manufacturer key compromise (mitigated by HSM, multi-sig root key) |
| Replay attacks | Unique proof_id, timestamp validation, verifier challenge nonce | Timestamp manipulation via GPS spoofing (mitigated by TEE clock + network time consensus) |
| Privacy attacks (data reconstruction) | MPC sharding, ZK proofs, data minimization | Side-channel leakage from metadata (ongoing research) |
| Collusion attack (validators) | Statistical anomaly detection, stake slashing, diverse validator set | Majority collusion (mitigated by high stake requirements + EigenLayer security inheritance) |

### 9.2 Cryptographic Agility

All cryptographic primitives are parameterized to allow migration to post-quantum algorithms when standards mature:

- Current: Ed25519 (signatures), SHA-256 (hashing), Groth16 (ZK)
- Future migration path: CRYSTALS-Dilithium (signatures), SHA-3 (hashing), STARK-based (ZK)

---

## 10. References

1. W3C Decentralized Identifiers (DIDs) v1.0 — https://www.w3.org/TR/did-core/
2. W3C Verifiable Credentials Data Model v1.1 — https://www.w3.org/TR/vc-data-model/
3. Groth16: "On the Size of Pairing-based Non-interactive Arguments" — EUROCRYPT 2016
4. EigenLayer Whitepaper — https://docs.eigenlayer.xyz/
5. ARM TrustZone Technology — https://developer.arm.com/ip-products/security-ip/trustzone
6. Shamir, A. "How to Share a Secret" — Communications of the ACM, 1979
7. GDPR Regulation (EU) 2016/679
8. HIPAA Privacy Rule — 45 CFR Part 160 and Subparts A and E of Part 164
9. 中华人民共和国个人信息保护法 (2021)

---

> **PoPB v1.0 Specification — End of Document**
>
> *"What TCP/IP did for the internet, PoPB does for human physical behavior data: an open protocol, a shared language, and a trustless bridge between the physical and the digital."*
>
> — PoPB Protocol Authors, June 2026
