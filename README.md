# agent-matrix

[English](README.en.md) · [采用指南](docs/ADOPTION.md) · [完整示例](docs/EXAMPLE.md) · [MIT](LICENSE)

**让多 Agent 协作成为需求清楚、设计统一、质量可验证的研发闭环。**

agent-matrix 是轻量、技术栈中立的工程方法包：用少量 Markdown 事实源、稳定契约和审核门禁，减少 Agent 猜需求、改错接口、覆盖成果或“代码写完就算完成”的问题。

面向开发者、技术负责人和开源维护者。可由一个人或多个 Agent 采用，不要求购买指定模型、安装编排平台或重组业务目录。

## 核心闭环

```mermaid
flowchart LR
    PRD[需求 PRD] --> DESIGN[设计 DESIGN]
    DESIGN --> TASKS[任务 TASKS]
    TASKS --> CODE[实现与测试]
    CODE --> REVIEW[审核 REVIEW]
    REVIEW --> DONE[验收 DONE]
```

- **需求与契约先行**：CONFIRMED / INFERRED / TODO_CONFIRM 区分依据；Task 绑定需求、设计、文件与验证。
- **协作与上下文受控**：按需加载、单写入、明确认领和交接；优先复用已有体系，不创建平行进度源。
- **完成必须有证据**：真实测试、多轮追加审核、P0/P1 熔断，满足验收后才能 DONE。

## 一分钟开始

1. 在 [采用指南](docs/ADOPTION.md#接入步骤)确认接入方式，复制其中的完整“初始化 Prompt”到你的项目 Agent。
2. 让 Agent 先检查 Git、现有规则和真实代码，再增量建立或复用事实源。已有修改和业务结构必须保留。
3. 审阅初始化报告并确认待定问题，再下达“执行 TASK-xxx”或一个范围明确的 Goal。初始化本身不会开发或提交代码。

**不要把本仓库的 PRD/TASKS 直接复制成你项目的需求与进度。** 它们是 agent-matrix 自己的维护实例；采用指南里的模板才是供外部填充的空白契约。

## 交付物导航

| 资产 | 用途 |
| --- | --- |
| [采用指南与模板](docs/ADOPTION.md) | 完整初始化 Prompt、AGENTS/PRD/DESIGN/TASKS 模板、增量接入与演进 |
| [完整示例](docs/EXAMPLE.md) | EX- 需求 → 设计 → 任务 → 可执行红绿灯测试 → 示意审核与完成 |
| [统一 Agent 规则](AGENTS.md) | 本仓库维护规则；按需加载、十条铁律与认领协议的有效实例 |
| [PRD](docs/PRD.md) / [DESIGN](docs/DESIGN.md) / [TASKS](docs/TASKS.md) | 本仓库唯一需求、设计与任务事实源 |
| [审核规范](docs/reviews/README.md) | 单任务单主报告、多轮追加、严重度及完成门禁 |
| [贡献指南](CONTRIBUTING.md) | 变更、检查与精确提交准备 |

最小目标项目只需根 AGENTS、三个文档事实源和 reviews；已有等价体系直接映射。Java/Spring、Python、Node.js/全栈、CLI/库或纯文档项目都按真实结构适配，不强制 Controller/Service 或某个包管理器。

## 验证本仓库

获取仓库后，在根目录使用 Python 3.9+；单测和提交检查另需 Git CLI，无第三方依赖或服务。

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_docs.py
python3 scripts/check_docs.py --example-red
python3 scripts/check_docs.py --example
```

准备提交后再运行 `python3 scripts/check_docs.py --staged`，检查的是真实暂存内容及其与工作区的一致性。命令不会替你暂存、提交或推送。

红灯命令只有在测试发现有意缺陷时成功；绿灯要求 14 个边界/类型案例全部通过。工具覆盖本地链接/锚点、追踪关系、统计/依赖、完成证据、许可和提交卫生；外部项目复用检查器时须适配自己的事实源格式与发布清单。

## 适用边界

本版交付生产导向的工程规范与本地验证，不提供自动 Agent 调度、分布式锁或云部署服务；不声称已在所有技术栈生产验证。人工协调不是原子互斥，静态检查也不能代替需求、安全和生产环境审核。

Codex、Claude、Hermes、Gemini 的角色只是能力分工建议，可以替换；作者自检和真实独立审核必须区分。初始化历史记录保留作审计，不是安装指南或额外进度源。

欢迎按 [贡献流程](CONTRIBUTING.md)提出问题和改进。许可为 [MIT](LICENSE)，版权署名 agent-matrix contributors。
