import hoi4
import csv
import os
import re
import collections




import pyradox

static_modifiers = pyradox.txt.parse_file(os.path.join(pyradox.get_game_directory('HoI4'), 'common', 'modifiers', '00_static_modifiers.txt'))

def compute_name(k, v):
    return pyradox.format.human_string(k.replace('weather_', ''), cap_first = True)

def is_precipitation(k, v):
    return 'weather' in k and 'air_accidents' in v

def is_temperature(k, v):
    return 'cold' in k or 'hot' in k

def is_ground_effect(k, v):
    return 'mud' in k or 'ground_snow' in k

def is_weather(k, v):
    return 'weather' in k or k == 'night'

allcolumns = (
    ('Condition', compute_name),
    ('Attrition', lambda k, v: pyradox.table.wiki_colored_percent_string(v['attrition'], color = 'red')),
    ('Winter attrition', lambda k, v: pyradox.table.wiki_colored_percent_string(v['winter_attrition'], color = 'red')),
    ('Land speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['army_speed_factor'], color = 'red')),
    ('Recovery rate', '{{red|%(local_org_regain)0.2f}}'),
    ('Entrenchment speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['dig_in_speed_factor'], color = 'red')),
    ('Naval speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_speed_factor'], color = 'red')),
    ('Naval detection', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_detection'], color = 'red')),
    ('Naval hit chance', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_hit_chance'], color = 'red')),
    ('Air accidents', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_accidents'], color = 'red')),
    ('Air detection', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_detection'], color = 'red')),
    ('Bombing targeting', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_bombing_targetting'], color = 'red')),
    ('Naval strike', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_strike'], color = 'red')),
    )

precipitation_columns = (
    ('Condition', compute_name),
    ('Recovery rate', '{{red|%(local_org_regain)0.2f}}'),
    ('Naval speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_speed_factor'], color = 'red')),
    ('Naval detection', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_detection'], color = 'red')),
    ('Naval hit chance', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_hit_chance'], color = 'red')),
    ('Air accidents', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_accidents'], color = 'red')),
    ('Air detection', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_detection'], color = 'red')),
    ('Bombing targeting', lambda k, v: pyradox.table.wiki_colored_percent_string(v['air_bombing_targetting'], color = 'red')),
    ('Carrier aircraft can take off', lambda k, v: '{{red|No}}' if 'carrier_traffic' in v else ''),
    ('Naval strike efficiency', lambda k, v: pyradox.table.wiki_colored_percent_string(v['naval_strike'], color = 'red')),
    )

temperature_columns = (
    ('Condition', compute_name),
    ('Attrition', lambda k, v: pyradox.table.wiki_colored_percent_string(v['attrition'], color = 'red')),
    ('Winter attrition', lambda k, v: pyradox.table.wiki_colored_percent_string(v['winter_attrition'], color = 'red')),
    ('Recovery rate', '{{red|%(local_org_regain)0.2f}}'),
    ('Entrenchment speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['dig_in_speed_factor'], color = 'red')),
    )

ground_effect_columns = (
    ('Condition', compute_name),
    ('Attrition', lambda k, v: pyradox.table.wiki_colored_percent_string(v['attrition'], color = 'red')),
    ('Land speed', lambda k, v: pyradox.table.wiki_colored_percent_string(v['army_speed_factor'], color = 'red')),
    ('Recovery rate', '{{red|%(local_org_regain)0.2f}}'),
    )

file = open("out/weather.txt", "w")

file.write(pyradox.table.make_table(static_modifiers, 'wiki', precipitation_columns, filter_function = is_precipitation))

file.write(pyradox.table.make_table(static_modifiers, 'wiki', temperature_columns, filter_function = is_temperature))

file.write(pyradox.table.make_table(static_modifiers, 'wiki', ground_effect_columns, filter_function = is_ground_effect))
file.close()
