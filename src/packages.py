import urllib.request   # GET requests for downloading F-droid apks.
import subprocess       # subprocess.run for adb commands
import json             # json.load
import io               # io.DEFAULT_BUFFER_SIZE
import os               # os.path.join

def uninstall_packages(packages: list[str]) -> tuple[int, int]:
    p_uninstalled = p_not_uninstalled = 0
    uninstall_command = "adb shell pm uninstall -k --user 0".split()
    for idx, package in enumerate(packages):
        result = subprocess.run(
                uninstall_command + [package],
                capture_output=True)

        # There are returncode != 0 that do not have stderr output only to
        # stdout, e.g: Failure [not installed for 0]
        message = result.stderr if result.stderr else result.stdout
        message = str(message)[2:-3] # Remove b' prefix
                                     # Remove '\n suffix
        if result.returncode != 0:
            p_not_uninstalled += 1

        else:
            p_uninstalled += 1

        print(f"{idx+1}|{package}: {message}")

    return p_uninstalled, p_not_uninstalled

def download_packages(packages: list[str], dir_path: str) -> tuple[int, int]:
    p_downloaded = p_not_downloaded = 0
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    for idx, package in enumerate(packages):
        url = f"https://f-droid.org/api/v1/packages/{package}"
        request = urllib.request.Request(url)

        try:
            print(f"GET suggested version on: {url}")
            with urllib.request.urlopen(request) as response:
                file = response.read()

        except Exception as error:
            message = error
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
                    print(f"GET apk version {version} on: {apk_url}")
                    with urllib.request.urlopen(request) as response:
                        while (apk_bytes := response.read(
                                io.DEFAULT_BUFFER_SIZE)):
                            binary_file.write(apk_bytes)
                    
                except Exception as error:
                    message = error
                    p_not_downloaded += 1

                else:
                    message = f"Sucess saved on {path_to_save_apk}"
                    p_downloaded += 1

        print(f"{idx+1} | {package}: {message}")

    return p_downloaded, p_not_downloaded

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
    with open(file_path, "r") as file:
        while (line := file.readline()):
            # Remove everything to the right of the comment (even the \n)
            # If comment not found then only \n will be deleted.
            comment_idx = line.find('#')
            line = line[:comment_idx].strip()
            if line:
                packages.append(line)

    return packages

# Sivefunc (1 + 2 + 3 + ... + n) -> [n * (n+1)] // 2
