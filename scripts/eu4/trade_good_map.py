import _initpath
import os
import re
import collections
import pyradox


basedir = pyradox.get_game_directory('EU4')

trade_good_colors = collections.OrderedDict([
    ('grain' , (0.96, 0.93, 0.58)),
    ('wine' , (0.36, 0.13, 0.28)),
    ('wool' , (0.83, 0.83, 0.83)),
    ('cloth' , (0.86, 0.19, 0.19)),
    ('fish' , (0.55, 0.82, 0.97)),
    ('fur' , (0.54, 0.40, 0.31)),
    ('salt' , (0.999, 0.999, 0.99)),
    ('naval_supplies' , (0.11, 0.17, 0.4)),
    
    ('copper' , (0.85, 0.46, 0.15)),
    ('gold' , (1.0, 0.84, 0.19)),
    ('iron' , (0.2, 0.2, 0.2)),
    
    ('slaves' , (0.0, 0.0, 0.0)),
    ('ivory' , (0.75, 0.75, 0.63)),
    
    ('tea' , (0.07, 0.33, 0.09)),
    ('chinaware' , (0.18, 0.57, 0.8)),
    ('spices' , (0.4, 0.65, 0.38)),

    ('coffee' , (0.22, 0.15, 0.09)),
    ('cotton' , (0.52, 0.68, 0.6)),
    ('sugar' , (0.74, 0.95, 0.68)),
    ('tobacco' , (0.33, 0.56, 0.38)),

    ('cocoa' , (0.45, 0.21, 0.09)),
    ('silk' , (0.72, 0.19, 0.10)),
    ('dyes' , (0.63, 0.17, 0.5)),
    ('tropical_wood' , (0.45, 0.47, 0.09)),
    ('livestock' , (0.72, 0.49, 0.44)),
    ('incense' , (0.89, 0.79, 0.47)),
    ('glass' , (0.0, 0.60, 0.45)),
    ('paper' , (0.9, 0.86, 0.71)),
    ('gems' , (0.96, 0.78, 0.78)),
    ('coal' , (0.0, 1.0, 1.0)),
    ('cloves' , (1.0, 0.5, 0.85)),

    ('unknown' , (0.5, 0.5, 0.5)),

    ('damestear' , (0, 230, 230)),
    ('precursor_relics' , (230, 230, 30)),
    ('mithril' , (220, 238, 251)),
    ('fungi' , (86, 51, 63)),
    ('serpentbloom' , (82, 15, 106)),
])

for trade_good, color in trade_good_colors.items():
    if (isinstance(color[0], float)):
        trade_good_colors[trade_good] = tuple(int(255 * rgb) for rgb in color)


legend = ''
for trade_good, color in trade_good_colors.items():
    bg_color_string = '#%02x%02x%02x' % color
    r, g, b = color
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if y >= 255 / 2:
        text_color_string = '#000000'
    else:
        text_color_string = '#ffffff'
    #legend += '<span style="color:%s; background-color:%s">%s </span>' % (text_color_string, bg_color_string, trade_good)
    legend += f'| style="color:{text_color_string}; background-color:{bg_color_string}" | {trade_good}\n'

print(legend)

colormap = {}
for filename, data in pyradox.txt.parse_dir(os.path.join(basedir, 'history', 'provinces'), verbose=False):
    m = re.match('\d+', filename)
    province_id = int(m.group(0))
    if 'trade_goods' in data:
        colormap[province_id] = trade_good_colors[data['trade_goods']]
        
province_map = pyradox.worldmap.ProvinceMap(basedir)
out = province_map.generate_image(colormap)
out.save('out/trade_good_map.png')


