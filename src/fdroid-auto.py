from term_args import term_args
from packages import (packages_from_file,
                        uninstall_packages,
                        download_packages,
                        install_packages)

def main():
    t_args = term_args()
    if t_args.uninstall:
        file_path = t_args.uninstall
        packages_to_uninstall = packages_from_file(file_path)
        uninstall_packages(packages_to_uninstall)

    if t_args.download:
        file_path, dir_path = t_args.download
        packages_to_download = packages_from_file(file_path)
        download_packages(packages_to_download, dir_path)

    if t_args.install:
        dir_path = t_args.install
        install_packages(dir_path)

if __name__ == '__main__':
    try:
        main()

    except (
            FileNotFoundError,
            IsADirectoryError,
            ) as error:
        print(error)
