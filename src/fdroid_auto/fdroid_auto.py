"""
This is the entry point where everything is going to start being executed.
python3 fdroid_auto.py --help
To get you informated and If wanna look deeper read the code.
"""

from .defaults import CONSOLE, SUCCESS_STYLE, ERROR_STYLE
from .term_args import term_args
from .packages import (packages_from_file,
                        uninstall_packages,
                        download_packages,
                        install_packages)

def main():
    """
    F-droid auto is a very little program that automates the process of:
     ______________          _____________          ____________
    |              |        |  internet   |        |            |
    | Uninstalling | ---->  | Downloading | -----> | Installing |
    .______________.        ._____________.        .____________.

    F-droid apks through ADB.
    """

    t_args = term_args()

    # First step
    if t_args.uninstall:
        file_path = t_args.uninstall
        p_uninstall = p_not_uninstall = 0
        try:
            packages_to_uninstall = packages_from_file(file_path)

        except FileNotFoundError:
            CONSOLE.print(
                    f"File with the packages to uninstall doesn't exist:"
                    " " f"{file_path}",
                    style=ERROR_STYLE)

        except IsADirectoryError:
            CONSOLE.print(
                    f"Path: {file_path} is a directory and not a file with the"
                    " " "packages to uninstall",
                    style=ERROR_STYLE)
        else:
            p_uninstall, p_not_uninstall = uninstall_packages(
                                                packages_to_uninstall)

        CONSOLE.print(
                f"{p_uninstall} Packages were uninstalled",
                style=SUCCESS_STYLE)

        CONSOLE.print(
                f"{p_not_uninstall} Packages were not uninstalled",
                style=ERROR_STYLE)

    # Second step
    if t_args.download:
        file_path, dir_path = t_args.download
        p_download = p_not_download = 0
        try:
            packages_to_download = packages_from_file(file_path)

        except FileNotFoundError:
            CONSOLE.print(
                    f"File with the packages to download doesn't exist:"
                    " " f"{file_path}",
                    style=ERROR_STYLE)

        except IsADirectoryError:
            CONSOLE.print(
                    f"Path: {file_path} is a directory and not a file with the"
                    " " "packages to download.",
                    style=ERROR_STYLE)
        else:
            p_download, p_not_download = download_packages(
                                            packages_to_download, dir_path)

        CONSOLE.print(
                f"{p_download} Packages were downloaded",
                style=SUCCESS_STYLE)

        CONSOLE.print(
                f"{p_not_download} Packages were not downloaded",
                style=ERROR_STYLE)

    # Last step
    if t_args.install:
        dir_path = t_args.install
        p_install, p_not_install = install_packages(dir_path)
        CONSOLE.print(
                f"{p_install} Packages were installed",
                style=SUCCESS_STYLE)

        CONSOLE.print(
                f"{p_not_install} Packages were not installed",
                style=ERROR_STYLE)

if __name__ == '__main__':
    main()
