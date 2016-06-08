import _initpath
import re
import os
import pyradox.hoi4.tech
import pyradox.hoi4.unit
import pyradox.format
import pyradox.struct
import pyradox.wiki
import pyradox.yml

def computeCountryTagAndName(filename):
    m = re.match('.*([A-Z]{3})\s*-\s*(.*)\.txt$', filename)
    return m.group(1), m.group(2)

countries = {}
total = pyradox.struct.Tree()

for filename, country in pyradox.txt.parseDir(os.path.join(pyradox.config.basedirs['HoI4'], 'history', 'countries')):
    tag, name = computeCountryTagAndName(filename)
    country['tag'] = tag
    rulingParty = country['set_politics']['ruling_party']
    country['name'] = pyradox.yml.getLocalization('%s_%s' % (tag, rulingParty), ['countries'], game = 'HoI4')
    countries[tag] = country

states = pyradox.txt.parseMerge(os.path.join(pyradox.config.basedirs['HoI4'], 'history', 'states'))
stateCategories = pyradox.txt.parseMerge(os.path.join(pyradox.config.basedirs['HoI4'], 'common', 'state_category'), verbose=False)

for state in states.values():
    history = state['history']
    tag = history['owner']
    country = countries[tag]

    country['states'] = (country['states'] or 0) + 1
    total['states'] = (total['states'] or 0) + 1
    
    stateCategoryKey = state['state_category']
    buildingSlots = stateCategories[stateCategoryKey]['local_building_slots'] or 0
    country['building_slots'] = (country['building_slots'] or 0) + buildingSlots
    total['building_slots'] = (total['building_slots'] or 0) + buildingSlots
    
    if 'manpower' in state:
        country['manpower'] = (country['manpower'] or 0) + state['manpower']
        total['manpower'] = (total['manpower'] or 0) + state['manpower']
    
    if 'resources' in state:
        for resource, quantity in state['resources'].items():
            country[resource] = (country[resource] or 0) + quantity
            total[resource] = (total[resource] or 0) + quantity

    for victoryPoints in history.findAll('victory_points'):
        for i in range(1, len(victoryPoints), 2):
            country['victory_points'] = (country['victory_points'] or 0) + victoryPoints[i]
            total['victory_points'] = (total['victory_points'] or 0) + victoryPoints[i]

    if 'buildings' in history:
        for building, quantity in history['buildings'].items():
            if isinstance(building, str):
                country[building] = (country[building] or 0) + quantity
                total[building] = (total[building] or 0) + quantity
            else:
                # province buildings
                for building, quantity in quantity.items():
                    country[building] = (country[building] or 0) + quantity
                    total[building] = (total[building] or 0) + quantity

def sumKeysFunction(*sumKeys):
    def resultFunction(k, v):
        return '%d' % sum((v[sumKey] or 0) for sumKey in sumKeys)
    return resultFunction

columns = (
    ('Country', '{{flag|%(name)s}}'),
    ('Tag', '%(tag)s'),
    ('Ruling party', lambda k, v: v['set_politics']['ruling_party'].title()),
    ('States', '%(states)d'),
    ('Research slots', lambda k, v: '%d' % (v['set_research_slots'] or 2)),
    ('Population (M)', lambda k, v: '%0.2f' % ((v['manpower'] or 0) / 1e6) ),
    ('Victory points', '%(victory_points)d'),
    ('Building slots', '%(building_slots)d'),
    ('Military factories', '%(arms_factory)d'),
    ('Naval dockyards', '%(dockyard)d'),
    ('Civilian factories', '%(industrial_complex)d'),
    ('Total factories', sumKeysFunction('arms_factory', 'dockyard', 'industrial_complex')),
    ('Oil', '%(oil)d'),
    ('Aluminium', '%(aluminium)d'),
    ('Rubber', '%(rubber)d'),
    ('Tungsten', '%(tungsten)d'),
    ('Steel', '%(steel)d'),
    ('Chromium', '%(chromium)d'),
    ('Total resources', sumKeysFunction('oil', 'aluminium', 'rubber', 'tungsten', 'steel', 'chromium')),
    ('Air base levels', '%(air_base)d'),
    ('Naval base levels', '%(naval_base)d'),
    )

out = open("out/countries.txt", "w")
out.write(pyradox.wiki.makeWikitable(countries, columns, sortFunction = lambda item: item[1]['name']))
out.close()

print(total)
