import argparse
import json
import subprocess


def main():
    parser = argparse.ArgumentParser(description="Print R-builds platforms as JSON.")
    parser.add_argument(
        'platforms',
        type=str,
        nargs='?',
        default='all',
        help='Comma-separated list of platforms. Specify "all" to use all platforms (the default).'
    )
    args = parser.parse_args()
    platforms = _get_platforms(which=args.platforms)
    if "fedora-41" in platforms:
        platforms.remove("fedora-41")
    if "fedora-40" in platforms:
        platforms.remove("fedora-40")
    if "fedora-39" in platforms:
        platforms.remove("fedora-39")
    if "fedora-38" in platforms:
        platforms.remove("fedora-38")
    if "ubuntu-2404" in platforms:
        platforms.remove("ubuntu-2404")
    if "ubuntu-2204" in platforms:
        platforms.remove("ubuntu-2204")
    if "debian-11" in platforms:
        platforms.remove("debian-11")
    print(json.dumps(platforms))


def _get_platforms(which='all'):
    supported_platforms = subprocess.check_output(['make', 'print-platforms'], text=True)
    supported_platforms = supported_platforms.split()
    if which == 'all':
        return supported_platforms
    platforms = which.split(',')
    platforms = [p for p in platforms if p in supported_platforms]
    return platforms


if __name__ == '__main__':
    main()
