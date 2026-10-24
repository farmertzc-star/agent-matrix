# agent-matrix 技术设计与共享契约

更新日期：2026-10-24。设计状态与事实等级独立：CONFIRMED 描述依据可信，不代表方案已获 APPROVED。

## 当前交付设计

**CONFIRMED（负责人新指令，2026-10-24）**：当前产品是技术栈中立的方法包，范围与许可证见 DEC-001、DEC-002。本仓库不建立 HTTP API、Service、DTO、数据库、缓存或部署服务；数据库变更：无。Python 3.9+ 仅用于可选的仓库验证器和示例，不成为采用者业务项目的技术栈要求。验证器只使用标准库及 Git CLI，不安装业务依赖。

当前路径与新增资产契约见 DESIGN-005、DESIGN-006；下节保留初始化扫描历史，不作为现在文件或能力仍缺失的断言。

## 初始化历史扫描（2026-10-24）

**CONFIRMED**：扫描基线为 `master`，提交 `fcca691`（Initial commit）。初始化前已跟踪文件仅 `README.md`、`README.en.md`、`.gitignore`；已跟踪文件无未提交或暂存变更；存在未跟踪 `.idea/`，必须保留。

**CONFIRMED**：已检查根目录可见与隐藏文件（排除 Git 内部文件，包含被忽略文件），并检查适用的祖先 AGENTS 规则。未发现既有 AGENTS、CLAUDE、CONTRIBUTING、PRD、DESIGN/SPEC、TASKS/TODO、原型、SQL、数据库设计、API、CI/CD 或其他治理目录，因此没有可增量复用的同类事实源。

| 扫描项 | 结论 | 事实等级 / 证据 |
| --- | --- | --- |
| 项目定位 | 多 Agent 工程与交付框架愿景；生产可用尚无实现证据 | CONFIRMED / 两份 README 第 4 行及占位章节 |
| 语言、框架、主要依赖、构建工具 | 无源码或依赖清单，无法确定 | TODO_CONFIRM / 先决条件为 PRD Q-001～Q-003 |
| Java 线索 | `.gitignore` 含 Java 产物规则，只是线索，不能确认 Java 选型 | INFERRED / `.gitignore` |
| 模块、包与分层 | 未发现业务模块、Controller、Service/Impl、Repository/Mapper/DAO、DTO/VO/Entity/DO、Converter、Validator、Exception、Config | CONFIRMED / 完整文件清单 |
| 数据库与中间件 | 未发现表、字段、索引、约束、迁移、实体映射或 Redis、MQ、搜索集成证据 | CONFIRMED / 完整文件清单；未来选型 TODO_CONFIRM |
| 公共能力 | 未发现返回对象、分页、登录权限、异常、ID、锁、存储、HTTP Client、日志、审计实现 | CONFIRMED / 无源码 |
| 第三方服务 | 未发现配置或调用实现 | CONFIRMED / 完整文件清单；未来是否需要 TODO_CONFIRM |
| 测试与 CI | 未发现单测、集成测试、Mock、Testcontainers、覆盖率或 CI 配置 | CONFIRMED / 完整文件清单 |
| 可用构建/测试命令 | 尚无；不得猜测 Maven、npm 等命令或声称业务测试通过 | CONFIRMED / 无构建与测试入口 |

## 设计索引

共 6 项：APPROVED 0、REVIEW 6、DRAFT 0、BLOCKED 0。所有设计 ID 永久保留。REVIEW 不妨碍已授权的简单文档/本地工具任务；若将来涉及重大架构或共享运行时契约，仍须负责人批准。

| ID | 名称 | PRD | 复杂度 | 事实等级 | 状态 |
| --- | --- | --- | --- | --- | --- |
| DESIGN-001 | 事实源与执行闭环 | REQ-001 | SIMPLE | CONFIRMED（负责人已要求该机制） | REVIEW |
| DESIGN-002 | 审核与交付门禁 | REQ-002 | SIMPLE | CONFIRMED（负责人已要求该机制） | REVIEW |
| DESIGN-003 | 变更、上下文与单写入 | REQ-003 | SIMPLE | CONFIRMED（负责人已要求该机制） | REVIEW |
| DESIGN-004 | 产品范围与实现契约的决策入口 | REQ-004、REQ-005、REQ-006、REQ-009 | SIMPLE | CONFIRMED（范围及许可已确认；REQ-006 延后） | REVIEW |
| DESIGN-005 | 采用指南、模板与开源入口 | REQ-004、REQ-005、REQ-007、REQ-009 | SIMPLE | CONFIRMED（交付需求） | REVIEW |
| DESIGN-006 | 可复现验证与提交检查 | REQ-008、REQ-009 | SIMPLE | CONFIRMED（交付需求） | REVIEW |

REVIEW 表示本次文档方案供负责人审阅；不暗示已有独立或多 Agent 审核。涉及公共接口、共享 DTO、数据库、跨模块或重大架构的方案，只有负责人明确确认后方可 APPROVED。

## DESIGN-001 事实源与执行闭环

**CONFIRMED / REQ-001**：采用 PRD → DESIGN → TASKS → CODE & TEST → REVIEW → DONE。没有代码时按文档验收，不虚构构建结果。

- 模块：仅治理文档；不新增运行时模块。
- 本设计涉及的初始化新增文件：`docs/PRD.md` [NEW]、`docs/DESIGN.md` [NEW]、`docs/TASKS.md` [NEW]；不是本次全部交付文件清单。
- 需求 ID 为 REQ-xxx、设计 ID 为 DESIGN-xxx、任务 ID 为 TASK-xxx、决策 ID 为 DEC-xxx，发布后不重用，不因重排更名。DEC-xxx 在对应设计的决策记录区登记，产品范围决策见 DESIGN-004。
- 每个任务同时引用需求与设计；TASKS 是唯一任务进度源，顶部看板与明细同步。
- 任务状态：TODO → IN_PROGRESS → REVIEW → DONE；缺少输入或条件时进入 BLOCKED，记录原因；解除后回到合适状态；审核失败返回 IN_PROGRESS 或 BLOCKED，不能直接 DONE。
- 设计状态：DRAFT → REVIEW → APPROVED；存在决策或契约阻塞时为 BLOCKED，解决后重入 DRAFT/REVIEW。已批准设计发生实质变化必须重新审核，不能沿用原批准。
- 实现准入：具体需求已确认、关联设计可执行且达到相应批准门槛、依赖 DONE、目标文件与契约明确。决策类文档任务可用于解除 BLOCKED 设计，不受“必须先有实现契约”约束，但不能借此写代码。
- 验证：检查唯一事实源、ID 关联、依赖无环、统计与任务明细、完成证据是否一致。

## DESIGN-002 审核与交付门禁

**CONFIRMED / REQ-002**：复用单个任务审核记录，不为每种 Agent 建立副本。

- 文件：`docs/reviews/README.md` [NEW] 定义规范并内嵌模板；本次 `docs/reviews/initialization-review.md` [NEW] 只记录初始化自检；后续任务按 `docs/reviews/TASK-xxx-review.md` [NEW，xxx 替换为任务编号] 创建主报告。
- 发现字段：Issue ID、Severity、Reviewer（人或 Agent）、Description、Evidence、Impact、Suggestion、Status、Verification。Reviewer 与原指令的 Agent 字段同义，扩展为支持人类审核者，不另设一套字段。
- 问题状态：OPEN → FIXED → VERIFIED；有证据可 REJECTED。FIXED 仍需复核，不能作为 P0/P1 已解决。P0/P1 的 REJECTED 必须记录反证，并经另一审核者确认或负责人认可后才有效；提出驳回者不能自行放行。
- 结论：PASS / PASS_WITH_CONDITIONS / FAIL；任何 P0/P1 未达 VERIFIED 或上述有效 REJECTED，强制 FAIL，不得 DONE 或合并。
- DONE：需求、设计、任务验收全部满足，必要验证真实通过，审核完成且 P0/P1 清零。审核者先在主报告登记 PASS 或 PASS_WITH_CONDITIONS，随后任务 Owner 或负责人核对证据后才可在 TASKS 登记 DONE，记录登记者、日期和报告链接。PASS_WITH_CONDITIONS 的条件若仍阻碍验收，保持 REVIEW；非阻断遗留项须记录负责人认可的处置或后续任务。
- 验证：按真实文件或测试输出核实问题；后续审核者先独立核对再追加 Confirm/Rebut 和新发现，不删除历史。

## DESIGN-003 变更、上下文与单写入

**CONFIRMED / REQ-003**：根目录 `AGENTS.md` [NEW] 作为统一规则入口，无厂商专属副本。

- 按 AGENTS → 绑定的 REQ → 绑定的 DESIGN → TASK → Target Files 加载。可先查看任务索引定位 ID，再按此顺序精读；不全量读取无关历史或模块。
- 同一任务、文件、TASKS 只能有一个写入主体。开始前确认所有者；发现冲突暂停写入并协调。当前采用人工/会话协调，不引入锁服务。
- 修改 TASKS/审核记录前重读最新内容，精准局部更新或追加；若与读取基线不同，先协调，禁止旧缓存全量覆盖。
- 需求确认与变更先回写 PRD，再更新设计、任务及统计；历史 DONE 保留，新增增量任务；不可行设计须记录原因、最小方案、影响并重新确认。
- 仅在初始化模式下执行“只新增/增量维护治理文档，报告后停止”。负责人选择 Task 或新 Goal 后，按新授权范围继续；不能让一次性初始化约束阻断已授权的后续维护。任何阶段不擅自提交、迁移或部署。
- 验证：比较初始化开始与结束时的既有文件校验值和 Git 状态；报告持久保存基线与检查时间范围。区分本次写入与后续工具/用户变化，无法归属的变化如实记录，不凭 mtime 判断操作者。IDE 易变文件保留原始哈希，但与稳定文件分开复验，不能为使检查通过而重置基线或改回文件。

## DESIGN-004 产品范围与实现契约的决策入口

**CONFIRMED / REQ-004、REQ-005、REQ-009**：范围与 MIT 许可已经负责人明确，原阻塞解除。TASK-001 记录确认，TASK-002 形成方法包交付设计。REQ-006 仍为后续候选，不是当前发布依赖；不因采用者未来可能需要 HTTP 或数据库而阻塞本仓库文档发布。

采用者运行时契约盘点（与本仓库自身方法包交付区分）：

| 契约 | 当前事实（CONFIRMED） | 后续决策（TODO_CONFIRM） |
| --- | --- | --- |
| 模块及调用链 | 无业务模块与调用链 | 范围确认后定义边界、依赖、公共能力复用 |
| HTTP API | 无已实现 API；Method、URL、Controller#Method、请求/响应、权限、校验、错误处理均不适用 | 如确定需要 HTTP，再逐项给出唯一契约；否则记录不适用及原因 |
| Service | 无 Service；方法名、参数、返回值、异常、事务要求均不适用 | 按实际交付形态明确核心调用签名，不能硬套分层 |
| DTO | 无共享 DTO | 若需要，明确字段、类型、必填、校验、语义及唯一归属 |
| 数据库 | 无脚本、实体或映射；本次数据库变更：无 | 仅在需求要求持久化时设计；明确表字段、类型、默认、NULL、主键、索引、唯一约束、关系、兼容性、迁移与 DDL 草案，不执行 |
| 状态/并发/事务/缓存/MQ | 无现有实现 | 按范围明确幂等、重试、补偿、一致性、性能、兼容和恢复；不需要的项标不适用 |
| 文件、构建与验证 | 无代码与测试入口 | 已有路径经扫描验证；新增路径标 [NEW]；未定路径为 TBD；技术栈确认后给出真实命令与测试策略 |

决策交付方式：按 SIMPLE/NORMAL/COMPLEX 深度形成可执行设计，必要时分配后续 DESIGN ID。完成契约检查后才生成业务开发任务。不创建未经确定的目录或依赖。

### 决策记录

| ID | 日期 / 决策者 | 关联 | 决定、依据与影响 |
| --- | --- | --- | --- |
| DEC-001 | 2026-10-24 / 项目负责人 | Q-001、Q-002；REQ-004、REQ-005 | 负责人明确定位为开源规范、工作流、模板与协作机制，并授权完善到提交就绪。交付静态方法包及本地验证；采用人工协调，不建立自动编排服务或云部署平台。Q-001/Q-002 在本版范围内解决；Q-003 延后。 |
| DEC-002 | 2026-10-24 / 项目负责人 | REQ-009 | 明确选择 MIT，署名 agent-matrix contributors；新增标准 LICENSE，入口标明许可，不擅自 commit/push。 |

后续决策继续增量登记 DEC-xxx、关联 Q/REQ、日期、决策者、选项、决定、依据与影响。旧决定被替代时保留原记录和新决定链接。需求正文仍以 PRD 为准。

## DESIGN-005 采用指南、模板与开源入口

**CONFIRMED / REQ-004、REQ-005、REQ-007、REQ-009**：以现有文档体系为主，不新建 agents/skills/workflows/templates 平行体系。

- 修改真实文件：`README.md`、`README.en.md`、`AGENTS.md`、`.gitignore`、`docs/reviews/README.md`。保留历史审核记录，仅追加后续结论与历史范围说明。
- 新增文件：`docs/ADOPTION.md` [NEW] 集中接入步骤、初始化 Prompt 和 AGENTS/PRD/DESIGN/TASKS 模板；`docs/EXAMPLE.md` [NEW] 展示完整示例链；`CONTRIBUTING.md` [NEW] 定义贡献与提交检查；`LICENSE` [NEW] 使用 DEC-002 的 MIT 文本。
- 资产区分：根 AGENTS 和 docs/PRD、DESIGN、TASKS 是本仓库的有效实例；ADOPTION 是供复制的模板；EXAMPLE 使用 EX- 前缀，不混入实际看板。历史 review 不是安装步骤或当前进度源。
- 接入算法：检查 Git/本地规则 → 扫描已有事实源/代码 → 映射现有路径 → 增量补齐缺失字段和稳定 ID → 显式处理未确认事项 → 审核报告 → 初始化停止。禁止脚本批量覆盖项目文件。
- 初始化 Prompt 必须可独立复制：包含边界、扫描顺序、事实等级、PRD/设计/任务必填字段、共享契约检查、TDD、review 门禁、报告格式和停止条件。存在现成事实源时映射复用，不另建副本。
- SIMPLE：位置、修改方式、验证；NORMAL：模块/文件、接口与调用契约、数据影响、边界测试；COMPLEX：再补调用链、状态/并发/一致性、性能、风险、恢复与测试策略。按实际架构解释组件，不强制 Controller/Service 分层。
- 协作：Owner 认领须先由负责人/协调者串行分配，登记 Claimed At、共享文件和交接说明；两者同时认领时都暂停写入，由协调者确定一方。Owner 异常退出后只由负责人明确移交，不以等待超时自动夺权。移交前核对 Git 与未提交成果；TASKS/review 写入由一个协调写入者串行完成，其他 Agent 返回建议或补丁。不同工作树不能代替共享状态协调。
- Goal 默认按 P0 → P1 → P2 → P3 从已满足依赖的任务中每次选一个；负责人限定 P0/P1 时遵循限制。无可执行任务时报告实际阻塞，不永久跳过普通任务。
- 验证：中英文入口一致，模板可独立采用；示例明确区分真实验证和示意审核；本机路径只可作为被标记历史记录，不成为安装依赖；不承诺已在所有技术栈生产验证。

## DESIGN-006 可复现验证与提交检查

**CONFIRMED / REQ-008、REQ-009**：新增 `scripts/check_docs.py` [NEW] 和 `tests/test_check_docs.py` [NEW] 是轻量验证支持，不是 Agent 运行平台；无第三方依赖。

- 命令：`python3 scripts/check_docs.py` 检查工作区；`python3 scripts/check_docs.py --staged` 检查实际索引及其与工作区的一致性；`python3 -m unittest discover -s tests -v` 验证检查器的失败检测；`python3 scripts/check_docs.py --example` 执行随文提供的独立示例。
- 输入：从脚本位置确定仓库根目录；工作区模式检查发布资产，不遍历个人配置；staged 模式通过 `git ls-files`/`git show` 读取暂存内容，拒绝本地 IDE/工具配置、个人绝对路径、发布文件遗漏和工作区/索引不一致。命令不修改源文件或 Git 索引。
- 文档检查：UTF-8、末尾换行与空白、本地相对链接和锚点、实际 REQ/DESIGN/TASK 引用、事实/状态枚举、任务必填字段、看板统计、未知/循环依赖、DONE 的审核证据字段与审核结论。模板和 EX- 示例不计入实际看板。
- 许可与入口：必需发布文件存在、MIT 署名符合 DEC-002、README 无初始化占位内容、指南包含独立 Prompt 和模板。
- 历史记录：`docs/reviews/initialization-review.md` 仅作为标明范围的历史证据保留；允许其中旧的临时命令作为历史原文，不执行或要求其存在。新验证不读取原机器临时目录、Git 全局配置或个人文件。
- 示例：从 EXAMPLE 文档指定的 Python 代码块读取到内存，运行其测试；以 `--example-red` 运行有意缺陷版本，测试失败才表示红灯演示成功。示例不是业务功能，不写文件、不访问网络/数据库。
- 测试策略：正常文档、断链/错锚点、统计/依赖错误、缺少 DONE 证据、临时路径泄漏、暂存旧内容/本地配置等必须有失败测试；临时 Git 测试仓库只在系统临时目录生成。
- 成功退出 0，发现错误退出 1，输出具体文件与原因。检查只能证明静态一致性及示例行为，不能证明模型服从、真实多进程互斥或生产适用性。

## 生成任务前的一致性检查

**CONFIRMED（2026-10-24 扫描结果）**：

以下六项来自初始化指令，是检查维度，不是已确定的分层架构。TASK-002 须按确认后的技术栈映射到实际组件，必要时增补检查；不存在的层明确记 N/A 与理由，不为凑表新增 Controller、Service、Entity 等结构。

| 检查 | 结果 | 原因 |
| --- | --- | --- |
| Database ↔ Entity | N/A | 两者均不存在，无字段或约束可核对，不等同运行验证通过 |
| Controller ↔ DTO | N/A | 两者均不存在 |
| Controller ↔ Service | N/A | 两者均不存在 |
| Service ↔ Repository | N/A | 两者均不存在 |
| DESIGN ↔ Existing Code | 无已发现冲突 | 仅治理文档设计，不宣称存在业务实现 |
| Shared Contract | 未发现重复定义 | 无运行时共享契约；DESIGN-004 阻塞，不生成实现任务 |

**CONFIRMED（任务导出约束）**：当前导出方法包文档、示例与验证工具任务，不导出无需求依据的业务功能。未来契约变更须重做适用检查，存在冲突先修正设计，不把冲突下放给执行者。

## 风险与验证边界

- **CONFIRMED**：初始化时的“Production-ready”措辞缺少跨项目验证；发布入口应改为生产导向的方法包，明确现有验证范围，不声称已通过采用者的生产验收。
- **TODO_CONFIRM**：REQ-006 的未来云端产品化延后，不阻塞本版方法包。
- **CONFIRMED**：初始化历史没有业务测试；新交付验证器及示例必须真实运行。公开方法仍需由采用者结合实际权限、数据与部署风险确认。
- **INFERRED**：若直接按宣传语扩展平台，容易形成过度设计；通过先确认范围再定义契约控制风险。
