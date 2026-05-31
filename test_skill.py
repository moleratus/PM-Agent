from metagpt.skills.skill_loader import SKILL_LOADER 
result = SKILL_LOADER.select_skills('Product Manager', scenario='iteration') 
print(result[:300] if result else 'EMPTY') 
