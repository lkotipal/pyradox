import _initpath
import os
import pyradox

locations = {
    "beikdugang_arsenal": 4908,
    "beikdugang_lights": 4907,
    "anzarzax_palace": 590,
    "elikhander_pyramid": 769,
    "elikhander_orbs": 759,
    "elikhander_sphinx": 756,
    "scp_bureau_hq": 1019,
    "icgm": 2931,
    "ravioli_bastion": 898,
    "feiten_aerodrome": 4879,
}

colormap = {}
monuments = {}
textmap = {}
for filename, data in pyradox.txt.parse_dir(os.path.join(pyradox.get_game_directory('EU4'), 'common', 'great_projects'), verbose=False):
    for name, monument_data in data.items():
        display_name = pyradox.yml.get_localisation(name, 'EU4')
        prov = monument_data['start']

        if (name in locations.keys()):
            prov = locations[name]

        if (not prov):
            print(name)

        if monument_data['type'] == 'monument':
            monuments[display_name] = monument_data['start']
            colormap[prov] = (183, 25, 25)
        else:
            if (not prov):
                try:
                    provs = list(monument_data['on_destroyed'].keys())
                    textmap[provs[1]] = display_name
                    for prov in provs[1:]:
                        colormap[prov] = (0, 38, 255)
                except:
                    continue
            else:
                textmap[prov] = display_name
                colormap[prov] = (0, 38, 255)

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
