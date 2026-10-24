# Example：从需求到审核的最小闭环

这是教学示例，不是 agent-matrix 的业务功能。EX- 前缀与真实 REQ/DESIGN/TASK 命名空间分离；示例状态不计入实际任务看板。下面的审核历史是明确标注的示意，不冒充真实第三方审核。代码与测试则可以通过随仓库交付的命令真实运行。

## EX-REQ-001 百分比输入边界

- 事实等级：CONFIRMED（仅在本教学场景中约定）。
- 用户与目标：调用者希望把整数百分比限制在 0～100，得到确定的结果。
- 范围：低于 0 返回 0，高于 100 返回 100，区间内保持原值；布尔值和非整数拒绝。
- 验收：覆盖上下界、区间内、超界及非法类型；不访问数据库、网络或文件。

## EX-DESIGN-001 确定实现契约

- 绑定：EX-REQ-001；Complexity：SIMPLE；状态：APPROVED（示例设定，不是项目负责人对实际设计的批准）。
- 示例目标文件：`percent.py` [NEW，采用者的示例工程，不在本仓库创建]。
- 方法：`normalize_percent(value: int) -> int`；仅接受实际 int 类型，bool 不接受；非法类型抛 `TypeError`；无事务或副作用。
- 数据库、HTTP、DTO：N/A；不为简单函数引入服务分层。
- 验证：先写下方测试，再运行有缺陷版本证明测试能失败，最后实现正确版本并执行同一测试。

## EX-TASK-001 实现边界归一化

- PRD：EX-REQ-001；DESIGN：EX-DESIGN-001；Priority：P1；Depends On：无。
- Target Module：教学示例；Target Files：示例 `percent.py` [NEW] 与 `test_percent.py` [NEW]，代码在本文交付。
- Target API / Method：`normalize_percent(value: int) -> int`。
- Owner：示例执行者；Status：DONE（教学流程设定，不计入实际任务）。
- Implementation：先定义 14 个边界/类型案例 → 确认红灯版本被检测 → 实现修正版本 → 同一套测试绿灯 → 进入 REVIEW → 复核后登记完成。
- Acceptance Criteria：函数契约与测试匹配，14 个案例通过，没有未解决 P0/P1；教学审核不等于外部独立审核。

## 可执行代码与测试

三个代码块只在内存中执行；命令不会写入采用者工程。

<!-- example:tests -->
```python
def run_example_tests(function):
    count = 0
    for value, expected in [(-9, 0), (-1, 0), (0, 0), (1, 1), (50, 50),
                            (99, 99), (100, 100), (101, 100), (1000, 100)]:
        actual = function(value)
        if actual != expected:
            raise AssertionError(f"{value}: expected {expected}, got {actual}")
        count += 1
    for invalid in [True, False, 2.5, "50", None]:
        try:
            function(invalid)
        except TypeError:
            count += 1
        else:
            raise AssertionError(f"expected TypeError for {invalid!r}")
    return count
```

<!-- example:red -->
```python
def normalize_percent(value: int) -> int:
    if type(value) is not int:
        raise TypeError("value must be an integer")
    return min(value, 100)
```

<!-- example:green -->
```python
def normalize_percent(value: int) -> int:
    if type(value) is not int:
        raise TypeError("value must be an integer")
    return max(0, min(value, 100))
```

在本仓库根目录执行：

```sh
python3 scripts/check_docs.py --example-red
python3 scripts/check_docs.py --example
```

红灯命令只有在测试实际发现缺陷时退出 0；如果错误版本意外通过，退出 1。绿灯命令要求全部 14 个案例通过。执行结果以命令输出为准，实际交付验证由 [TASK-005](TASKS.md#task-005-交付并验证可复现的检查工具)承担并写入其主审核记录，不依赖原机器的临时文件。

## 示例审核记录（示意，不是真实第三方意见）

| Issue ID | Severity | Reviewer | Description | Evidence | Impact | Suggestion | Status | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EX-I001 | P1 | 示例审核者 | 红灯实现没有处理负数下界 | `normalize_percent(-9)` 返回 -9，契约要求 0 | 违反验收 | 增加下界限制 | VERIFIED（教学设定） | 修正代码后以同一套测试复验；真实可执行结果由上述命令产生 |

示意历史：OPEN/P1 → FAIL（不能 DONE）→ FIXED（仍不能放行）→ 复验后 VERIFIED → PASS → 示例 Owner 登记 DONE。真实项目必须记录实际审核者、日期、命令、结果和报告链接，不能复制这些示例状态作为证据。

## 需求或设计变化时

- 若需要支持小数：先修改需求并重新定义类型、舍入与边界契约，再追加增量任务；不直接把 int 换成 float。
- 若测试发现设计不可行：暂停实现，记录原因、最小修正与影响，再更新设计/任务并取得必要确认。
- 若两个 Agent 同时要改函数：暂停写入，由协调者明确 Owner；共享任务记录串行合入，不能靠覆盖文件“抢到”任务。
