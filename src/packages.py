import subprocess

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
