import re
with open(r'c:\Users\kevin\Downloads\Projet code\YGO ULTIME DECK\diff_3_1.txt', 'r', encoding='utf-16le') as f:
    content = f.read()
files = re.findall(r'^diff --git a/(.*?) b/', content, re.MULTILINE)
with open(r'c:\Users\kevin\Downloads\Projet code\YGO ULTIME DECK\diff_files.txt', 'w', encoding='utf-8') as f:
    for file in files:
        f.write(file + '\n')
