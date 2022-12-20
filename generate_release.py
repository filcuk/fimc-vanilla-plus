import os
import json
import toml
import click
from consolemenu import *
from consolemenu.items import *
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
    return output, success1

def main():
    menu = ConsoleMenu("Title", "Subtitle")
    
    # MenuItem is the base class for all items, it doesn't do anything when selected
    menu_item = MenuItem("Menu Item")

    # A FunctionItem runs a Python function when selected
    function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

    # A CommandItem runs a console command
    command_item = CommandItem("Run a console command",  "touch hello.txt")

    # A SelectionMenu constructs a menu from a list of strings
    selection_menu = SelectionMenu(["item1", "item2", "item3"])

    # A SubmenuItem lets you add a menu (the selection_menu above, for example)
    # as a submenu of another menu
    submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

    # Once we're done creating them, we just add the items to the menu
    menu.append_item(menu_item)
    menu.append_item(function_item)
    menu.append_item(command_item)
    menu.append_item(submenu_item)

    # Finally, we call show to show the menu and allow the user to interact
    menu.show()
    

# TODO: Check for packwiz updates (currently not possible)

main()

exit()

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
    readme.write('Mod updates:  \n```')
    readme.write(updates)
    readme.write('```')
    
    readme.close

# Submit git

# Create release