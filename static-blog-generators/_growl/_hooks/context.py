"""
Load config.yml into blog context
"""

import yaml
import os

try:
    config = open(os.path.join(Site.BASE_DIR, '_config.yml')).read()
except (OSError, IOError):
    config = ''


data = yaml.load(config)
Site.CONTEXT.blog = AttrDict(data or {})
