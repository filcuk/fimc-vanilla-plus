import os
import json
import toml
import subprocess

# Get current properties from pack.toml
with open('pack.toml', 'r') as f:
    c = toml.load(f)
    name = c['name']
    author = c['author']
    version = c['version']

print('Modpack: ' + name)
print('Author:  ' + author)
print('Version: ' + version)
print('Leave blank to keep current value.')
print('\n')

# Let user update
name = input('Modpack: ') or name
author = input('Author:  ') or author
version = input('Version: ') or version

os.system('')
print('Modpack: ' + name)
print('Author:  ' + author)
print('Version: ' + version)

# Update Better Compatibility Checker bcc.json
print('Updating bcc.json...')
with open('config/bcc.json', 'r') as f:
    c = json.load(f)
    c['modpackName'] = name
    c['modpackVersion'] = version
    f.close()
    
with open('config/bcc.json', 'w') as f:
    json.dump(c, f, indent=2)
    f.close()

# Update packwiz pack.toml
print('Updating pack.toml...')
with open('pack.toml', 'r') as f:
    c = toml.load(f)
    c['name'] = name
    c['author'] = author
    c['version'] = version
    f.close()

with open('pack.toml', 'w') as f:
    toml.dump(c, f)
    f.close()

# Update mods
#! Not working
# subprocess.run(["packwiz.exe", "packwiz update -a -y"])

# Create exports
# print('Generating CurseForge pack...')

# print('Generating Modrinth pack...')

# Submit git

# Create release