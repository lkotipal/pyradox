import pyradox
import re

def get_units(beta = False):
    game = 'HoI4_beta' if beta else 'HoI4'
    return pyradox.parse_merge('common/units', game = game, merge_levels = 1)['sub_units']

def get_technologies(beta = False):
    game = 'HoI4_beta' if beta else 'HoI4'
    return pyradox.parse_merge('common/technologies', game = game, merge_levels = 1)['technologies']

def get_equipments(beta = False):
    game = 'HoI4_beta' if beta else 'HoI4'
    return pyradox.parse_merge('common/units/equipment', game = game, merge_levels = 1)['equipments']

def compute_country_tag_and_name(filename):
    m = re.match('.*([A-Z]{3})\s*-\s*(.*)\.txt$', filename)
    return m.group(1), m.group(2)
    
def get_countries(beta = False, date = '1936.1.1'):
    game = 'HoI4_beta' if beta else 'HoI4'
    
    countries = {}

    for filename, country in pyradox.txt.parse_dir(('history', 'countries'), game = game):
        country = country.at_time(date)
        tag, name = compute_country_tag_and_name(filename)
        country['tag'] = tag
        if 'set_politics' in country and 'ruling_party' in country['set_politics'] and country['set_politics']['ruling_party']:
            ruling_party = country['set_politics']['ruling_party']
        else:
            ruling_party = 'neutrality'
        country['ruling_party'] = ruling_party

        localisation_key = '%s_%s' % (tag, ruling_party)
        country['name'] = pyradox.yml.get_localisation(localisation_key, game = game) or localisation_key
        countries[tag] = country
    
    return countries
    
    
def get_states(beta = False):
    game = 'HoI4_beta' if beta else 'HoI4'
    result = pyradox.parse_merge(['history', 'states'], game = 'HoI4')
    result.replaced_key_with_subkey('state', 'id')
    return result