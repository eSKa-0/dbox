#!/usr/bin/python
try:
    from tqdm import tqdm; import os; import json; import sys; from urllib.request import urlretrieve; from datetime import datetime; import platform; from pathlib import Path; import shutil
except:
    print("Not all dependencies have been installed!!")
    sys.exit(1)
def get_install_path(name):
    if platform.system() == "Windows":
        return Path(os.getenv("ROAMING"), "rbox", name)
    elif platform.system() == "Linux":
        return Path(Path.home(), "Applications", name)
    else:
        return Path(Path.home(), "Library", "Application Support", name)
def remove_pkg(name, skip):
    try:
        install_path = get_install_path(name)
        if not install_path.exists():
            print(f"{name} has not yet been installed!")
        if not skip:
            c = input(f"Are you sure you want to remove {name}? (Y/N): ").lower()
            if c != "y":
                print("Removal has been cancelled")
                return
        shutil.rmtree(install_path)
        print(f"Removal of {name} succecsfull")
    except Exception as e:
        print(f"Something unexpected happened while removing {name} : {str(e)}, Please try again!")
def update_pkglist():
    url = "https://raw.githubusercontent.com/eska-0/dbox/refs/heads/main/packages.json"
    try:
        try:
            with open(get_install_path("packages.json"), 'r') as r:
                data = json.load(r)
            url = data.get('updateurl')
            print("Updating packagelist.")
            urlretrieve(url, get_install_path("packages.json"))
            print("Packagelist was updated.")
        except:
            print("Package list is missing or corrupted...")
            print("Installing package list.")
            urlretrieve(url, get_install_path("packages.json"))
            print("Packagelist was installed.")
    except Exception as e:
        print(f"Failed to update or install packagelist: {e}")