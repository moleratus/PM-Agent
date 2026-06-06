

# 介绍与演示：

PM-Agent是面向产品经理(Product Manager)的端到端AI协作工具，基于 MetaGPT框架构建，支持Windows系统本地运行。PM-Agent 将 AI 能力深度融入产品设计和产品迭代工作流——输入一句需求，自动完成需求分析、PRD 输出和可交互原型生成。内置 Kano 模型、用户旅程图、5 Whys、Jobs Scoping 等专业 PM 方法论作为可插拔 Skills，支持用户上传自定义Skills，根据场景智能调用。支持 0-1 新产品设计与 1-N 迭代优化双模式，一键驱动多角色 Agent 协作，让产品经理从想法到验证原型的时间大幅压缩。PM-Agent旨在将产品经理的隐性方法论知识显性化、系统化，并根据工作场景自动调用，让 AI 真正模拟 PM 的工作流。

# 核心特性

- **端到端 Pipeline**：输入需求 → 需求分析 → PRD 文档 → HTML 原型，一键式全自动完成
- **可插拔 Skills**：基于 txt 文件的 PM 方法论库，支持用户自定义skill 并配置调用条件
- **场景化调用**：区分 `new_product` / `iteration` 场景，可根据用户指令，关键词匹配，场景判断加载对应 skills
- **双模式支持**：`new_product` 模式从零到一设计产品，`--update-mode` 模式优化迭代
- **本地运行**：支持Windows系统部署，完全本地化，数据不上云

# 如何安装

推荐使用python3.9-3.11版本。在Windows环境部署时，推荐使用Anaconda虚拟环境

首先创建虚拟环境：
```bash
conda create -n metagpt python=3.9
```

激活进入虚拟环境：
```bash
conda activate metagpt
```

将项目代码git到本地：
```bash
git clone https://github.com/moleratus/PM-Agent.git
```

初始化配置：
```bash
# Check https://docs.deepwisdom.ai/main/en/guide/get_started/configuration.html for more details
metagpt --init-config  # it will create ~/.metagpt/config2.yaml, just modify it to your needs
```

设置api key，位置位于刚刚创建的配置文件 `~/.metagpt/config2.yaml `：
```bash
llm:
  api_type: "openai"  # or azure / ollama / groq etc. Check LLMType for more options
  model: "gpt-4-turbo"  # or gpt-3.5-turbo
  base_url: "https://api.openai.com/v1"  # or forward url / other llm url
  api_key: "YOUR_API_KEY"
```

# 如何使用

进入项目目录
```bash
cd PM-Agent-main
```

## 产品设计模式

默认状态下为产品设计模式，该模式下只会调用和需求分析，0-1产品设计等相关的skills。可使用以下命令进行测试，agent将输出prd和网页原型：
```bash
metagpt "设计一个todo app，用于记录用户待办日程，输出prd，完成html原型设计" --n-round 30
```

## 产品迭代模式

在命令中手动添加`--update-mode`切换为迭代模式，该模式下会调用功能边界界定，需求分析等产品迭代相关skills，需提供prd和网页原型的本地路径。可使用以下命令进行测试：
```bash
metagpt "给待办事项添加优先级记录功能，修改prd和html原型" --update-mode --prd-path "..." --prototype-path "..." --n-round 30
```
也可只提供现有问题，由agent自行分析根本原因并做出修改：
```bash
metagpt "待办事项统计页面点击率很低，分析原因并修改prd和html原型" --update-mode --prd-path "..." --prototype-path "..." --n-round 30
```

## Skills调用逻辑以及配置方法

### 调用逻辑

skills采用分层调用的方式，更准确灵活。具体来说，用户指名，关键词匹配，是否默认加载都会影响skill是否被调用，其中用户指名的优先级最高，默认加载其次。只有当用户没有明确提到要调用，且不是默认调用时，才会进入关键词匹配阶段。需注意，skills被严格限制只能在对应的场景中调用。例如在产品迭代模式下，无法调用产品0-1设计相关skills，用户指名无效。

目前初始只提供6个基础skills，用户可根据需要自行添加

new_product：jobs_scoping（功能边界定义），kano_model（卡诺模型），pov（产品pov称述），user_journey_map（用户旅程地图）

iteration：five_why（五why模型）， iceberg_model（冰山模型），jobs_scoping，pov


### 配置方法
自定义skills时，需严格按照格式进行定义，保存为txt格式文件。配置路径为：
`\PM-Agent-main\metagpt\skills\ProductManager`

skills内容分成元数据和描述两部分。

---
name: skills的名称

description: 简单介绍skills用途

roles: [Product Manager]

scenarios: [new_product, iteration]（该skills在设计产品时调用还是优化迭代时调用，还是都调用）

triggers: [pain point, problem,...]（用于匹配到此skills的关键词）

default: false/true （当无关键词匹配和用户指定时，是否默认调用该skills）

---
#POV Statement (MANDATORY in UPDATE MODE)
When you see [UPDATE MODE], apply this skill first to frame the problem before analysis.

##Steps（skills定义）
1. **Identify the user** — Concrete user type based on research.
2. **State the need** — Verb phrase expressing user goal, not a solution.
3. **Articulate the insight** — The non-obvious "because" clause.
4. **Validate** — Narrow enough to act on, broad enough for multiple solutions.
5. **Iterate** — Write 2-3 variations, select the best one.

##Output Format（限制输出）
Primary POV: "[User] needs [need] because [insight]."
2-3 alternative phrasings + rationale for selecting the final version.

# 相关链接

感谢MetaGPT对开源社区的贡献：https://github.com/FoundationAgents/MetaGPT

