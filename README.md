# PubMed 科研情报分析平台（笔试 Demo）

> 沿长科技 · 成都中心 笔试作品

## 一、项目简介

本 Demo 是一个**独立开发**的网页应用：用户输入研究关键词 → 实时调用 **NCBI PubMed E-utilities API** 检索近 5 年文献 → 自动完成统计、可视化、影响力排序与中文综述生成。

## 二、核心功能对照（笔试要求）

| 笔试要求 | 实现情况 |
|---|---|
| 用户输入关键词 → PubMed 检索 | ✅ 输入框 + 实时调用 PubMed esearch/esummary/efetch |
| ① 统计研究数量、年份、分区、影响因子 | ✅ 统计卡片 + 逐年发文量柱状图 + **JCR 分区（Q1–Q4）** 环形图 + **中科院大类分区（1–4 区）** 环形图 + 影响因子均值 / 最高值 + 匹配覆盖率 |
| ② 生成词云、总结研究方向、可视化图表 | ✅ 关键词词云（wordcloud2.js）+ 研究方向排行 + 图表（Chart.js） |
| ③ 影响力排序，近 5 年影响因子前 100 文献 | ✅ 按影响因子降序的 TOP 100 表格，每行同时给出 JCR 分区与中科院分区；支持筛选与排序，标题可跳转 PubMed |
| ④ 基于摘要生成 500 字左右中文综述（分点呈现） | ✅ 自动生成分段中文综述报告 |
| 现场演示及功能测试 | ✅ 附演示视频（artifacts/demo_video.webm / .mp4） |

## 三、竞品调研

> 调研时间：2026 年 10 月；方式：基于各产品官方站点与公开评测资料的功能梳理。

### 3.1 调研目的

题面要求「提前进行竞品调研，了解相似产品大致情况」。本 Demo 的产品链路是「关键词 → PubMed 检索 → 统计分析 → 可视化 → 中文综述」，因此调研聚焦三类相似产品：

1. **PubMed 阅读增强型**：在 PubMed 页面上叠加期刊指标，帮助快速筛选文献；
2. **文献关系发现型**：用引文网络推荐和发现相关文献；
3. **文献计量分析型**：做共现网络、知识图谱等专业计量分析。

### 3.2 竞品概览

| 竞品 | 形态 | 核心能力 | 主要局限 |
|---|---|---|---|
| **Scholarscope** | 浏览器插件（PubMed 增强） | 在 PubMed 结果列表直接显示影响因子、JCR/中科院分区、被引次数；支持按 IF/分区筛选与排序；文献标记与简单管理；支持导出 EndNote/Zotero | 依赖浏览器插件、需逐个页面浏览；不做整体统计图表、词云、TOP100 榜单和综述；IF/分区数据更新有延迟（官方说明最长约 4 个月） |
| **ResearchRabbit** | 在线工具（文献发现） | 以若干「种子文献」为起点，沿引文网络推荐相关/后续工作；支持集合长期跟踪、作者追踪、时间线视图与协作；免费 | 定位是"发现层"而非分析层；不产出统计图表、分区统计、IF 排行和中文综述 |
| **Connected Papers** | 在线工具（文献图谱） | 输入一篇种子文献，几分钟内生成相似文献关系图，适合快速了解陌生领域 | 单次快照式图谱；不做关键词批量统计，不涉及 IF/分区排名与综述生成 |
| **Litmaps** | 在线工具（引文轨迹） | 以时间轴展示引文演进，识别奠基性/修正性论文，适合长期追踪前沿 | 侧重追踪新进展，缺少影响因子维度的量化排行与中文综述 |
| **Elicit** | AI 研究助手 | 语义检索 + 从多篇文献中抽取结构化数据（列式表格），辅助系统综述 | 面向英文问答、输出形态不固定；免费额度有限；AI 抽取结果仍需人工核对 |
| **Scite** | 引用语境分析 | 展示引用是「支持 / 反驳 / 仅提及」，用于验证结论可靠性、排查争议文献 | 不做影响因子统计、词云与综述 |
| **Semantic Scholar** | AI 学术搜索 | 覆盖广、提供 TLDR 摘要与相关推荐 | 非 PubMed 专用；不提供 JCR 分区/IF 排行，无中文结构化综述 |
| **CiteSpace / VOSviewer** | 桌面软件（文献计量） | 关键词共现网络、知识图谱、突现词检测等专业计量分析 | 需本地安装与参数调优，学习成本高；不直连 PubMed 在线检索，无综述输出 |
| **Web of Science / Dimensions** | 商业学术数据库 | 权威引文数据与高阶计量分析 | 需机构订阅，成本与门槛高；不适合零成本快速检索场景 |

### 3.3 与本题四项核心功能的对照

| 能力维度 | 本 Demo | Scholarscope | ResearchRabbit | Elicit | CiteSpace |
|---|---|---|---|---|---|
| 关键词 → PubMed 实时检索 | ✅ | ✅（插件内） | ➖（以种子文献起步） | ✅（自有文献库） | ➖（需先导入数据） |
| 发文量 / 年份 / 分区 / 影响因子统计 | ✅ | ➖（列表内逐条显示） | ❌ | ❌ | ➖（需自行配置） |
| 词云 + 研究方向总结 | ✅ | ❌ | ❌ | ➖（要点式总结） | ✅（关键词共现） |
| 近 5 年影响因子 TOP100 排行 | ✅ | ➖（可手动排序） | ❌ | ❌ | ❌ |
| 约 500 字中文综述（分点呈现） | ✅ | ❌ | ❌ | ❌（英文问答式） | ❌ |
| 使用门槛 | 本地一键运行 | 安装插件 | 注册账号 | 注册账号 | 本地安装 + 调参 |

### 3.4 调研中涉及的关键概念

| 概念 | 说明 |
|---|---|
| **影响因子（IF）** | Clarivate 在 JCR 中发布的期刊年度指标：某期刊前两年论文在统计年的平均被引次数。它衡量**期刊**整体影响力，不等同于单篇论文质量。PubMed、Google Scholar 等均不直接提供该值，需依赖 JCR 数据。 |
| **JCR 分区（Q1–Q4）** | Clarivate 把**同一学科**内的期刊按 IF 降序排列后四等分：前 25% 为 Q1，依次 Q2、Q3、Q4。一门期刊可属于多个学科，各学科分区可能不同，通常取其中最好的一个。 |
| **中科院分区（1–4 区）** | 中国科学院文献情报中心发布的分区表（"升级版"）。按大类学科划分，前 5% 为 1 区，6%–20% 为 2 区，21%–50% 为 3 区，其余为 4 区；另标记是否 Top 期刊。它不与 JCR 分区等价，国内投稿、考核多以中科院分区为准，因此本 Demo **两套分区同时呈现**。 |
| **词云** | 对文献标题与摘要分词、去停用词后，按词频或短语频次映射字号大小，用于快速识别高频主题词。 |
| **文献综述** | 对某一领域研究进展的系统性归纳。本题要求基于检索到的摘要生成约 500 字、分点呈现的中文综述。 |
| **近 5 年时间窗** | 以当前年份为终点向前回溯 5 个自然年（含当年），本题用于限定统计与影响力排序的文献范围。 |

### 3.5 调研结论与本 Demo 定位

- 现有产品可归为三类：**阅读增强型**（Scholarscope、Scite、Semantic Scholar）、**关系发现型**（ResearchRabbit、Connected Papers、Litmaps）、**计量分析型**（CiteSpace、VOSviewer、Web of Science）。
- 三者各解决一个环节，但**很少有产品把「检索 → 统计可视化 → 影响力排行 → 中文综述」串成一条闭环**，其中中文输出的结构化领域简报尤其稀缺。
- 因此本 Demo 的定位是：**面向中文科研人员的「一站式 PubMed 情报简报」**——输入一个关键词，几分钟内得到一份可直接阅读的领域概览（统计 + 图表 + 榜单 + 综述）。
- **已知差距（后续可补）**：暂不提供引文网络/关系图谱（对应 ResearchRabbit、Connected Papers 的能力）；影响因子与分区采用内置参考数据集，尚未接入机构授权的 JCR 数据；综述由「结构化模板 + 统计量注入 + 摘要文本挖掘」生成，尚未接入大模型润色与引用溯源。

## 四、技术架构

```
用户浏览器 (Vue 3 + Chart.js + wordcloud2.js)
        │  fetch /search?keyword=...
        ▼
Flask 后端 (app.py)
        │  requests
        ▼
NCBI PubMed E-utilities (esearch / esummary / efetch)
```

- **前端**：Vue 3 + Vite 组件化开发，按业务分组组织组件；Chart.js 做统计图，wordcloud2.js 做词云。构建产物已生成在 `static/dist/`，因此运行时无需安装 Node。
- **后端**：Python Flask，已拆分为配置 / 路由 / 服务三层，负责调用 PubMed API、解析 XML/JSON、文本挖掘、生成综述。
- **数据源**：NCBI PubMed（真实实时数据）提供文献本身；Clarivate JCR 与中科院分区表提供影响因子与分区（详见 4.1）。

### 4.1 影响因子与分区的数据来源

PubMed 的 E-utilities 接口**不返回影响因子和分区**，因此这两项必须由外部数据集补齐。本 Demo 采用两份公开发布的数据表，并由 `tools/build_journal_metrics.py` 离线合并成 `data/journal_metrics.json`：

| 数据项 | 来源 | 版本 | 覆盖规模 |
|---|---|---|---|
| 影响因子、JCR 分区（Q1–Q4）、学科内的 IF 排名 | Clarivate **Journal Citation Reports** | **JCR 2025** | 22,643 本期刊 |
| 中科院大类分区（1–4 区）、Top 标记、各小类分区 | 中国科学院文献情报中心**分区表升级版** | **2025** | 21,772 本期刊 |
| 合并后的指标库 | `data/journal_metrics.json` | — | 23,029 本期刊 / 40,248 个 ISSN 号 |

> 原始数据 CSV 存于 `data/source/`，可运行 `scripts/download_journal_data.bat`（或 `.sh`）重新获取，再执行 `tools/build_journal_metrics.py` 重建索引。JCR 属商业数据库，本项目使用公开发布的整理版；生产环境应替换为机构授权的 JCR 接口。

### 4.2 期刊匹配策略（为什么不用"期刊名模糊匹配"）

早期版本用「期刊名子串包含」匹配（如 `nature`、`cell`、`science` 作为子串去比对其它刊名），导致
`Life sciences` 被赋成 56.9、`Journal of cellular and molecular medicine` 被赋成 64.5 这类明显错误。
现版本**取消了全部包含匹配**，改为按优先级查表的**精确匹配**：

| 优先级 | 规则 | 命中率贡献 | 误判风险 |
|---|---|---|---|
| 1 | **ISSN / EISSN 精确匹配**（PubMed esummary 每篇都返回） | 绝大部分 | 无 |
| 2 | 期刊全称归一化后精确相等 | 兜底 | 无 |
| 3 | 去掉副标题（`Molecular therapy : the journal of ...`） | 兜底 | 无 |
| 4 | 去掉括号限定符（`Science (New York, N.Y.)`） | 兜底 | 无 |
| 5 | 去掉前导 `the` / 方括号前缀（`The Biochemical journal`） | 兜底 | 无 |

**匹配不上就如实标记「未收录」**，既不臆造数值，也不参与影响因子均值与 TOP100 排序。

以 `CAR-T therapy`（200 篇）实测对比：

| 指标 | 修复前 | 修复后 |
|---|---|---|
| 影响因子命中率 | 61.5%（123/200） | **89.5%（179/200）** |
| 中科院分区命中率 | — | **90.5%（181/200）** |
| JCR 分区取值 | 仅 Q1 + 未知 | **Q1 133 / Q2 23 / Q3 18 / Q4 5 / 未收录 21** |
| 中科院分区取值 | 未实现 | **1 区 88 / 2 区 35 / 3 区 28 / 4 区 30 / 未收录 19** |
| 平均影响因子 | 40.16（虚高） | **20.49**（与该领域实际水平相符） |
| `Life sciences` | 56.9（错） | **6.4 / Q1 / 中科院 3 区** |
| `Journal of cellular and molecular medicine` | 64.5（错） | **4.7 / Q2 / 中科院 3 区** |

剩余约 10% 未收录的主要是日文、俄文等非 SCIE 收录的小刊，属于数据源本身的覆盖范围，界面上已明确区分。


## 五、目录结构（分层架构）

```
pubmed_demo/
├── app.py                     # 入口：创建 Flask 应用、注册蓝图
├── config.py                  # 全局配置（路径 / API / 参数 / 缓存）
├── routes/                    # ── 路由层 ──
│   └── api.py                 # 首页 + /search 接口
├── services/                  # ── 服务层 ──
│   ├── http_utils.py          # 带重试的 HTTP 请求 + 磁盘缓存
│   ├── storage.py             # 本地数据文件读取
│   ├── pubmed.py              # PubMed E-utilities 客户端
│   ├── metadata.py            # 年份解析、文献类型归一化
│   ├── metrics.py             # 影响因子 / JCR 分区 / 中科院分区（ISSN 精确查表）
│   ├── nlp.py                 # 分词、词云、研究方向归纳
│   ├── report.py              # 中文综述生成
│   └── analysis.py            # 分析流水线（编排以上模块）
├── tools/                     # ── 数据构建 ──
│   └── build_journal_metrics.py  # JCR + 中科院分区表 -> journal_metrics.json
├── scripts/
│   ├── download_journal_data.bat / .sh  # 下载原始 JCR / 中科院分区表 CSV
│   └── setup_windows / setup_linux      # 环境初始化
├── start.bat                  # Windows 一键启动（自动装依赖 + 校验指标库）
├── frontend/                  # Vue 3 + Vite 前端工程源码
│   ├── src/
│   │   ├── App.vue            # 根组件
│   │   ├── components/        # 按业务分组：layout / search / charts / analysis / common
│   │   ├── composables/       # 可复用逻辑：检索状态机、图表生命周期等
│   │   ├── api/pubmed.js      # 后端接口封装
│   │   └── styles/main.css    # 全局样式
│   ├── package.json
│   └── vite.config.js
├── static/dist/               # Vue 3 构建产物（Flask 直接托管，运行时无需 Node）
├── data/
│   ├── journal_metrics.json   # 期刊影响因子 / 分区参考数据
│   └── stopwords.txt          # 停用词表
└── artifacts/                 # 交付物：视频、截图
```

### 模块职责一览

| 模块 | 职责 |
|---|---|
| `config.py` | 所有可调参数集中管理（批量大小、限流间隔、检索条数、缓存 TTL） |
| `services/pubmed.py` | 封装 esearch / esummary / efetch，只负责取数据 |
| `services/metrics.py` | 期刊影响因子与分区查询，数据源可替换 |
| `services/nlp.py` | 文本挖掘：分词、词云、研究方向 |
| `services/report.py` | 综述模板 + 真实统计量注入，纯函数、易测试 |
| `services/analysis.py` | 编排流水线，输出前端可渲染的统一结构 |
| `routes/api.py` | 只做参数校验、缓存读写与响应 |

**设计原则**：路由层不碰业务、服务层不碰 HTTP；数据流向单向（route → analysis → 各 service），便于单独替换或测试任一环节。

## 六、本地运行

`static/dist/` 已包含构建产物，因此**无需安装 Node**即可直接运行：

```bash
cd D:/pubmed_demo
pip install -r requirements.txt
python app.py
# 浏览器打开 http://127.0.0.1:5000
```

Windows 用户也可以直接双击 `start.bat`；若该文件不在目录中，按上面的命令手动启动即可。

### 6.1 关于 PubMed 账户与 API Key

本 Demo **无需注册 PubMed、无需任何 API Key** 即可运行：后端直接调用 NCBI 公开的 E-utilities 接口，按公共速率（约 3 次/秒）抓取数据。代码中已内置请求间隔与磁盘缓存，现场演示不会触发限流。

**如需修改前端源码**，需进入 `frontend/` 安装依赖并构建：

```bash
cd D:/pubmed_demo/frontend
npm install
npm run build       # 产物自动输出到 ../static/dist
```

> 注：在受限沙箱环境中构建时，`esbuild`/`rollup` 的原生二进制可能因子进程策略无法自动安装，需手动补装：`npm install @esbuild/win32-x64 @rollup/rollup-win32-x64-msvc`。

## 七、交付物位置

笔试额外要求的材料均位于 `D:\pubmed_demo\artifacts\`：

- **演示视频**：`demo_video.webm` / `demo_video.mp4`
- **数据来源截图**：`screenshot_source_pubmed.png`（PubMed 官网）、`screenshot_source_api.png`（E-utilities API）
- **笔试 demo 整个页面截图**：`screenshot_demo_full.png`
- 其他关键页面截图：`screenshot_01_home.png`、`screenshot_02_stats.png`、`screenshot_03_top100.png`、`screenshot_04_report.png`、`screenshot_05_second_query.png`

详见 `artifacts/README.md`。

## 八、前端组件化设计

本次 Vue 3 重构按业务领域把页面拆成可复用组件，便于后续扩展：

| 分组 | 组件 | 职责 |
|---|---|---|
| **layout** | `SiteHeader` / `SectionNav` / `PageFooter` / `BackToTop` | 页面骨架、分区锚点导航、回到顶部 |
| **search** | `SearchBar` / `QuickTags` / `SearchSection` | 关键词输入、快捷示例 |
| **common** | `PanelSection` / `StatCard` / `LoadingState` / `ErrorAlert` / `EmptyState` | 通用卡片、加载状态、错误/空结果 |
| **charts** | `YearChart` / `QuartileChart` / `JournalChart` / `WordCloudChart` / `ChartCard` | Chart.js / wordcloud2.js 图表封装，自动销毁实例 |
| **analysis** | `ResultHeader` / `StatGrid` / `StatsSection` / `TopicsSection` / `TopPapersSection` / `ReviewSection` | 四大功能模块：统计、词云/方向、TOP100 表格、综述 |

通过 `composables/useSearch.js` 把检索流程收敛为单一状态机，`composables/useChart.js` 统一处理 Chart 实例生命周期，避免内存泄漏。

## 九、设计思考（结合 AI 完成）

1. **数据真实性优先**：所有文献均为 PubMed 实时检索结果，不做假数据；受 API 速率限制，默认抓取近 5 年 200 篇做深度分析（可调 `retmax`）。
2. **前端工程化**：使用 Vue 3 + Vite 将原本 300 行的原生 JS 拆分为组件与可复用逻辑，提升可读性和可维护性；构建产物托管在 Flask 中，保证一键运行。
3. **影响因子来源**：JCR 属商业数据库，Demo 阶段采用可替换的本地参考表 + 归一化匹配；生产环境应接入机构授权的 JCR/LetPub API。
4. **综述生成策略**：采用「结构化模板 + 真实统计量注入」的可解释方案，避免大模型幻觉，确保数字与图表一致；后续可替换为 LLM 生成 + 引用溯源。
5. **性能与限流**：批量请求 PubMed 并 sleep 控制速率，避免被封；增加磁盘缓存保证 demo 现场流畅；前端一次性渲染，表格超 100 行采用滚动容器。
6. **可扩展性**：前后端分离，后端 REST 接口便于接入更多数据源（如 Europe PMC、Web of Science）；Vue 组件结构便于继续新增分析维度。
