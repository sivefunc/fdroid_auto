from term_args import term_args
from packages_from_file import packages_from_file

def main():
    t_args = term_args()
    if t_args.uninstall:
        file_path = t_args.uninstall
        uninstall_packages = packages_from_file(file_path)

if __name__ == '__main__':
    main()
