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
