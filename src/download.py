import json
import os
import requests

from utils import log, server, directory, get_directories

from parse import parse


def download(addon):
    # TODO: prevent multiple downloads.
    current = addon['current_version']
    for file_obj in current['files']:
        url = file_obj['url']
        filename = file_obj['id']

        directories = get_directories(addon['id'])
        target = '{}.xpi'.format(
            os.path.join(directories['files'], str(file_obj['id'])),
        )

        if os.path.exists(target):
            log.info('{}: Skipping download'.format(addon['id']))
            continue

        res = requests.get(url)
        if res.status_code == 404:
            log.warning('{}: got a 404'.format(addon['id']))
            continue
        else:
            res.raise_for_status()

        with open(target, 'wb') as filehandle:
            for chunk in res.iter_content(10000):
                filehandle.write(chunk)

        log.info('{}: Downloaded file: {}'.format(addon['id'], file_obj['id']))


def downloads(addons):
    for k, addon in enumerate(addons):
        # Only download 1 in 100.
        if not k % 100:
            download(addon)


if __name__=='__main__':
    downloads(parse('is_extension'))
