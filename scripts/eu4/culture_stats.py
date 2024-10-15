import _initpath
import os
import re
import collections



import pyradox




sources = ['EU4', 'text', 'nw2', 'res_publica', "aow"]

def localized(s):
    return pyradox.yml.get_localisation(s, 'EU4') or pyradox.format.human_title(s)


culture_groups = {}

culture_tree = pyradox.txt.parse_file(os.path.join(pyradox.get_game_directory('EU4'), 'common', 'cultures', 'anb_cultures.txt'))

for group_name, group_data in culture_tree.items():
    for culture in group_data:
        culture_groups[culture] = group_name

culture_data = {}
culture_group_data = {}

for filename, data in pyradox.txt.parse_dir(os.path.join(pyradox.get_game_directory('EU4'), 'history', 'provinces'), verbose=False):
    data = data.at_time(pyradox.Time('1444.11.11'))
    if 'culture' not in data:
        if 'base_tax' in data:
            print('No culture defined in %s.' % filename)
        continue
    if 'owner' not in data:
        continue
    culture = data['culture']
    culture_group = culture_groups[culture]

    culture = localized(culture)
    if culture not in culture_data:
        culture_data[culture] = ['', 0, 0, 0, 0, 0]
    culture_data[culture][0] = localized(culture_group)
    culture_group = localized(culture_group)

    if culture_group not in culture_group_data:
        culture_group_data[culture_group] = [0, 0, 0, 0, 0]

    culture_data[culture][1] += 1
    culture_group_data[culture_group][0] += 1

    if 'base_tax' in data:
        culture_data[culture][3] += data['base_tax']
        culture_group_data[culture_group][2] += data['base_tax']
        culture_data[culture][2] += data['base_tax']
        culture_group_data[culture_group][1] += data['base_tax']
    if 'base_production' in data:
        culture_data[culture][4] += data['base_production']
        culture_group_data[culture_group][3] += data['base_production']
        culture_data[culture][2] += data['base_production']
        culture_group_data[culture_group][1] += data['base_production']
    if 'base_manpower' in data:
        culture_data[culture][5] += data['base_manpower']
        culture_group_data[culture_group][4] += data['base_manpower']
        culture_data[culture][2] += data['base_manpower']
        culture_group_data[culture_group][1] += data['base_manpower']

result = ''

result += '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
result += '! Culture group !! Province count !! Development !! Base tax !! Base production !! Base manpower\n'

for culture_group, stats in sorted(culture_group_data.items()):
    result += '|-\n'
    result += '| %s || %d || %d || %d || %d || %d \n' % tuple([culture_group] + stats)

result += '|}\n'

print(result)

result = ''

result += '{|class = "wikitable sortable mw-collapsible mw-collapsed"\n'
result += '! Culture !! Culture group !! Province count !! Development !! Base tax !! Base production !! Base manpower\n'

for culture, stats in sorted(culture_data.items()):
    result += '|-\n'
    result += '| %s || %s || %d || %d || %d || %d || %d\n' % tuple([culture] + stats)

result += '|}\n'

print(result)
