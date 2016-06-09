import logging
import os
import sys
import time

server = os.getenv('AMO_SERVER', 'https://addons.mozilla.org')
directory = '../data'

level = int(os.getenv('AMO_LOGGING_LEVEL', logging.DEBUG))
logging.basicConfig(stream=sys.stdout, level=level)
log = logging.getLogger('mirror')


def get_directories(addon_id):
    addon_id = str(addon_id)
    first, second = addon_id[0], addon_id[:2]
    root = os.path.join(directory, first, second, addon_id)
    directories = {
        'root': root,
        'changes': os.path.join(root, 'changes'),
        'files': os.path.join(root, 'files'),
    }

    for d in directories.values():
        if not os.path.exists(d):
            os.makedirs(d)

    return directories


def get_files(addon_id):
    directories = get_directories(addon_id)
    files = {
        'root': os.path.join(directories['root'], 'addon.json'),
        'backup': os.path.join(
            directories['changes'],
            'addon.{}.json'.format(str(time.time())))
    }
    return files
