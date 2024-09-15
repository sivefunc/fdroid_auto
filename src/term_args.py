import argparse

def term_args():
    parser = argparse.ArgumentParser(
            prog="fdroid-auto",
            formatter_class=argparse.RawTextHelpFormatter,
            usage='%(prog)s [options]',
            description="Little program to automate installation and removal"
                        " of android apps.")

    parser.add_argument(
            '-v','--version',
            action='version',
            version="""
%(prog)s v1.0.0
Copyright (C) 2024 Sivefunc
License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by a human""")

    parser.add_argument(
            '-u', '--unistall',
            help="Uninstall packages listed from FILE on device using adb",
            type=str,
            metavar="[FILE]")

    parser.add_argument(
            '-i', '--install',
            help="Install packages .apk listed from DIR on device using adb",
            type=str,
            metavar="[DIR]")

    parser.add_argument(
            '-d', '--download',
            help="Download fdroid packages listed from FILE using API + wget",
            type=str,
            metavar="[FILE]")

    args = parser.parse_args()
    return args
