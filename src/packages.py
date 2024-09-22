import urllib.error     # URLError, HTTPError, ContentTooShortError
import urllib.request   # GET requests for downloading F-droid apks.
import subprocess       # subprocess.run for adb commands
import json             # json.load
import io               # io.DEFAULT_BUFFER_SIZE
import os               # os.path.join, os.path.listdir, os.mkdir

from rich.live import Live
from rich.table import Table
from rich.console import Group
from rich.progress import (
        BarColumn,
        Progress,
        TaskProgressColumn,
        TimeElapsedColumn,
        TimeRemainingColumn,
        DownloadColumn
        )
from defaults import CONSOLE, ERROR_STYLE, SUCCESS_STYLE

def uninstall_packages(packages: list[str]) -> tuple[int, int]:
    """
    Uninstall from Android device through ADB the .apks names listed on
    packages list[str].

    Parameters
    ----------
    
    packages : list[str]
        List of strings where each string is the name of the package to
        uninstall.

    Returns
    -------
    tuple[int, int]:
        Packages uninstalled and packages not uninstalled respectively.

    Notes
    -----
    packages_from_file() can be used as argument to packages parameter,
    because it strips whitespaces and removes comments '#'.
    
    Whether or not an error happens while uninstalling an app it will
    show a message and then continue to the next one and so on.

    Uninstallation is done by the command:
    
    adb shell pm uninstall -k --user 0
    |   |     |  |         |  |
    |   |     |  |         |  |_ Remove the apk from the default (first)
    |   |     |  |         |     user, it's like directories.
    |   |     |  |         |   
    |   |     |  |         |_ Keep cache and data, e.g: Contacts.
    |   |     |  |
    |   |     |  |_ Command there are others like install-existing
    |   |     |
    |   |     |_ Package Manager
    |   |
    |   |_ Instruction to run a command
    |
    |_ CLI Tool that communicates with the device.
    """

    table = Table(
            "N", "Package", "Message",
            title = "Uninstalling",
            highlight=True
            )

    p_uninstalled = p_not_uninstalled = 0
    uninstall_command = "adb shell pm uninstall -k --user 0".split()

    with Live(table, refresh_per_second=30, vertical_overflow="visible"):
        for idx, package in enumerate(packages):
            result = subprocess.run(
                    uninstall_command + [package],
                    capture_output=True,
                    check=False)

            # There are returncode != 0 that do not have stderr output only to
            # stdout, e.g: Failure [not installed for 0]
            message = (result.stderr if result.stderr else result.stdout)
            message = message.decode().rstrip('\n')

            # Error
            if result.returncode != 0:
                style = ERROR_STYLE
                p_not_uninstalled += 1

            else:
                style = SUCCESS_STYLE
                p_uninstalled += 1
            
            table.add_row(
                    f"{idx+1}",
                    f"{package}",
                    f"{message}",
                    style=style)

            table.add_section()

    return p_uninstalled, p_not_uninstalled

def download_packages(packages: list[str], dir_path: str) -> tuple[int, int]:
    """
    Download to a DIR_PATH in Host machine (not Android device) the
    F-droid .apks (Suggested Versions) listed on PACKAGES list[str].

    The .apks are saved in the following format:

    PackageName_SuggestedVersion.apk

    Parameters
    ----------
    
    packages : list[str]
        List of strings where each string is the name of the F-droid
        package to download.

    dir_path : str
        String containing the path to the directory where the 
        .apks are going to be stored on Host machine.

    Returns
    -------
    tuple[int, int]:
        Packages downloaded and packages not downloaded respectively.

    Notes
    -----
    packages_from_file() can be used as argument to packages parameter,
    because it strips whitespaces and removes comments '#'.

    If directory doesn't exist it creates it.

    Whether or not an error happens while downloading an app it will
    show a message and then continue to the next one and so on.

    Downloading of F-droid apps is done on the following way:

    GET request to: https://f-droid.org/api/v1/packages/[PACKAGE_NAME]
        This way we get the .json file containing the Suggested Version
        To install.

    GET request to:
        https://f-droid.org/repo/[PackageName_SuggestedVersion.apk]
        This way we get the .apk file.
    """

    table = Table(
            "N", "Package", "Message",
            title="Downloading",
            highlight=True,
            )

    p_downloaded = p_not_downloaded = 0
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    progress_columns = (
        "[progress.description]{task.description}",
        BarColumn(),
        TaskProgressColumn(),
        "Elapsed:", TimeElapsedColumn(),
        "Remaining:", TimeRemainingColumn(),
        "Memory:", DownloadColumn()
    )

    progress = Progress(*progress_columns)
    with Live(
            Group(table, progress),
            refresh_per_second=30,
            vertical_overflow="visible"):

        for idx, package in enumerate(packages):
            url = f"https://f-droid.org/api/v1/packages/{package}"
            request = urllib.request.Request(url)

            try:
                table.add_row(
                        f"{idx+1}",
                        f"{package}",
                        f"GET suggested version on: {url}")

                with urllib.request.urlopen(request) as response:
                    file = response.read()

            # Handling of urllib exceptions
            except (urllib.error.URLError,
                    urllib.error.HTTPError,
                    urllib.error.ContentTooShortError) as urllib_error:

                style = ERROR_STYLE
                message = urllib_error
                p_not_downloaded += 1
            
            else:
                version = json.loads(file)['suggestedVersionCode']
                package_full = f"{package}_{version}.apk"
                apk_url = f"https://f-droid.org/repo/{package_full}"
                path_to_save_apk = os.path.join(dir_path, package_full)
                with (open(os.path.join(dir_path, package_full), "w+b") as
                        binary_file):

                    request = urllib.request.Request(apk_url)
                    try:
                        table.add_row(
                                "",
                                "",
                                f"GET apk version on {version} on: {apk_url}")

                        with urllib.request.urlopen(request) as response:
                            size = int(response.headers["Content-Length"])
                            
                            downloading_task = progress.add_task(
                                    "Downloading...", total=size)

                            while (apk_bytes := response.read(
                                    io.DEFAULT_BUFFER_SIZE)):
                                binary_file.write(apk_bytes)
                                progress.update(
                                        downloading_task,
                                        advance=io.DEFAULT_BUFFER_SIZE)

                            progress.remove_task(downloading_task)

                    except (urllib.error.URLError,
                            urllib.error.HTTPError,
                            urllib.error.ContentTooShortError) as urllib_error:

                        style = ERROR_STYLE
                        message = urllib_error
                        p_not_downloaded += 1

                    else:
                        style = SUCCESS_STYLE
                        message = f"Sucess saved on {path_to_save_apk}"
                        p_downloaded += 1

            table.add_row(
                    "",
                    "",
                    f"{message}", style=style)

            table.add_section()


    return p_downloaded, p_not_downloaded

def install_packages(dir_path: str) -> tuple[int, int]:
    """
    Install to Android device through ADB the .apks listed on
    DIR_PATH directory str.

    Parameters
    ----------
    dir_path : str
        String containing the path to the directory where the 
        .apks are located.

    Returns
    -------
    tuple[int, int]:
        Packages installed and packages not installed respectively.

    Notes
    -----
    Whether or not an error happens while uninstalling an app it will
    show a message and then continue to the next one and so on.

    The installation command is:

    adb install

    Why is it different from the uninstall function?
        1. It's shorter (adb shell pm install --user 0)
        2. pm install requires pushing the contents (adb push) to the
           device and then 'cp' it to /data/local/tmp/ so it's easier
           just this one little command.
    """

    p_installed = p_not_installed = 0
    if not os.path.isdir(dir_path):
        CONSOLE.print(
                f"Path: {dir_path} is not a directory",
                style=ERROR_STYLE)
        return p_installed, p_not_installed
    
    # https://stackoverflow.com/questions/50540334/install-apk-using-root-handling-new-limitations-of-data-local-tmp-folder
    install_command = "adb install".split()
    packages = [apk for apk in os.listdir(dir_path) if apk.endswith('.apk')]

    if not packages:
        CONSOLE.print(
                f"No .apk files to install on {dir_path}",
                style=ERROR_STYLE)
        return p_installed, p_not_installed

    table = Table(
            "N", "Package", "Message",
            title = "Installing",
            highlight=True
            )

    with Live(table, refresh_per_second=30, vertical_overflow="visible"):
        for idx, package in enumerate(packages):
            result = subprocess.run(
                    install_command + [os.path.join(dir_path, package)],
                    capture_output=True,
                    check=False)

            # There are returncode != 0 that do not have stderr output only to
            # stdout, e.g: Failure [not installed for 0]
            message = result.stderr if result.stderr else result.stdout
            message = message.decode().rstrip('\n')

            if result.returncode != 0:
                style = ERROR_STYLE
                p_not_installed += 1

            else:
                style = SUCCESS_STYLE
                p_installed += 1

            table.add_row(
                    f"{idx+1}",
                    f"{package}",
                    f"{message}",
                    style=style)

            table.add_section()

    return p_installed, p_not_installed

def packages_from_file(file_path: str) -> list[str]:
    """
    Reads the file to get the possible packages.

    Parameters
    ----------
    file_path : str
        File location, e.g: /usr/share/doc/file.txt

    Returns
    -------
    list[str]:
        A list of string where each string is a non empty package name without
        left nor right blank spaces and finally not comments '#'.
    """

    packages = []
    with open(file_path, "r", encoding="utf-8") as file:
        while (line := file.readline()):
            # Remove everything to the right of the comment (even the \n)
            # If comment not found then only \n will be deleted.
            comment_idx = line.find('#')
            line = line[:comment_idx].strip()
            if line:
                packages.append(line)

    return packages

# Sivefunc (1 + 2 + 3 + ... + n) -> [n * (n+1)] // 2
