import os
import json
import toml
import click
from subprocess import call, check_output, CalledProcessError, STDOUT

# https://stackoverflow.com/a/47144897/1657229
def system_call(command):
    """ 
    params:
        command: list of strings, ex. `["ls", "-l"]`
    returns: output, success
    """
    try:
        output = check_output(command, stderr=STDOUT).decode()
        success = True 
    except CalledProcessError as e:
        output = e.output.decode()
        success = False
    return output, success

# TODO: Check for packwiz updates (currently not possible)

# Get current properties from pack.toml
with open('pack.toml', 'r') as f:
    c = toml.load(f)
    name = c['name']
    author = c['author']
    version = c['version']

print('Modpack: ' + name)
print('Author:  ' + author)
print('Version: ' + version)
print('\n')

# Let user update values
print('Leave blank to keep current value.')
name = input('Modpack: ') or name
author = input('Author:  ') or author
version = input('Version: ') or version
print('\n')

# Show updated values
os.system('')   # Clear CLI (doesn't work)
print('Modpack: ' + name)
print('Author:  ' + author)
print('Version: ' + version)
print('\n')

# Update Better Compatibility Checker
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

# Update mods and record for changelog
if click.confirm('Apply mod updates? (True)', default=True):
    updates, success = system_call(['packwiz.exe', 'update', '-a', '-y'])

# Create exports
if click.confirm('Export CurseForge pack? (True)', default=True):
    print('Generating CurseForge pack...')
    call(['packwiz.exe', 'curseforge', 'export'])

if click.confirm('Export Modrinth pack? (False)', default=False):
    print('Generating Modrinth pack...')
    call(['packwiz.exe', 'modrinth', 'export'])

# Update README.md
try:
    print(updates)
except:
    updates = 'none'


with open('README.md', 'wt', encoding='UTF-8') as readme, open('README.md-template', 'r') as template:
    # Write template first
    for line in template:
        readme.write(line)
    template.close
    
    # Write current version details
    readme.write('Version: ' + version + '  \n')
    readme.write('Updates:  \n```')
    readme.write(updates)
    readme.write('```')
    
    readme.close

# Submit git

# Create release