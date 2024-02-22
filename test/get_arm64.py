import argparse
import json
import subprocess
import re
import urllib.request

native_platforms = [ 'fedora-37', 'fedora-38' ]

VERSIONS_URL = 'https://cdn.posit.co/r/versions.json'

# Minimum R version for "all"
MIN_ALL_VERSION = '3.1.0'

def main():
    parser = argparse.ArgumentParser(description="Print platforms to build on native arm64 as JSON.")
    parser.add_argument(
        'platforms',
        type=str,
        nargs=1,
        default='all',
        help='Comma-separated list of platforms. Specify "all" to use all platforms (the default).'
    )
    parser.add_argument(
        'rversions',
        type=str,
        nargs=1,
        default='all',
        help='Comma-separated list of R versions. Specify "all" to use all supported R versions.'
    )
    args = parser.parse_args()
    platforms = _get_platforms(args.platforms[0])
    platforms = [p for p in platforms if p in native_platforms]
    versions = _get_versions(args.rversions[0])
    builds = [{ 'platform': x, 'rversion': y }
              for x in platforms for y in versions]
    print(json.dumps(builds))

def _get_platforms(which='all'):
    supported_platforms = subprocess.check_output(['make', 'print-platforms'], text=True)
    supported_platforms = supported_platforms.split()
    if which == 'all':
        return supported_platforms
    platforms = which.split(',')
    return platforms

def _get_versions(which='all'):
    supported_versions = sorted(_get_supported_versions(), reverse=True)
    versions = []
    for version in which.split(','):
        versions.extend(_expand_version(version, supported_versions))
    return versions

def _expand_version(which, supported_versions):
    last_n_versions = None
    if which.startswith('last-'):
        last_n_versions = int(which.replace('last-', ''))
    elif which != 'all':
        return [which] if which in supported_versions else []

    versions = {}
    for ver in supported_versions:
        # Skip unreleased versions (e.g., devel, next)
        if not re.match(r'[\d.]', ver):
            continue
        if ver < MIN_ALL_VERSION:
            continue
        minor_ver = tuple(ver.split('.')[0:2])
        if minor_ver not in versions:
            versions[minor_ver] = ver
    versions = sorted(list(versions.values()), reverse=True)

    if last_n_versions:
        return versions[0:last_n_versions]

    return versions

def _get_supported_versions():
    request = urllib.request.Request(VERSIONS_URL)
    response = urllib.request.urlopen(request)
    data = response.read()
    result = json.loads(data)
    return result['r_versions']

if __name__ == '__main__':
    main()
