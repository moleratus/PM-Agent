lines = open(r'D:\AIProjects\MetaGPT\metagpt\roles\di\engineer2.py', encoding='utf-8').readlines()
for i, l in enumerate(lines, 1):
    if 'pwd' in l:
        print(f'{i}: {l}', end='')
