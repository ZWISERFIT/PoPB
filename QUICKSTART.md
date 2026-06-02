# PoPB Quickstart — 5 分钟上手

> 想理解 PoPB 协议并跑通第一个验证流程？你只需要一个终端和 5 分钟。

---

## 前提

- 终端（Linux / macOS / WSL）
- `python3` + `openssl`
- 不需要区块链节点、不需要特殊硬件

---

## 三步走

### Step 1: 理解一个行为事件

PoPB 的核心是一个 JSON 对象，长这样：

```json
{
  "event_id": "evt_20260602_001",
  "member_did": "did:zwf:0x7a3b...",
  "event_type": "heart_rate_reading",
  "timestamp": 1750000000000,
  "source_device": "polar_h10_chest_strap",
  "payload": {
    "heart_rate_bpm": 142,
    "duration_seconds": 300,
    "zone": "cardio"
  }
}
```

这就是 ZWF-20 数据标准定义的格式。每个行为事件都绑定到一个 DID（去中心化身份）。

---

### Step 2: 生成你的第一个证明

```bash
# 1. 克隆仓库
git clone https://github.com/ZWISERFIT/PoPB.git && cd PoPB

# 2. 创建一个测试事件
cat > test-event.json << 'EOF'
{"event_id":"test_001","member_did":"did:example:test","event_type":"demo","timestamp":1700000000000,"source_device":"demo","payload":{"demo":true}}
EOF

# 3. 计算哈希（这就是链上存证的内容）
cat test-event.json | openssl dgst -sha256
# 输出: SHA2-256(test-event.json)= <一串十六进制>

# 4. 模拟 Agent 签名（ED25519）
openssl genpkey -algorithm ED25519 -out demo-key.pem
cat test-event.json | openssl dgst -sha256 -sign demo-key.pem -out test-event.sig
echo "✅ 签名已生成 (test-event.sig)"
```

---

### Step 3: 理解证明链

```
  [传感器采集] → [ZWF-20格式化] → [SHA-256哈希]
       ↓
  [Agent ED25519签名] → [hash-chain.jsonl]
       ↓
  [Merkle Tree聚合] → [GitHub commit] → [链上锚定]
```

你刚才在 Step 2 做的是：
- ✅ 创建了一个 ZWF-20 格式的事件
- ✅ 计算了它的 SHA-256 哈希（即链上存证的内容）
- ✅ 用 ED25519 签了名

真实的 PoPB 管线会在门店自动完成这整个流程——从门禁"哔"一声开始。

---

## 下一步

| 想做的事 | 看这里 |
|----------|--------|
| 理解协议全貌 | `spec/PoPB-Protocol-Spec-v1.0.md` |
| 了解数据标准 | `standards/ZWF20-Behavior-Data-Standard-v1.0.md` |
| 追溯信任架构 | `trust/TRUST-Architecture-v1.0.md` |
| 了解完整管线 | `attestation-flow.md` |
| 接入你的设备 | 提交一个 [Hardware Integration Issue](https://github.com/ZWISERFIT/PoPB/issues/new?template=hardware-integration.yml) |
| 提议协议改进 | 提交一个 [PIP](https://github.com/ZWISERFIT/PoPB/issues/new?template=pip-proposal.yml) |

---

## 常见问题

**Q: 我需要真实传感器吗？**
不需要。协议的验证逻辑对模拟数据和真实数据一视同仁——都是 SHA-256 输入。

**Q: 我需要区块链钱包吗？**
了解协议不需要。接入验证节点时需要 DID 密钥对。

**Q: 这个协议和 Strava/Apple Health 有什么区别？**
那些是平台。PoPB 是协议——你的数据用你的 DID 签名，平台技术上无法访问原始数据。

---

*5 分钟到。你现在理解了 PoPB 的核心循环：采集 → 格式化 → 签名 → 哈希 → 链上。*
