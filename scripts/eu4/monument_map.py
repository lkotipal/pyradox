import _initpath
import os
import pyradox

colormap = {}
monuments = {}
textmap = {}
for filename, data in pyradox.txt.parse_dir(os.path.join(pyradox.get_game_directory('EU4'), 'common', 'great_projects'), verbose=False):
    for name, monument_data in data.items():
        display_name = pyradox.yml.get_localisation(name, 'EU4')
        if monument_data['type'] == 'monument':
            monuments[display_name] = monument_data['start']
            colormap[monument_data['start']] = (183, 25, 25)
        else:
            textmap[monument_data['start']] = display_name
            colormap[monument_data['start']] = (0, 38, 255)

# sort the monuments alphabetically and give them a number starting by 1 so that it matches the number on the wiki
i = 1
for display_name in sorted (monuments):
    if monuments[display_name] in textmap:
        textmap[monuments[display_name]] += '/' + str(i)
    else:
        textmap[monuments[display_name]] = str(i)
    i += 1

province_map = pyradox.worldmap.ProvinceMap(game = 'EU4')
out = province_map.generate_image(colormap, default_land_color=(211, 211, 211), default_water_color=(127,127,127), edge_width=0)
province_map.overlay_text(out, textmap,
                            fontfile='Arial_Black.ttf',
                          antialias=True, fontsize=16)
pyradox.image.save_using_palette(out, 'out/Location of Monuments.png')
