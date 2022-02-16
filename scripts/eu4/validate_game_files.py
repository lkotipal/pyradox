import _initpath
import os, re

import pyradox

class GameFileValidator():
    """ search_typical_folders_for_utf8() can be used to find utf8 lines
        in files which should use the ANSI/cp1252 encoding """

    def __init__(self, root_folder):
        self.root_folder = root_folder

    def search_file_for_utf8(self, filename):
        """ detect utf8 lines by interpreting the lines as cp1252
            and utf8 and output lines which differ.
            Lines which can't be parsed as utf8 are ignored and lines which can't
            be parsed as cp1252 are output with a different error message"""

        with open(filename, 'rb') as file:
            lineno = 0
            for line in file.readlines():
                lineno += 1
                try:
                    cp1252string = str(line, 'cp1252')
                    try:
                        utf8string = str(line, 'utf8')
                        if utf8string != cp1252string:
                            print("Possible utf8 line {} found in {}".format(lineno, filename))
                            print('utf8: {}'.format(utf8string), end='')
                            print('1252: {}'.format(cp1252string), end='')
                            print('-------------------------------------------------------')
                    except UnicodeDecodeError:
                        pass # so its not utf8

                except UnicodeDecodeError:
                    print("non1252 line found in {}".format(filename))
                    print(line)

    def search_folder_for_utf8(self, folder):
        for root, dirs, files in os.walk(os.path.join( self.root_folder, folder)):
            for filename in files:
                self.search_file_for_utf8(os.path.join(root, filename))

    def search_typical_folders_for_utf8(self):
        for folder in ['common', 'decisions', 'events', 'history', 'missions']:
            self.search_folder_for_utf8(folder)


if __name__ == '__main__':
    validator = GameFileValidator(pyradox.get_game_directory('EU4'))
    validator.search_typical_folders_for_utf8()

