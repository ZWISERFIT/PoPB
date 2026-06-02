# Contributing to PoPB

首先——感谢你愿意贡献。PoPB (Proof of Physical Behavior) 是一个开放协议，所有改进都通过社区驱动的 PIP 流程完成。

---

## 行为准则

本项目采用 [Contributor Covenant v2.1](CODE_OF_CONDUCT.md)。一句话：专业、尊重、就事论事。

---

## PIP 流程（PoPB Improvement Proposal）

所有协议级的改动——新增字段、修改证明流程、升级数据标准——必须走 PIP。

### PIP 可以是什么？

- 新增行为事件类型（如：新增 `sleep_quality` 事件到 ZWF-20）
- 修改证明链的密码学方案（如：从 SHA-256 升级）
- 新增硬件设备支持（如：接入 Apple Watch 心率数据）
- 改进隐私保护机制（如：新增 MPC 聚合方案）

### PIP 怎么做？

1. **开 Issue** → 使用 [PIP Proposal 模板](https://github.com/ZWISERFIT/PoPB/issues/new?template=pip-proposal.yml)
2. **社区讨论** → 至少 7 天公开讨论期
3. **技术验证** → 提供 PoC 代码或测试数据
4. **核心维护者审阅** → 至少 1 位维护者 Approve
5. **合并** → PR 合并到 `main`，PIP 编号归档到 `pips/` 目录

---

## 开发环境

```bash
git clone https://github.com/ZWISERFIT/PoPB.git
cd PoPB

# 验证哈希链完整性
python3 -c "
import hashlib, json
# 读取根哈希
with open('ROOT-HASH.md') as f: print(f.read()[:200])
print('✅ Repo 克隆成功 — 哈希链可独立验证')
"
```

### 提交规范

- Commit message 格式：`<type>: <description>`
- 类型：`feat` / `fix` / `docs` / `spec` / `pip`
- 示例：`spec: add sleep_quality event type to ZWF-20`

**重要：不要修改 `hash-chain.jsonl` 或 `ROOT-HASH.md`。** CI 会自动更新哈希链。

---

## 硬件集成

如果你想把新的传感器 / 可穿戴设备接入 PoPB 验证层：

1. 开 [Hardware Integration Issue](https://github.com/ZWISERFIT/PoPB/issues/new?template=hardware-integration.yml)
2. 提供设备数据格式示例（JSON/CSV）
3. 说明如何映射到 ZWF-20 字段
4. 我们会协助你完成适配

**目前已支持的设备类型：**
- 心率传感器（Polar H10 / 兼容 BLE HRM）
- 体测仪（InBody 兼容格式）
- 门禁系统（任意输出时间戳 + ID 的硬件）

---

## 许可证

本仓库采用双许可：
- 协议规范文档：PDL (Protocol Definition License)
- 参考实现代码：Apache 2.0

贡献即表示你同意在相同许可下发布你的贡献。

---

*有问题？开一个 [普通 Issue](https://github.com/ZWISERFIT/PoPB/issues/new) 就行。*
