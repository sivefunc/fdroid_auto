""" Single function just to parse CLI args """

from .version import __version__
import argparse
import sys

def term_args() -> argparse.Namespace:
    """
    Analyzes sys.argv to map the text to options.

    Parameters
    ----------
    None

    Returns
    -------
    argparse.Namespace
        C struct in python where each member is an option. 
    """

    parser = argparse.ArgumentParser(
            prog="fdroid_auto",
            formatter_class=argparse.RawTextHelpFormatter,
            usage='%(prog)s [options]',
            description=
"""
F-droid auto is a very little program that automates the process of:

    First                   Second                  Last
 ______________          _____________          ____________
|              |        |  internet   |        |            |
| Uninstalling | ---->  | Downloading | -----> | Installing |
.______________.        ._____________.        .____________.

F-droid apks through ADB.
""")

    parser.add_argument(
            '-v','--version',
            action='version',
            version=f"""
%(prog)s v{__version__}
Copyright (C) 2024 Sivefunc
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by a human""")

    parser.add_argument(
            '-u', '--uninstall',
            help="Uninstall ALL packages listed from FILE on device using adb",
            type=str,
            metavar="[FILE]")

    parser.add_argument(
            '-d', '--download',
            help="Download ALL fdroid .apks listed from FILE and push them into"
                " " "DIR",
            type=str,
            nargs=2,
            metavar=("[FILE]", "[DIR]"))

    parser.add_argument(
            '-i', '--install',
            help="Install ALL packages .apk listed from DIR on device using"
                " " "adb",
            type=str,
            metavar="[DIR]")

    parser.add_argument(
            '-n','--notation',
            action='version',
            help="Shows how to format the FILE and exit",
            version="""
Comments
Written using the hash symbol '#'
Everything after a '#' get's ignored.
Empty lines will be deleted.

e.g This is a comment
-------------------------------------------------------------------------------
Packages names

These follow the normal android package name convention:
http://stackoverflow.com/questions/6273892/ddg#6273935

e.g:

org.fdroid.fdroid
-------------------------------------------------------------------------------
Check apps/uninstall.txt and apps/download.txt to know the examples.
""")

    # No arguments given, I just decided to leave it here.
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args
