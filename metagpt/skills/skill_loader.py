# metagpt/skills/skill_loader.py

from pathlib import Path
from metagpt.logs import logger

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class SkillLoader:
    """
    最小可用版本：按角色加载 skill 文件。
    设计上预留 forced / auto / default 三层选择接口，
    当前只实现 default（角色匹配即加载）。
    """

    def __init__(self):
        self.skill_root = Path(__file__).parent
        self._cache: dict = {}
        self._load_all()

    def _load_all(self):
        """只扫描指定的角色目录，不扫描 MetaGPT 内置 skills"""
        # 只扫描这些子目录，忽略其他所有目录
        allowed_dirs = ["shared", "ProductManager", "Architect", "Engineer", "DataAnalyst"]

        for dir_name in allowed_dirs:
            skill_dir = self.skill_root / dir_name
            if not skill_dir.exists():
                continue
            for txt_file in skill_dir.glob("*.txt"):  # 只扫一层，不递归
                meta, content = self._parse(txt_file)
                name = meta.get("name", txt_file.stem)
                self._cache[name] = {"meta": meta, "content": content}

    def _parse(self, path: Path):
        raw = path.read_text(encoding="utf-8")
        if raw.startswith("---") and HAS_YAML:
            parts = raw.split("---", 2)
            if len(parts) >= 3:
                meta = yaml.safe_load(parts[1]) or {}
                return meta, parts[2].strip()
        return {"name": path.stem}, raw.strip()



    def select_skills(
            self,
            role_profile: str,
            idea: str = "",
            forced_skills: list = None,
            scenario: str = "new_product",
    ) -> str:
        """
        两层筛选：
        Layer 1: 场景匹配（new_product / iteration / diagnosis）
        Layer 2: 场景内关键词匹配或默认加载
        """
        selected = {}

        for name, skill in self._cache.items():
            meta = skill["meta"]
            roles = meta.get("roles", [])

            # 角色不匹配跳过
            role_normalized = role_profile.replace(" ", "").lower()
            if not any(r.replace(" ", "").lower() == role_normalized for r in roles) \
                    and "shared" not in roles:
                continue

            # Layer 1: 强制指定（最高优先级，跳过场景过滤）
            if forced_skills and name in forced_skills:
                selected[name] = (skill["content"], "forced")
                logger.info(f"✅ Skill '{name}' selected for '{role_profile}' (forced)")
                continue

            # Layer 1: 场景过滤
            skill_scenarios = meta.get("scenarios", ["new_product"])
            if scenario not in skill_scenarios:
                continue  # 不属于当前场景，跳过

            # Layer 2a: 场景内默认加载
            if meta.get("default", False):
                selected[name] = (skill["content"], "default")
                logger.info(f"✅ Skill '{name}' selected for '{role_profile}' "
                            f"(scenario={scenario}, source=default)")
                continue

            # Layer 2b: 场景内关键词匹配
            triggers = meta.get("triggers", [])
            if idea and any(t.lower() in idea.lower() for t in triggers):
                selected[name] = (skill["content"], "auto")
                logger.info(f"✅ Skill '{name}' selected for '{role_profile}' "
                            f"(scenario={scenario}, source=keyword_match)")

        if not selected:
            return ""

        result = "\n\n## Your Available Skills\n"
        result += "Apply the relevant skill when performing your tasks:\n"
        for name, (content, source) in selected.items():
            result += f"\n### [{source}] Skill: {name}\n{content}\n"

        return result


# 全局单例，避免重复加载
SKILL_LOADER = SkillLoader()