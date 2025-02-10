"""
"""
import os
import argparse


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('working_dir',
                        help='name of the working directory to change to')

    params = parser.parse_args()
    working_dir = os.path.expanduser(params.working_dir)

    os.chdir(working_dir)


if __name__ == '__main__':
    main()
