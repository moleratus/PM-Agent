import os

workspace = r'D:\AIProjects\MetaGPT\workspace'
if not os.path.exists(workspace):
    print(f"workspace 目录不存在: {workspace}")
else:
    for root, dirs, files in os.walk(workspace):
        level = root.replace(workspace, '').count(os.sep)
        indent = '  ' * level
        print(f'{indent}{os.path.basename(root)}/')
        for f in files:
            fpath = os.path.join(root, f)
            size = os.path.getsize(fpath)
            print(f'{indent}  {f} ({size} bytes)')
