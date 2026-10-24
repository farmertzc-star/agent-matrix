# Contributing

欢迎改善规范、模板、示例或验证工具。入口见 [中文 README](README.md)、[English README](README.en.md) 与 [AGENTS](AGENTS.md)。贡献内容使用仓库 [MIT License](LICENSE)；不要提交你无权公开的业务资料或个人配置。

## 变更流程

1. 提出问题及可验证结果；维护者确认范围后，沿 PRD → DESIGN → TASKS 传导。纯文字小改也说明修改位置和验证，不需要新增平行体系。
2. 按实际任务认领和依赖执行，已有 DONE 保留，新变更分配新 ID。默认按优先级串行；并行工作必须协调共享文件与唯一写入者。
3. 修订规范时同步采用模板和示例；事实源不复制进 README。真实验证与示意流程分开，不伪造独立审查或测试。
4. 审核使用任务唯一主报告，多轮追加；未解决 P0/P1 强制 FAIL。小规模文档/工具变更可如实记录作者自检；若项目要求独立审查，必须获得真实独立审核者结论，不能换署名。

## 本地检查

Python 3.9+ 与 Git CLI 即可，无第三方依赖，无网络请求、数据库或云服务。

```sh
python3 -m unittest discover -s tests -v
python3 scripts/check_docs.py
python3 scripts/check_docs.py --example-red
python3 scripts/check_docs.py --example
git diff --check
```

`--example-red` 运行有意缺陷版本：示例断言检测到失败时命令才成功；`--example` 验证修正版本。两者不写文件，不代表对采用者业务做了测试。

## 准备提交

先查看 `git status --short` 和 `git diff`，用明确路径暂存，不默认 `git add .`。本地 `.idea/`、`.vscode/`、`.DS_Store`、个人 `.claude/settings.local.json` 和环境文件不应发布；忽略规则不影响已暂存文件，移出索引时保留磁盘内容。

```sh
python3 scripts/check_docs.py --staged
git diff --cached --check
git diff --cached --stat
```

`--staged` 检查的是实际将提交的索引，发布文件若只修改工作区而未重新暂存会失败。必须先解决所有错误再提交；工具不会替你 commit、push 或更改索引。

建议提交信息：`docs: publish reusable multi-agent engineering workflow`。工具逻辑变化可使用 `fix: ...` 或 `test: ...`，以实际变更为准，不把提交格式当作质量证明。

## 验证器边界与干净导出

检查器覆盖本仓库 Markdown 的本地链接/锚点、追踪 ID、任务字段/统计/依赖、DONE 审核证据、MIT 许可与提交卫生，并运行标记的 Python 示例。它不检查远程网页可用性、不证明人工协调具备原子互斥，也不替代对需求、安全或生产环境的审核。

发布前可把索引中的文件导出到临时目录，在不含 `.git`、IDE、个人全局配置或历史临时脚本的环境中运行工作区检查、单元测试和示例。工作区检查无需 `.git`；只有 `--staged` 模式要求 Git 仓库。不要把初始化历史报告中的旧临时命令当作安装步骤。
