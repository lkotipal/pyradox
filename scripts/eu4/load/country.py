import os

import pyradox


def get_country_name(tag):
    """
    Gets the name a country by its tag according to localisation.
    """
    return pyradox.yml.get_localisation(tag, game = 'EU4')

def get_countries():
    result = pyradox.Tree()
    for filename, tree in pyradox.parse_dir(os.path.join('history', 'countries'), game='EU4'):
        tag, raw_name = pyradox.format.split_filename(filename)
        tag = tag.replace('-', '')
        result.append(tag, tree)
    return result
