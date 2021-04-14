#!/usr/bin/python3

# Checks if `url` and `iconUrl` (if it exists) are valid
# Usage: ./check_urls.py manifests/
# Usage: ./check_urls.py myPlugin.yaml
import os
import yaml
import sys
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import urlopen, Request


def check_url(url):
    print("  Testing " + url)
    try:
        conn = urlopen(Request(url, method="HEAD"))
        return True
    except HTTPError as e:
        print("  %s: %s" % (e.code, e.reason))
        return False


def check_plugin(file):
    print("Checking " + file)
    with open(file, "r") as f:
        manifest = yaml.load(f, Loader=yaml.FullLoader)

    url_valid = check_url(manifest["url"])
    if "iconUrl" in manifest:
        icon_url_valid = check_url(manifest["iconUrl"])
    else:
        icon_url_valid = True
    return url_valid and icon_url_valid


target = sys.argv[1]
files = []
if os.path.isdir(target):
    for filename in os.listdir(target):
        files.append(os.path.join(target, filename))
else:
    files = [target]

success = True
for file in files:
    if not check_plugin(file):
        success = False

if not success:
    exit(1)
