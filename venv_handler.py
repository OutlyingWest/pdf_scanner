# This is a script which activate venv if it is not activated
# and install missing packages.
import os
import sys
import subprocess
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict


def main():
    # Check is venv installation needs
    venv_install = False
    args = sys.argv
    for arg in args:
        if arg == '--venvinstall':
            venv_install = True

    venv_directory_name = 'venv'
    path_to_venv_python = r'venv\Scripts\python'
    install = venv_installer(venv_directory_name, path_to_venv_python, venv_install)
    
    # If venv installation needs, script install venv only (with arg --venvinstall)
    if not venv_install:
        if install == 0 or install == 1:
            requirement_list = [
                'PyMuPDF',
                'PySide6',
            ]
            install_packages(requirement_list, path_to_venv_python)


def venv_installer(venv_dir_name, path_to_venv_python, venv_install=False):
    is_windows = False
    if sys.platform == "linux" or sys.platform == "linux2":
        # linux
        print('It is a Linux system')
        print('This script do not works in it')
        return -1
    elif sys.platform == "darwin":
        # OS X
        print('It is a OS X system')
        print('This script do not works in it')
        return -1
    elif sys.platform == "win32":
        # Windows
        is_windows = True

    if is_windows:
        if venv_install:
            subprocess.call([sys.executable, '-m', 'venv', venv_dir_name])
        subprocess.call([path_to_venv_python, '-m', 'pip', 'install', '--upgrade', 'pip'])
        if not venv_install:
            return 1
    return 0


def should_install_requirement(requirement):
    should_install = False
    try:
        pkg_resources.require(requirement)
    except (DistributionNotFound, VersionConflict):
        should_install = True
    return should_install


def install_packages(requirement_list, path_to_venv_python):
    try:
        requirements = [
            requirement
            for requirement in requirement_list
            if should_install_requirement(requirement)
        ]
        if len(requirements) > 0:
            subprocess.check_call([path_to_venv_python, "-m", "pip", "install", *requirements])
        else:
            print("Requirements already satisfied.")

    except Exception as expt:
        print(expt)


if __name__ == '__main__':
    main()
