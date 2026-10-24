# 任务与进度唯一事实源

## 全局看板

更新日期：2026-10-24。只统计实际任务；模板和 EX- 示例不计入。

| Total | TODO | IN_PROGRESS | BLOCKED | REVIEW | DONE |
| --- | --- | --- | --- | --- | --- |
| 6 | 0 | 0 | 0 | 0 | 6 |

| 焦点 | 当前值 |
| --- | --- |
| P0 | 无 |
| P1 | TASK-001（DONE）、TASK-002（DONE）、TASK-004（DONE）、TASK-005（DONE）、TASK-006（DONE） |
| P2 | TASK-003（DONE） |
| P3 | 无 |
| 阻塞项 | 无 |
| 进行中 | 无 |
| 下一可执行任务 | 无；当前 Goal 完成后等待新指令 |

**CONFIRMED**：当前授权范围为方法包文档、示例、验证工具与提交准备，不是业务系统开发。Owner 在任务被选择时登记，同一时间只允许一位写入者；共享事实源由当前唯一执行者串行更新。

依赖链：TASK-001 → TASK-002 → TASK-004 → TASK-005；TASK-003 依赖 TASK-002；TASK-006 汇总 TASK-003/004/005。未来新增业务或平台任务必须另有确认后的 PRD + DESIGN。

## TASK-001 确认首版产品范围与验收场景

- PRD：REQ-004、REQ-005、REQ-006；Q-001～Q-003。
- DESIGN：DESIGN-004（解除其范围阻塞的决策任务，不是实现任务）。
- Priority：P1。
- Status：DONE。
- Depends On：无。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权本 Goal 后串行认领。
- Target Module：产品范围与治理文档。
- Target Files：`docs/PRD.md`、`docs/DESIGN.md`、`docs/TASKS.md`（本次初始化建立的真实文件）。
- Target API / Method：不适用（仅负责人决策与文档维护）。
- Implementation：
  1. 负责人选择本任务后，重读 Git、当前任务和关联需求/设计；登记唯一 Owner 与 IN_PROGRESS。
  2. 获取负责人对 Q-001～Q-003 的明确回答，记录首版用户、交付形态、必做/不做、协作与云端边界、成功/失败场景。需要决策但未回复时转 BLOCKED，不以等待时间代替确认。
  3. 已确认事项标 CONFIRMED，记录负责人、日期与依据；清理对应待确认列表，更新统计；保留未确认问题，不自动否定候选需求。
  4. 同步 DESIGN-004 的决策记录和 TASK-002 输入；不自行选择技术栈或编写代码。
  5. 核对所有验收场景可判定，创建 `docs/reviews/TASK-001-review.md` [NEW] 并进入 REVIEW；依据规范闭环问题。
- Acceptance Criteria：范围和相关问题已由负责人明确决策；REQ/设计/任务引用及统计一致；审核完成且无未解决 P0/P1；文档链接和路径检查通过。编译与业务测试 N/A（纯文档任务），必须如实记录，不得写为通过。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-001-review.md`。

## TASK-002 定稿首版技术设计与共享契约

- PRD：REQ-001、REQ-003、REQ-004、REQ-005、REQ-006（采用 TASK-001 确认后的范围）。
- DESIGN：DESIGN-001、DESIGN-003、DESIGN-004。
- Priority：P1。
- Status：DONE。
- Depends On：TASK-001。
- Previous Blocker：等待 TASK-001 记录已获得的范围与许可决定；本版不设计业务运行时共享契约。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权 Goal，串行认领。
- Target Module：技术设计与任务规划。
- Target Files：`docs/DESIGN.md`、`docs/TASKS.md`、`AGENTS.md`；业务源码目标文件为 TBD（由设计确认后绑定，当前不创建或修改）；若决策改变需求，先回写 `docs/PRD.md`。
- Target API / Method：不适用（仅设计）；未来产品契约为 TBD，不能在本任务自行实现。
- Implementation：
  1. 依赖 DONE 后重扫真实仓库、读取关联事实源，登记 Owner 与 IN_PROGRESS。确认技术约束，提出最小方案，按“复用 → 扩展 → 新增”设计。
  2. 按范围补齐 DESIGN-004 或新增稳定设计 ID：模块与调用链、真实/新增路径、构建测试策略、适用的 API/Service/DTO/数据库契约；不适用项写明理由，未定项保留 TODO_CONFIRM 并阻塞相应实现。
  3. 按复杂度记录并发、事务、重试、一致性、兼容、风险与恢复；需要数据库变更只写草案，不执行 DDL。
  4. 将 DESIGN 中六项契约检查映射到已确认技术栈和实际组件，不存在的层标 N/A 并解释，按实际需要增补检查，不为检查表引入分层；先消除冲突，再向负责人提交涉及公共契约或重大架构的方案，确认前不得标 APPROVED。
  5. 依据确认后的 PRD + DESIGN 追加可执行的实现任务，真实文件存在才引用；新增路径标 [NEW]。核心逻辑任务必须明确先编写/更新测试验证边界与预期，或同步编写单元/集成测试，确保覆盖后才提审；仅登记任务，不执行。
  6. 仅在存在真实入口后更新 AGENTS 的构建/测试命令；创建 `docs/reviews/TASK-002-review.md` [NEW]，完成设计与文档审核。
- Acceptance Criteria：所选首版范围存在确定性契约与测试策略，必需的负责人批准有记录；六项检查无未解决冲突；任务映射完整且不重复造轮子；无未解决 P0/P1。编译/业务测试 N/A（设计任务），未创建或执行代码、依赖、DDL 或部署。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-002-review.md`。

## TASK-003 同步中英文项目说明

- PRD：REQ-001、REQ-003、REQ-004、REQ-007。
- DESIGN：DESIGN-001、DESIGN-003、DESIGN-004、DESIGN-005。
- Priority：P2。
- Status：DONE。
- Depends On：TASK-002。
- Previous Blocker：产品范围与技术设计未定，不能补写不存在的安装、使用或部署步骤。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权 Goal，串行认领。
- Target Module：项目说明。
- Target Files：`README.md`、`README.en.md`、`docs/TASKS.md`。
- Target API / Method：不适用。
- Implementation：
  1. 依赖 DONE 后重新读取两份 README 和最新设计；检查用户修改后登记唯一 Owner 与 IN_PROGRESS。
  2. 使用已确认定位替换占位介绍和章节；区分规划与已实现能力；增加到四类事实源的导航，不复制需求、契约或进度正文。
  3. 安装/构建/测试仅写实际存在的入口；尚无实现时明确未提供，不编造可执行步骤；中英文含义保持一致。
  4. 检查相对链接、事实与双语一致性，创建 `docs/reviews/TASK-003-review.md` [NEW] 并审核。
- Acceptance Criteria：两份说明准确反映确认范围与实际实现，消除未经证实的生产就绪表述或清晰标为愿景；链接有效，审核无未解决 P0/P1；无代码变更。编译/业务测试 N/A（文档任务），如未来加入真实运行指引，须记录其实际验证结果与限制。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-003-review.md`。

## TASK-004 交付可移植采用指南、模板与完整示例

- PRD：REQ-003、REQ-004、REQ-005、REQ-007、REQ-009。
- DESIGN：DESIGN-003、DESIGN-005。
- Priority：P1。
- Status：DONE。
- Depends On：TASK-002。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权 Goal，串行认领。
- Target Module：通用方法包。
- Target Files：`AGENTS.md`、`docs/reviews/README.md`、`.gitignore`；`docs/ADOPTION.md` [NEW]、`docs/EXAMPLE.md` [NEW]、`CONTRIBUTING.md` [NEW]、`LICENSE` [NEW]。
- Target API / Method：不适用（文档与许可）。
- Implementation：先按 DESIGN-005 定义模板字段和认领/交接协议；提供可独立复制的初始化 Prompt 与技术栈映射；示例标 EX-，验证输出由 TASK-005 真实运行补入；更新常驻规则与初始化模式边界；增加 MIT 与本地配置忽略规则，不删除本地文件。最后创建 `docs/reviews/TASK-004-review.md` [NEW] 并核对链接、字段、许可与范围。
- Acceptance Criteria：模板无需本机历史文件即可采用；SIMPLE/NORMAL/COMPLEX 有深度标准；人工协调不冒充原子锁；示例与实际任务分离；没有平台依赖或生产认证承诺；纯文档验证通过，业务编译 N/A；无未解决 P0/P1。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-004-review.md`。

## TASK-005 交付并验证可复现的检查工具

- PRD：REQ-001、REQ-002、REQ-008、REQ-009。
- DESIGN：DESIGN-001、DESIGN-002、DESIGN-006。
- Priority：P1。
- Status：DONE。
- Depends On：TASK-004。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权 Goal，串行认领。
- Target Module：本地文档/提交验证。
- Target Files：`scripts/check_docs.py` [NEW]、`tests/test_check_docs.py` [NEW]、`docs/EXAMPLE.md`；`AGENTS.md`、`docs/DESIGN.md`、`CONTRIBUTING.md`、`docs/ADOPTION.md`、`docs/reviews/README.md`（同步实际兼容版本与验证字段约定）。
- Target API / Method：`scripts/check_docs.py` 的 CLI，参数与退出码严格遵循 DESIGN-006。
- Implementation：先写失败场景与边界测试，再实现工作区/暂存区/示例检查；使用标准库与 Git CLI，不安装依赖；断链、统计、依赖、DONE 证据、暂存陈旧/个人文件必须能报错；运行单测、工作区检查与示例红/绿灯；真实结果写审核，不执行历史临时脚本。创建 `docs/reviews/TASK-005-review.md` [NEW]。
- Acceptance Criteria：工具边界单测及示例实际通过；工具可在干净导出目录运行且能检测暂存旧内容；本任务验证工具能力，完整发布内容在 TASK-003 同步入口后由 TASK-006 做工作区/暂存/导出验收，不以测试夹具通过替代发布验收；工具不更改源文件或索引；无未解决 P0/P1。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-005-review.md`。

## TASK-006 完成发布卫生与精确提交准备

- PRD：REQ-002、REQ-003、REQ-007、REQ-008、REQ-009。
- DESIGN：DESIGN-002、DESIGN-003、DESIGN-005、DESIGN-006。
- Priority：P1。
- Status：DONE。
- Depends On：TASK-003、TASK-004、TASK-005。
- Owner：Codex。
- Claimed At：2026-10-24，负责人授权 Goal，串行认领。
- Target Module：发布与审核。
- Target Files：`.gitignore`、`docs/TASKS.md`、`docs/reviews/initialization-review.md`；`docs/reviews/TASK-006-review.md` [NEW]；Git 索引（只调整明确发布文件的暂存范围）。
- Target API / Method：`python3 scripts/check_docs.py --staged`。
- Implementation：检查发布清单与内容；保留初始化历史，追加当前阶段说明与既有问题处置；把 `.idea/` 从暂存区移除但保留磁盘文件；精确暂存最终发布资产；在索引快照上复验链接、依赖、许可与工作区一致性，另做干净导出验证；记录结论与推荐提交信息，不执行 commit/push。
- Acceptance Criteria：无本地配置进入索引；发布文件均为最终版本；单测、文档、示例、暂存与导出检查真实通过；审核无未解决 P0/P1；原有 IDE/工具配置保留；工作区无未暂存的发布修改；没有新提交或推送。
- Completed By：Codex（Owner 登记，作者自检范围）。
- Completed At：2026-10-24。
- Review：`docs/reviews/TASK-006-review.md`。

## 状态与验收维护

**CONFIRMED / REQ-001～REQ-003**：状态变化立即同步任务明细和看板。开始前读最新文件；局部更新，不以缓存全量覆盖。DONE 必须同时满足 PRD、DESIGN、任务验收、真实必要验证、审核完成、P0/P1 清零。文档任务使用适用的文档验证，不声称业务测试通过；历史 DONE 不删除，通过新任务追踪变化。

审核者先在任务主审核文件登记 PASS 或 PASS_WITH_CONDITIONS；任务 Owner 或负责人随后核对全部完成门槛，方可登记 DONE，并在任务明细记录登记者、日期和审核报告链接。条件仍阻碍验收时保持 REVIEW。P0/P1 的 REJECTED 只有在保留反证且获另一审核者确认或负责人认可后，才可用于解除熔断；不能由修复者单方面驳回后登记完成。
