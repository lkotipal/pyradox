import hoi4
import re
import os
import hoi4


import pyradox


def list_commander_traits(k, v):
    if 'traits' not in v: return ''
    result = ''
    for trait in v.find_all('traits'):
        if not isinstance(trait, str): continue
        result += '{{iconify|' + pyradox.yml.get_localisation(trait, game = 'HoI4') + '}}, '
    return result[:-2]

commander_type_keys = {
    'create_field_marshal' : 'Field Marshal',
    'create_corps_commander' : 'General',
    'create_navy_leader' : 'Admiral',
    }

columns = (
    ('Country', '{{flag|%(country)s}}'),
    ('Name', '%(name)s'),
    ('Type', lambda k, v: commander_type_keys[k]),
    ('Skill', '%(skill)d'),
    ('Traits', list_commander_traits),
    )

commanders = pyradox.Tree()

for tag, country in hoi4.load.get_countries().items():
    for commander_type_key in commander_type_keys.keys():
        for leader in country.find_all(commander_type_key):
            leader['country'] = country['name']
            commanders.append(commander_type_key, leader)

out = open("out/military_commanders.txt", "w", encoding="utf-8")
out.write(pyradox.table.make_table(commanders, 'wiki', columns, sort_function = lambda key, value: (value['country'], key, value['name'])))
out.close()
