# 介绍：

PM-Agent是面向产品经理(Product Manager)的端到端AI协作工具，基于 MetaGPT框架构建，支持Windows系统本地运行。PM-Agent 将 AI 能力深度融入产品设计和产品迭代工作流——输入一句需求，自动完成需求分析、PRD 输出和可交互原型生成。内置 Kano 模型、用户旅程图、5 Whys、Jobs Scoping 等专业 PM 方法论作为可插拔 Skills，支持用户上传自定义Skills，根据场景智能调用。支持 0-1 新产品设计与 1-N 迭代优化双模式，一键驱动多角色 Agent 协作，让产品经理从想法到验证原型的时间大幅压缩。

# 核心特性

- **端到端 Pipeline**：输入需求 → 需求分析 → PRD 文档 → HTML 原型，一键式全自动完成
- **可插拔 Skills**：基于 txt 文件的 PM 方法论库，支持用户自定义skill 并配置调用条件
- **场景化调用**：区分 `new_product` / `iteration` 场景，按需加载对应 skills
- **双模式支持**：`new_product` 模式从零到一设计产品，`--update-mode` 模式优化迭代
- **本地运行**：支持Windows系统部署，完全本地化，数据不上云

# 如何安装

推荐使用python3.9-3.11版本。在Windows环境部署时，推荐使用Anaconda虚拟环境。

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

# 如何使用
