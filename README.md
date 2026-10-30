# ResumeCraft Skill

面向 Codex 与兼容 Agent Skills 宿主的本地简历制作工具，Python 3.11+。
根据有来源的真实经历，生成五种风格的 A4 HTML、可复制文本的 PDF、预览和质量报告。
事实提取/润色由宿主 Agent 审核，脚本负责可复用的数据约束、匹配、排版和验证。

## 安装与快速开始（Windows PowerShell）

从项目文件夹执行；Python 可用 `py -3.12` 或实际安装的 `python`。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe scripts/build_resume.py examples/sample_profile.json --no-photo --output outputs
.\.venv\Scripts\python.exe -m pytest -q
```

macOS/Linux 使用 `python3 -m venv .venv` 与 `.venv/bin/python`；Linux 可能需
`python -m playwright install --with-deps chromium`。安装依赖需要网络，基础处理本地运行。
若仅调用 scripts，也可 `pip install -r requirements.txt`；测试另装 pytest。
可选 OCR：本地安装 Tesseract 与 chi_sim/eng 数据，图片另装 pytesseract。

## 在 Codex 安装与自然语言使用

按官方本地发现规则，将整个文件夹复制至 `$HOME/.agents/skills/resume-craft-skill`：

```powershell
$skillSource = Join-Path ([Environment]::GetFolderPath('Desktop')) 'resume-craft-skill'
$skillParent = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Force -Path $skillParent | Out-Null
Copy-Item -LiteralPath $skillSource -Destination (Join-Path $skillParent 'resume-craft-skill') -Recurse
```

目标已存在时先检查旧内容，避免嵌套/覆盖。安装副本后，在副本里按上节安装依赖。
Codex 通常自动发现变更，未出现时重启。也可项目级放在 `.agents/skills/` 下。
自然语言：`请使用 $resume-craft-skill，根据我上传的经历制作极简商务风 A4 单页简历，输出 HTML 和 PDF。`
后续可要求“换成学术风”“按网络运营 JD 排序”“缩小照片”“列出模板”；复用事实库与配置，生成新版本。
不要把真实资料保存到 Skill 安装目录或开源仓库；选择独立私有工作目录。

官方来源（核对日期 2026-10-28）：
[Codex 本地 Skill 发现与创建](https://learn.chatgpt.com/docs/build-skills)、
[Agent Skills 规范](https://agentskills.io/specification)。

## CLI 与输入输出

```powershell
python scripts/extract_profile.py old-resume.pdf --output user_data/intake.json
python scripts/parse_job.py examples/sample_job.txt --output user_data/job_description.json
python scripts/match_job.py examples/sample_profile.json user_data/job_description.json --output user_data/match.json
python scripts/build_resume.py examples/sample_profile.json --job user_data/job_description.json --template Resume003-ModernTech --no-photo --output outputs
python -m resume_craft.cli templates
```

TXT/MD/DOCX/PDF 提取器保留全文来源，自动识别带标签的姓名/联系方式；其余经历需 Agent
按 `references/profile-schema.md` 结构化。不能把提取器输出直接当作完整个人事实库。
图片/扫描件需要宿主视觉或可选 OCR。所有示例均为 DEMO 合成资料，example.invalid 不是真实邮箱。
`schemas/` 提供机器 schema。`examples/resume_config.json` 展示模块、语言、字号、照片控制。

每次 build 产生递增目录：resume.html、resume.pdf、preview.png、quality_report.json、
profile_snapshot.json、resume_config.json，可选 job_description.json / matching_report.json。
保留 master_profile.json；报告记录省略条目。失败退出码为 2；不得把失败 PDF 当作成功交付。
示例输出在 `examples/sample_output/`，图和 PDF 只使用合成数据；模板预览也是合成数据。

## 架构与真实性

`SKILL.md` 只放 Agent 路由和关键约束；`references/` 渐进披露；`scripts/` 独立 CLI；
`src/resume_craft/` 分模型、解析、匹配、模板、渲染、验证、文件工具。
`assets/templates/` 为唯一模板源，构建 wheel 时复制入包资源，安装后仍可渲染。
不依赖任何宿主专有 API，不要求 API key，不自动创建仓库或推送。

Claim 保存 raw/text/source_id/confirmed。脚本检查引用、元数据、数字日期、重复 ID、逆序日期；
无法自动确认的改写阻止生成，交用户审核。确认不是事实真实性证明，状态/否定/团队归属仍需语义复核。
JD 采用可解释词表匹配和稳定排序，未支持技能进入报告，绝不写入个人事实库。
非技术要求、语义匹配与英文润色由 Agent 执行，脚本不会声称保证 ATS 或录用。

## 模板、字体与质量

现有五套原创模板，包括三套单栏、一套左侧信息栏双栏和一套日期轴，完整名称见下方模板列表。
添加 Word 模板见 `references/template-guide.md`：解析结构样式、保留 DOCX、编写 HTML/CSS
适配、检查后启用。复杂表格/文本框/浮动元素必须人工适配，**没有无损转换承诺**。
默认本地 CJK 字体；跨机器建议指定有合法授权的开源中文字体，见 assets/fonts/README.md。

自动检查页数/A4、文本提取一致性、边界/裁切/重叠、照片、字号/行距、空模块、字体状态等；
最多 3 次修复，先压间距再减低优先级条目，保持可读字号。不能容纳时明确失败。
美观、字形和阅读顺序需查看截图及实际 PDF。详见 references/formatting-rules.md。

## WorkBuddy 兼容范围

采用标准 SKILL.md 结构。可在支持上传技能包的客户端导入，仍需本地 Python/Chromium。
本项目未进行 WorkBuddy 实机验证。可用 package_project.py --workbuddy 生成带额外元数据的包。

## 隐私、FAQ、贡献与发布

基础脚本不上传个人数据；宿主云端模型边界见 references/privacy-and-truthfulness.md。
日志隐藏输入值，照片移除 EXIF；版本快照也属隐私。删除数据请核对独立私有目录后删除。
无照片可正常继续；缺 Chromium/字体、扫描件、损坏文档和过量内容见 troubleshooting.md。
运行 `python -m pytest -q` 查看测试结果。不是所有平台和 OCR 能力都经过验证。

贡献前运行 pytest、检查五套模板实际 PDF，提交合成复现，不提交真实简历。
发布前复核第三方模板/字体许可，扫描源码与 ZIP 是否混入私人资料，在干净环境复测、
补充 macOS/Linux/WorkBuddy 实机验证、检查依赖更新与许可证，再由维护者自行创建 GitHub 仓库。
`scripts/package_project.py` 使用允许清单打包，不删除源文件，排除缓存/虚拟环境/用户资料。
允许清单不能检测混入源码的私人资料，发布前仍要人工检查。
项目原创代码/模板 MIT；第三方资源各遵其许可，详情见 THIRD_PARTY_NOTICES.md。


## Current public template library / 当前公开模板库

- `Resume001-MinimalBusiness`
- `Resume002-AcademicResearch`
- `Resume003-ModernTech`
- `Resume004-SidebarProfile`
- `Resume005-TimelineLedger`

Five original MIT designs. The two new designs are sidebar and date-axis layouts.
See [new-designs.md](references/new-designs.md) and [template-naming.md](references/template-naming.md).
Next template: Resume006-NewEnglishName. Third-party Word-derived templates are not included.
