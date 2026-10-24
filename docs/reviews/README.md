# 统一审核规范与内嵌模板

**CONFIRMED / REQ-002、DESIGN-002**：任务只维护一个主报告 `TASK-xxx-review.md`，不为每个 Agent 另建报告。初始化自检用 `initialization-review.md`，它不是任何后续 Task 的完成证明。

## 审核步骤

1. 首位审核者创建主报告，注明审核者、日期、范围、Git 基线/变更范围、关联 REQ/DESIGN/Task 与实际验证。
2. 后续审核者先读取最新报告和绑定事实源，独立检查代码与测试，再追加 Confirm/Rebut、新问题与结论；不得删除历史意见或覆盖记录。写前协调唯一写入者。
3. 每个问题有永久唯一 ID（如 TASK-001-I001）。状态 OPEN → FIXED → VERIFIED；有充分反证可 REJECTED。P0/P1 的 REJECTED 还须另一审核者确认或负责人认可，记录认可者、日期与依据，提出驳回者不能自行放行。状态可精准更新，但必须追加保留处置和复核历史。
4. P0（BLOCKER）、P1（HIGH）、P2（MEDIUM）、P3（LOW）必须有具体证据。Evidence 使用真实文件行号、实际命令及输出；未执行项写明未执行，N/A 写理由。
5. 任何 P0/P1 未达 VERIFIED 或满足第 3 条的有效 REJECTED，强制 FAIL，禁止 DONE 或合并；FIXED 仍为未解决。
6. PASS 表示满足范围内全部验收且无阻断；PASS_WITH_CONDITIONS 只能用于无未解决 P0/P1 的剩余条件，有未满足的任务验收时保持 REVIEW，不能 DONE。非阻断遗留项记录负责人认可的处置/后续任务。
7. 不同结论按观点 + 代码证据 + 实际测试证据 + DESIGN 契约交叉验证；无足够依据则 TODO_CONFIRM，待负责人裁决，保留原结论及争议过程。不能依模型声望决定。
8. 审核者先登记 PASS 或 PASS_WITH_CONDITIONS；Owner 或负责人再核对验收并在 TASKS 登记 DONE，记录登记者、日期和审核报告链接。修复者自检不能冒充另一审核者的复核，外部结论仅由该审核者或负责人根据证据更新。

## 最小模板（复制到所选任务的唯一主报告）

```markdown
# TASK-xxx Review

- Task / PRD / DESIGN：填写实际 ID
- Reviewer：填写真实参与者，并注明独立审核或作者自检
- Date：填写实际日期
- 审核范围 / Git 基线与变更：填写可复核内容
- 事实等级：CONFIRMED / INFERRED / TODO_CONFIRM（各发现分别标注）
- 验证记录：命令、真实输出摘要、结果、未运行或 N/A 的原因
- Conclusion：PASS / PASS_WITH_CONDITIONS / FAIL（实际审核后只保留一个枚举）
- Conditions Resolved：仅在条件全部满足时填 yes，否则不能据条件通过登记 DONE

## 发现

| Issue ID | Severity | Reviewer（人或 Agent） | Description | Evidence | Impact | Suggestion | Status | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

无发现时明确写“本次范围内未发现问题”，不要生成虚构问题行。

## 追加历史

- 日期 / 审核者 / Issue ID / Confirm 或 Rebut / 依据 / 状态变化 / 结论。

## 完成门禁

- PRD、DESIGN 与 Task 验收逐项核对。
- 必要验证真实通过；无未解决 P0/P1；审核完成。
- 条件与遗留项、负责人认可的处置、是否允许 DONE。
- 审核结论登记者/日期；DONE 登记者/日期/报告链接（尚不满足时留空并说明）。
```

**CONFIRMED（维护规则）**：本模板不是实际审核报告，不能凭模板里的枚举或空表宣称审核完成。审核结论只覆盖实际检查范围，不等于生产可用认证。

Reviewer 与原指令的 Agent 字段同义，可填人或实际参与的 Agent。用户转交外部复核时注明来源；模型身份未经确认不得自行署名。保留原问题编号与结论，追加修订响应及真实复验结果，不把提交修复等同外部审核已通过。

本仓库工具读取 `Conclusion`、`Reviewer`、`Date` 和任务的 `Completed By`、`Completed At`、`Review` 字段。若 P0/P1 以 REJECTED 解除门禁，报告还须记录 `Rejection Approved By` 与 `Rejection Evidence`，人工核实认可者与证据是否充分；有字段不等于自动批准。外部采用项目可保留自己的等价字段，但要相应适配检查器。
