'''Quite possibly the most simplistic remotely available ci server ever created'''
import json
import os
import sys
from contextlib import contextmanager
from subprocess import PIPE, Popen
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import hot_redis as redis
import hug
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageColor import getrgb as color
from sh import cd, ci_worker, git, pwd

__version__ = '0.0.1'

NOT_FOUND = -1
REDIS_AUTH = urlparse(os.environ.get('REDISCLOUD_URL'))
redis.configure({'host': REDIS_AUTH.hostname, 'port': REDIS_AUTH.port or 6379, 'password': REDIS_AUTH.password})


def draw_pin(text, background_color='green', font_color='white'):
    '''Draws and returns a pin with the specified text and color scheme'''
    image = Image.new('RGB', (120, 20))
    draw = Image.Draw(image)
    draw.rectangle([(1, 1), (118, 18)], fill=color(background_color))
    draw.text((10, 4), text, fill=color(font_color))
    return image


def pin(value):
    '''A small pin that represents the result of the build process'''
    if value is False:
        return draw_pin('Build Failed', 'red', 'black')
    elif value is True:
        return draw_pin('Build Passed')
    elif value is NOT_FOUND:
        return draw_pin('Build N / A', 'lightGray')
    return draw_pin('In progress ...', 'lightGray', 'black')


@contextmanager
def repository(namespace, name, branch='master'):
    '''Returns a repository'''
    with TemporaryDirectory() as download_path:
        old_directory = pwd()
        git.clone('https://github.com/{0}/{1}.git'.format(namespace, name), download_path)
        cd(download_path)
        git.fetch('origin', branch)
        git.checkout(branch)
        yield (download_path, git('rev-parse', 'HEAD'), redis.Dict(key=download_path))
        cd(old_directory)


def ci_data(namespace, name, branch='master'):
    '''Returns or starts the ci data collection process'''
    with repository(namespace, name, branch) as (path, latest, cache):
        if not repo:
            return {'build_success': NOT_FOUND, 'status': NOT_FOUND}

        if latest in cache:
            return json.loads(cache['latest'])
        return cache.setdefault(latest, json.dumps({'status': 'starting'}))


@hug.get('/ci/{namespace}/{name}/status.png', output=hug.output_format.png_image)
def build_status(namespace, name, branch='master') -> pin:
    '''Returns the current status of the build'''
    return ci_data(namespace, name, branch).get('build_success', None)


@hug.get('/ci/{namespace}/{name}', output=hug.output_format.text)
def build_text(namespace, name, branch='master'):
    '''Returns the current text stored for the build'''
    return ci_data(namespace, name, branch).get('result', '')


@hug.cli('ci_worker', version=__version__)
def worker(namespace, name, branch='master'):
    '''The simple_ci background worker process'''
    with repository(namespace, name, branch) as (path, latest, cache):
        if latest in cache and json.loads(cache[latest])['status'] != 'starting':
            return 'Build already started'

    data = {'status': 'in_progress', 'result': ''}
    cache[latest] = json.dumps(data)
    with Popen(('tox'), stdout=PIPE, buffsize=1, universal_newlines=True) as tox:
        for line in tox.stdout:
            data['result'] += line
            cache[latest] = json.dumps(data)
    data['build_success'] = True if tox.returncode == 0 else False
    data['status'] = 'complete'
    cache[latest] = json.dumps(data)
    return 'Build successfully completed'
