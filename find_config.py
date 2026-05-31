import os

search_dirs = [
    r'D:\AIProjects\MetaGPT',
    os.path.expanduser('~') + r'\.metagpt',
    os.path.expanduser('~'),
]

print("=== 搜索 config2.yaml ===")
for d in search_dirs:
    if not os.path.exists(d):
        continue
    for root, dirs, files in os.walk(d):
        # 跳过 .git 和 node_modules
        dirs[:] = [x for x in dirs if x not in ('.git', 'node_modules', '__pycache__')]
        for f in files:
            if 'config' in f.lower() and f.endswith('.yaml'):
                path = os.path.join(root, f)
                print(f"\n找到: {path}")
                try:
                    content = open(path, encoding='utf-8').read()
                    if 'deepseek' in content.lower() or 'api_key' in content.lower():
                        print(">>> 内容预览:")
                        for line in content.splitlines():
                            if any(k in line.lower() for k in ['model', 'api_key', 'base_url', 'max_token', 'api_type']):
                                print(f"    {line}")
                except:
                    pass
