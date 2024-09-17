from term_args import term_args
from packages import (packages_from_file,
                        uninstall_packages)

def main():
    t_args = term_args()
    if t_args.uninstall:
        file_path = t_args.uninstall
        packages_to_uninstall = packages_from_file(file_path)
        uninstall_packages(packages_to_uninstall)

if __name__ == '__main__':
    main()
