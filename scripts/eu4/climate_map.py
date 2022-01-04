import _initpath
import os
import re
import collections

import pyradox
from PIL import Image


color_defs = collections.OrderedDict([
    ('default', (102, 127, 68)),
    ('tropical' , (102, 178, 48)),
    ('arid' , (216, 214, 66)),
    ('arctic' , (255, 255, 255)),
    ])

color_defs_weather = collections.OrderedDict([
    ('default', (0, 0, 0)),
    ('mild_winter', (85, 85, 85)),
    ('normal_winter', (170, 170, 170)),
    ('severe_winter', (255, 255, 255)),
    ('mild_monsoon', (0, 0, 85)),
    ('normal_monsoon', (0, 0, 170)),
    ('severe_monsoon', (0, 0, 255)),
    ])

def generate_map_and_legend(color_defs, prefer_last=True):
    legend = ''
    for name, color in color_defs.items():
        bg_color_string = '#%02x%02x%02x' % color
        r, g, b = color
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        if y >= 255 / 2:
            text_color_string = '#000000'
        else:
            text_color_string = '#ffffff'
        legend += '<span style="color:%s; background-color:%s">%s </span>' % (text_color_string, bg_color_string, name)

    print(legend)

    climate_map = {}
    for climate, province_id in pyradox.txt.parse_file(os.path.join(pyradox.get_game_directory('EU4'), 'map', 'climate.txt'), verbose=False).items():
        if climate == 'equator_y_on_province_image':
            continue
        if climate in color_defs.keys():
            if prefer_last or province_id not in climate_map:
                climate_map[province_id] = climate

    colormap = {}
    for filename, data in pyradox.txt.parse_dir(os.path.join(pyradox.get_game_directory('EU4'), 'history', 'provinces'), verbose=False):
        m = re.match('\d+', filename)
        province_id = int(m.group(0))
        if 'base_tax' not in data: continue # skip wastelands
        if province_id in climate_map:
            colormap[province_id] = color_defs[climate_map[province_id]]
        else:
            colormap[province_id] = color_defs['default']

    province_map = pyradox.worldmap.ProvinceMap(game = 'EU4')
    return province_map.generate_image(colormap, default_land_color = (93, 93, 93))

generate_map_and_legend(color_defs).save('out/Climate_map.png')

# create a shaded image
# first create an image where winter overrides monsoon(which is last in the climate.txt)
# then merge the images by alternating using three pixel form each image
prefer_monsoon_image = generate_map_and_legend(color_defs_weather)
prefer_winter_image = generate_map_and_legend(color_defs_weather, prefer_last=False)

shaded_image = Image.new(prefer_monsoon_image.mode, prefer_monsoon_image.size)
for x in range(prefer_monsoon_image.width):
        for y in range(prefer_monsoon_image.height):

            if (x+y) % 6 < 3:
                source_image_for_current_pixel = prefer_monsoon_image
            else:
                source_image_for_current_pixel = prefer_winter_image

            shaded_image.putpixel((x,y), source_image_for_current_pixel.getpixel((x,y)))

shaded_image.save('out/Weather_map.png')
